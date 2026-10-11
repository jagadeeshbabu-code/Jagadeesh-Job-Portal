from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Application, Job, Profile

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="profile.role", read_only=True)
    company = serializers.CharField(source="profile.company", read_only=True)
    resume = serializers.FileField(source="profile.resume", read_only=True)
    bio = serializers.CharField(source="profile.bio", read_only=True)
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role", "company", "resume", "bio"]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name"]
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Profile.objects.get_or_create(user=user)
        return user

class JobSerializer(serializers.ModelSerializer):
    posted_by_name = serializers.CharField(source="posted_by.get_full_name", read_only=True)
    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ["posted_by", "created_at"]

class ApplicationSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source="candidate.get_full_name", read_only=True)
    candidate_email = serializers.EmailField(source="candidate.email", read_only=True)
    job_title = serializers.CharField(source="job.title", read_only=True)
    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ["candidate", "created_at"]
