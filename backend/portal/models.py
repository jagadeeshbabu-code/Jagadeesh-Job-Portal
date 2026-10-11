from django.conf import settings
from django.db import models

class Profile(models.Model):
    CANDIDATE = "candidate"
    EMPLOYER = "employer"
    ROLE_CHOICES = [(CANDIDATE, "Candidate"), (EMPLOYER, "Employer")]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=12, choices=ROLE_CHOICES, default=CANDIDATE)
    company = models.CharField(max_length=160, blank=True)
    resume = models.FileField(upload_to="resumes/%Y/%m/", blank=True)
    bio = models.TextField(blank=True)

    def __str__(self): return f"{self.user.username} ({self.role})"

class Job(models.Model):
    EMPLOYMENT_CHOICES = [("Full-time", "Full-time"), ("Part-time", "Part-time"), ("Contract", "Contract"), ("Remote", "Remote")]
    title = models.CharField(max_length=180)
    company = models.CharField(max_length=160)
    location = models.CharField(max_length=160)
    category = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_CHOICES, default="Full-time")
    salary = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="jobs")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: ordering = ["-created_at"]
    def __str__(self): return f"{self.title} at {self.company}"

class Application(models.Model):
    STATUS_CHOICES = [("submitted", "Submitted"), ("reviewing", "Reviewing"), ("interview", "Interview"), ("rejected", "Not selected"), ("hired", "Hired")]
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="submitted")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [models.UniqueConstraint(fields=["job", "candidate"], name="unique_job_application")]
    def __str__(self): return f"{self.candidate} → {self.job}"
