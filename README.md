# Student Management System

A full-stack Student Management System built with **Django 6**, **MySQL/SQLite**, and **Bootstrap 5**.

## Features

### Student Records (CRUD)
- Add new student with photo, guardian details, admission date
- Searchable, sortable, paginated student list (filter by class/section/gender)
- Individual profile page with attendance & result history
- Edit & soft-delete students (recoverable from admin)

### Attendance Tracking
- Mark daily attendance per class (Present/Absent/Late/Leave)
- Bulk attendance checkbox UI for entire class at once
- View attendance history filtered by student/class/month
- Monthly attendance percentage summary with progress bars

### Result Management
- Manage subjects per class with configurable max/pass marks
- Enter marks per student per subject per exam
- Auto-calculate percentage, grade (A+ to F), pass/fail status
- Class-wise result summary with ranking
- Printable report card per student

### Authentication & Roles
- Custom User model with roles: Admin, Teacher, Student, Parent
- Login/Register with role-based access
- Django admin panel for full data management

### Dashboard
- Total students, today's attendance %, quick action links

## Tech Stack

- **Backend:** Django 6, Python 3
- **Database:** MySQL (production) / SQLite (development)
- **Frontend:** Bootstrap 5, jQuery, HTML5, CSS3
- **Static Files:** Whitenoise
- **Libraries:** django-crispy-forms, reportlab, openpyxl, pillow

## Setup Instructions

### 1. Clone & Create Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Database

**Option A: SQLite (Default - Quick Start)**
- No configuration needed. The project uses SQLite by default.

**Option B: MySQL (Production)**
1. Create a MySQL database:
   ```sql
   CREATE DATABASE student_management CHARACTER SET utf8mb4;
   ```
2. Copy `.env.example` to `.env` and update credentials:
   ```
   DJANGO_DB_ENGINE=mysql
   DB_NAME=student_management
   DB_USER=root
   DB_PASSWORD=your-password
   DB_HOST=localhost
   DB_PORT=3306
   ```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. (Optional) Seed Sample Data

```bash
python manage.py seed_data
```

### 7. Run Development Server

```bash
python manage.py runserver
```

### 8. Access the Application

- **App:** http://127.0.0.1:8000/
- **Admin:** http://127.0.0.1:8000/admin/
- **Login:** Use the superuser credentials or register a new account

## Default Credentials (After Seed)

| Username  | Password    | Role    |
|-----------|-------------|---------|
| admin     | admin123    | Admin   |
| teacher   | teacher123  | Teacher |
| teacher2  | teacher123  | Teacher |

## Project Structure

```
student_management/
├── accounts/           # Custom User model, authentication
│   ├── models.py       # User with role field
│   ├── views.py        # Login, Register, Dashboard
│   └── management/commands/seed_data.py
├── students/           # Student & Class management
│   ├── models.py       # Student (soft-delete), Class
│   ├── views.py        # CRUD + list/detail + API
│   └── templates/students/
├── attendance/         # Attendance tracking
│   ├── models.py       # Attendance records
│   ├── views.py        # Mark, history, summary
│   └── templates/attendance/
├── results/            # Exam & Result management
│   ├── models.py       # Subject, Exam, Result
│   ├── views.py        # Manage, class summary, report card
│   └── templates/results/
├── templates/          # Base templates
├── static/             # CSS, JS
└── student_management/ # Project settings, URLs
```

## Deployment (Render/Heroku)

1. Set `DJANGO_DB_ENGINE=mysql` and DB credentials in environment variables
2. Add `web: gunicorn student_management.wsgi` to `Procfile`
3. Ensure `ALLOWED_HOSTS` includes your domain
4. Whitenoise handles static files automatically

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/attendance/api/get-students/<class_id>/` | Get students for attendance |
| `/attendance/api/save/` | Save attendance (POST) |
| `/results/api/get-data/` | Get subjects/exams for class |
| `/results/api/save/` | Save results (POST) |
| `/students/api/students/?class=<id>` | Get students for results |
