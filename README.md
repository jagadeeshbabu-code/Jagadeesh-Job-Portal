# Jagadeesh Job Portal

A full-stack recruitment portal starter with a Django REST API and React UI.

## Features

- Browse and filter jobs by keyword, location, and category
- Employer job posting and applicant tracking
- Candidate registration, login, profile, and resume upload
- Apply to jobs and view application status
- Admin dashboard for managing jobs and applications

## Run locally

### API

1. Create a MySQL database (or run `docker compose up -d db`).
2. In `backend/`, copy `.env.example` to `.env` and set database credentials.
3. Create a virtual environment, install `requirements.txt`, then run:

```sh
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_jobs
python manage.py runserver
```

API runs at `http://localhost:8000`; admin at `/admin/`.

### Web

```sh
cd frontend
npm install
npm run dev
```

The Vite dev server runs at `http://localhost:5173` and proxies `/api` to Django.
For a quick UI preview without the API, the app includes demo job data; account and
application actions require the API.

## Roles

Register as a candidate by default. An administrator can grant employer access
through Django admin. Employers can create, edit, and close their own job listings.
The `seed_jobs` command adds fictional sample listings owned by the administrator
so a new local install has jobs to browse and apply to.

## Production notes

Set a strong `DJANGO_SECRET_KEY`, `DEBUG=False`, and `ALLOWED_HOSTS`; use HTTPS,
private object storage for resumes, and configure email delivery before deployment.
