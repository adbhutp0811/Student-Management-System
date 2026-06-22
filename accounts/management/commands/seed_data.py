from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import User
from students.models import Class, Student
from attendance.models import Attendance
from results.models import Exam, Subject, Result
import random
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        if User.objects.filter(username='teacher').exists():
            self.stdout.write('Data already seeded, skipping.')
            return

        User.objects.create_user('teacher', 'teacher@school.com', 'teacher123', role='teacher', first_name='John', last_name='Doe')
        User.objects.create_user('teacher2', 'teacher2@school.com', 'teacher123', role='teacher', first_name='Jane', last_name='Smith')

        classes = []
        for cls_name in ['1', '2', '3', '4', '5']:
            for section in ['A', 'B']:
                c = Class.objects.create(name=cls_name, section=section, academic_year='2025-2026')
                classes.append(c)

        male_names = ['Aarav', 'Vivaan', 'Aditya', 'Vihaan', 'Arjun', 'Pranav', 'Dhruv', 'Krishna', 'Shaurya', 'Reyansh', 'Atharv']
        female_names = ['Anaya', 'Diya', 'Ishita', 'Aadhya', 'Riya', 'Sara', 'Aanya', 'Saanvi', 'Priya', 'Neha']
        last_names = ['Sharma', 'Verma', 'Patel', 'Singh', 'Kumar', 'Gupta', 'Reddy', 'Joshi', 'Nair', 'Das']

        students = []
        roll = 1
        for cls in classes:
            for i in range(8):
                gender = random.choice(['male', 'female'])
                ln = random.choice(last_names)
                s = Student.objects.create(
                    roll_number=f'{cls.name}{cls.section}{roll:03d}',
                    first_name=random.choice(first_names),
                    last_name=ln,
                    student_class=cls,
                    date_of_birth=date(2010 + random.randint(0, 8), random.randint(1, 12), random.randint(1, 28)),
                    gender=gender,
                    contact_number=f'+91{random.randint(7000000000, 9999999999)}',
                    email=f'student{roll}@school.com',
                    address=f'{random.randint(1, 999)}, Main Street, City',
                    father_name=f'{random.choice(male_names)} {ln}',
                    mother_name=f'{random.choice(female_names)} {ln}',
                    guardian_contact=f'+91{random.randint(7000000000, 9999999999)}',
                )
                students.append(s)
                roll += 1

        for cls in classes:
            sem = int(cls.name) if cls.name.isdigit() else 1
            for sub in ['Mathematics', 'English', 'Hindi', 'Science', 'Social Studies']:
                Subject.objects.create(
                    name=sub,
                    code=f'{sub[:3].upper()}-{cls.name}{cls.section}',
                    student_class=cls,
                    semester=sem,
                    is_lab=False,
                    max_marks=100,
                    pass_marks=33,
                )
            for lab in ['Science Lab', 'Computer Lab']:
                Subject.objects.create(
                    name=lab,
                    code=f'LAB{lab[:3].upper()}-{cls.name}{cls.section}',
                    student_class=cls,
                    semester=sem,
                    is_lab=True,
                    max_marks=100,
                    pass_marks=40,
                )

        today = timezone.localdate()
        for s in students[:60]:
            for day_offset in range(30):
                d = today - timedelta(days=day_offset)
                if d.weekday() < 6:
                    status = random.choices(['present', 'absent', 'late', 'leave'], weights=[70, 15, 10, 5])[0]
                    Attendance.objects.create(
                        student=s,
                        student_class=s.student_class,
                        date=d,
                        status=status,
                    )

        for cls in classes:
            exam = Exam.objects.create(
                name=f'Midterm {cls.name}',
                exam_type='midterm',
                student_class=cls,
                start_date=today - timedelta(days=60),
                end_date=today - timedelta(days=55),
                is_published=True,
            )
            subjects = Subject.objects.filter(student_class=cls)
            class_students = Student.objects.filter(student_class=cls, is_deleted=False)
            for s in class_students:
                for sub in subjects:
                    if sub.is_lab:
                        int_marks = random.randint(30, 50)
                        ext_marks = random.randint(30, 50)
                    else:
                        int_marks = random.randint(15, 30)
                        ext_marks = random.randint(40, 70)
                    total = min(int_marks + ext_marks, sub.max_marks)
                    Result.objects.create(
                        student=s, exam=exam, subject=sub,
                        internal_marks=int_marks, external_marks=ext_marks,
                        marks_obtained=total,
                    )

        self.stdout.write(self.style.SUCCESS(f'Created {len(classes)} classes, {len(students)} students, subjects, attendance, and results!'))


