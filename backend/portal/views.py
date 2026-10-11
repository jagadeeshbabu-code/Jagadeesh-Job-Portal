from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Application, Job, Profile
from .serializers import ApplicationSerializer, JobSerializer, RegisterSerializer, UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all(); serializer_class = RegisterSerializer; permission_classes = [permissions.AllowAny]

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request): return Response(UserSerializer(request.user).data)

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def patch(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        if "resume" in request.FILES:
            file = request.FILES["resume"]
            if file.size > 5 * 1024 * 1024: return Response({"resume": "Maximum file size is 5 MB."}, status=400)
            if not file.name.lower().endswith((".pdf", ".doc", ".docx")): return Response({"resume": "Upload a PDF or Word document."}, status=400)
            profile.resume = file
        profile.bio = request.data.get("bio", profile.bio)
        profile.save()
        return Response(UserSerializer(request.user).data)

class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    def get_queryset(self):
        qs = Job.objects.select_related("posted_by")
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            qs = qs.filter(is_active=True)
        params = self.request.query_params
        q = params.get("q")
        if q: qs = qs.filter(Q(title__icontains=q) | Q(company__icontains=q) | Q(description__icontains=q) | Q(category__icontains=q))
        if params.get("location"): qs = qs.filter(location__icontains=params["location"])
        if params.get("category"): qs = qs.filter(category__iexact=params["category"])
        return qs
    def perform_create(self, serializer):
        if not self.request.user.is_staff and not getattr(getattr(self.request.user, "profile", None), "role", "") == Profile.EMPLOYER:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Employer access is required to post a job.")
        serializer.save(posted_by=self.request.user)
    def perform_update(self, serializer):
        if not (self.request.user.is_staff or serializer.instance.posted_by_id == self.request.user.id):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only edit your own listings.")
        serializer.save()
    def perform_destroy(self, instance):
        if not (self.request.user.is_staff or instance.posted_by_id == self.request.user.id):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only remove your own listings.")
        instance.delete()

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        qs = Application.objects.select_related("job", "candidate", "job__posted_by")
        if user.is_staff: return qs
        return qs.filter(candidate=user) | qs.filter(job__posted_by=user)
    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated: return Response({"detail": "Log in to apply."}, status=401)
        if Application.objects.filter(job_id=request.data.get("job"), candidate=request.user).exists():
            return Response({"detail": "You have already applied."}, status=400)
        return super().create(request, *args, **kwargs)
    def perform_create(self, serializer): serializer.save(candidate=self.request.user, status="submitted")
    def perform_update(self, serializer):
        if not self.request.user.is_staff and serializer.instance.job.posted_by_id != self.request.user.id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only the employer can update application status.")
        serializer.save()
    def perform_destroy(self, instance):
        if not (self.request.user.is_staff or instance.candidate_id == self.request.user.id):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied()
        instance.delete()
