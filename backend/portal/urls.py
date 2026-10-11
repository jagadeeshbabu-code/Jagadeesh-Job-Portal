from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ApplicationViewSet, JobViewSet, MeView, ProfileView, RegisterView

router = DefaultRouter()
router.register("jobs", JobViewSet, basename="job")
router.register("applications", ApplicationViewSet, basename="application")
urlpatterns = [
    path("auth/register/", RegisterView.as_view()), path("auth/login/", TokenObtainPairView.as_view()),
    path("auth/refresh/", TokenRefreshView.as_view()), path("auth/me/", MeView.as_view()),
    path("profile/", ProfileView.as_view()), path("", include(router.urls)),
]
