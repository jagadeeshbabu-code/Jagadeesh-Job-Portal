from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from portal.models import Job, Profile


SAMPLE_JOBS = [
    {
        "title": "Product Designer",
        "company": "Fieldnotes Studio",
        "location": "Remote · North America",
        "category": "Design",
        "employment_type": "Full-time",
        "salary": "$110k–$145k",
        "description": "Help a small, kind team make everyday tools feel clear and welcoming. You will work closely with research, product, and engineering from early ideas through launch.",
        "requirements": "A thoughtful portfolio, strong interaction design skills, and comfort working through open-ended problems.",
    },
    {
        "title": "Frontend Engineer",
        "company": "Morrow Health",
        "location": "Austin, TX · Hybrid",
        "category": "Engineering",
        "employment_type": "Full-time",
        "salary": "$125k–$165k",
        "description": "Build simple, accessible experiences that help people take care of their health. Partner with design and product to ship improvements every week.",
        "requirements": "Experience building production web interfaces with React, a focus on accessibility, and a collaborative approach.",
    },
    {
        "title": "Community Marketing Manager",
        "company": "Common Ground",
        "location": "Remote · US",
        "category": "Marketing",
        "employment_type": "Full-time",
        "salary": "$90k–$120k",
        "description": "Grow a generous community around practical climate solutions. Create useful stories and programs alongside the people who use our products.",
        "requirements": "Clear writing, experience building community programs, and care for evidence-led storytelling.",
    },
    {
        "title": "People Operations Partner",
        "company": "Juniper Works",
        "location": "Chicago, IL · Hybrid",
        "category": "People",
        "employment_type": "Full-time",
        "salary": "$105k–$135k",
        "description": "Make the employee experience more thoughtful as our team grows. You will work across onboarding, manager support, and people programs.",
        "requirements": "Hands-on people operations experience, good judgment with sensitive information, and a practical mindset.",
    },
    {
        "title": "Product Data Analyst",
        "company": "Goodwell Learning",
        "location": "Remote · US",
        "category": "Data",
        "employment_type": "Full-time",
        "salary": "$100k–$130k",
        "description": "Help our product teams understand how people learn. Turn questions into clear analysis that guides experiments and product decisions.",
        "requirements": "Strong SQL, clear communication, and experience translating product data into useful recommendations.",
    },
]


class Command(BaseCommand):
    help = "Create sample job listings for a local development workspace."

    def handle(self, *args, **options):
        User = get_user_model()
        owner = User.objects.filter(is_superuser=True).first()
        if owner is None:
            owner, created = User.objects.get_or_create(
                username="jagadeesh-demo",
                defaults={"email": "demo@example.invalid", "first_name": "Jagadeesh demo"},
            )
            if created:
                owner.set_unusable_password()
                owner.save(update_fields=["password"])
            Profile.objects.update_or_create(user=owner, defaults={"role": Profile.EMPLOYER, "company": "Jagadeesh Job Portal"})
        for sample in SAMPLE_JOBS:
            Job.objects.update_or_create(
                title=sample["title"],
                company=sample["company"],
                defaults={**sample, "posted_by": owner, "is_active": True},
            )
        self.stdout.write(self.style.SUCCESS(f"Loaded {len(SAMPLE_JOBS)} sample jobs."))
