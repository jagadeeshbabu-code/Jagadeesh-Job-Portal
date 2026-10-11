from django.contrib import admin
from .models import Application, Job, Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin): list_display = ("user", "role", "company"); list_filter = ("role",); search_fields = ("user__username", "user__email", "company")
@admin.register(Job)
class JobAdmin(admin.ModelAdmin): list_display = ("title", "company", "location", "is_active", "created_at"); list_filter = ("is_active", "category"); search_fields = ("title", "company")
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin): list_display = ("job", "candidate", "status", "created_at"); list_filter = ("status",)
