import os, django, random
os.environ['DJANGO_SETTINGS_MODULE'] = 'student_management.settings'
django.setup()

from students.models import Class, Student
from results.models import Exam, Subject, Result
from attendance.models import Attendance
from django.utils import timezone
from datetime import date, timedelta

Attendance.objects.all().delete()
Result.objects.all().delete()
Exam.objects.all().delete()
Subject.objects.all().delete()
Student.objects.all().delete()
Class.objects.all().delete()

BRANCHES = ['TT', 'TC', 'MMFT', 'ME', 'ECE', 'CSE']
SEMESTERS = list(range(1, 9))

SUBJECTS = {
    ('TT', 1): ['Engineering Mathematics I', 'Engineering Physics', 'Engineering Chemistry', 'Textile Fibers I', 'Textile Engineering I', 'Communication Skills'],
    ('TT', 2): ['Engineering Mathematics II', 'Programming for Problem Solving', 'Fabric Manufacturing I', 'Textile Fibers II', 'Textile Engineering II', 'Environmental Science'],
    ('TT', 3): ['Mathematics III', 'Fabric Manufacturing II', 'Yarn Manufacturing I', 'Textile Chemistry I', 'Textile Mechanics', 'Basics of Textile Design'],
    ('TT', 4): ['Yarn Manufacturing II', 'Fabric Manufacturing III', 'Textile Chemistry II', 'Textile Testing I', 'Heat Transfer in Textiles', 'Industrial Management'],
    ('TT', 5): ['Textile Testing II', 'Garment Manufacturing', 'Technical Textiles I', 'Textile Costing', 'Fabric Structure & Design', 'Operations Research'],
    ('TT', 6): ['Technical Textiles II', 'Textile Waste Management', 'Apparel Production', 'Textile Marketing', 'Dyeing & Printing', 'Quality Control in Textiles'],
    ('TT', 7): ['Nonwovens', 'Textile Composites', 'Smart Textiles', 'Industrial Training', 'Major Project I', 'Textile Economics'],
    ('TT', 8): ['Textile Supply Chain', 'Nanotechnology in Textiles', 'Protective Textiles', 'Entrepreneurship', 'Major Project II', 'Seminar'],
    ('TC', 1): ['Engineering Mathematics I', 'Engineering Physics', 'Engineering Chemistry', 'Organic Chemistry I', 'Textile Fibers', 'Communication Skills'],
    ('TC', 2): ['Engineering Mathematics II', 'Programming for Problem Solving', 'Physical Chemistry', 'Organic Chemistry II', 'Analytical Chemistry', 'Environmental Science'],
    ('TC', 3): ['Mathematics III', 'Textile Chemistry I', 'Dye Chemistry', 'Polymer Chemistry', 'Color Physics', 'Chemical Engineering Principles'],
    ('TC', 4): ['Textile Chemistry II', 'Dyeing Technology I', 'Printing Technology I', 'Fabric Preparation', 'Chemistry of Textile Auxiliaries', 'Industrial Chemistry'],
    ('TC', 5): ['Dyeing Technology II', 'Printing Technology II', 'Textile Finishing', 'Water & Effluent Treatment', 'Biochemistry', 'Chemical Reaction Engineering'],
    ('TC', 6): ['Advanced Dyeing Techniques', 'Advanced Printing', 'Functional Finishes', 'Textile Testing (Chemical)', 'Environmental Chemistry', 'Process Control'],
    ('TC', 7): ['Textile Nanotechnology', 'Green Chemistry', 'Chemical Safety', 'Major Project I', 'Industrial Training', 'Research Methodology'],
    ('TC', 8): ['Biodegradable Textiles', 'Smart Coatings', 'Forensic Chemistry', 'Entrepreneurship', 'Major Project II', 'Seminar'],
    ('MMFT', 1): ['Engineering Mathematics I', 'Engineering Physics', 'Engineering Chemistry', 'Introduction to Fibers', 'Polymer Science I', 'Communication Skills'],
    ('MMFT', 2): ['Engineering Mathematics II', 'Programming for Problem Solving', 'Polymer Science II', 'Melt Spinning Technology', 'Fiber Structure & Properties', 'Environmental Science'],
    ('MMFT', 3): ['Mathematics III', 'Man-Made Fiber Production I', 'Polymer Processing', 'Fiber Physics', 'Textile Raw Materials', 'Thermodynamics of Polymers'],
    ('MMFT', 4): ['Man-Made Fiber Production II', 'Spinning Technology', 'Fiber Blending', 'Textured Yarn Technology', 'Fiber Testing', 'Polymer Characterization'],
    ('MMFT', 5): ['Specialty Fibers', 'Melt Spinning Design', 'Fiber Composites', 'Nanofibers', 'Polymer Blends', 'Quality Management'],
    ('MMFT', 6): ['High Performance Fibers', 'Bicomponent Fibers', 'Recycling of Polymers', 'Fiber Surface Modification', 'Polymer Rheology', 'Process Optimization'],
    ('MMFT', 7): ['Carbon Fibers', 'Bio-based Polymers', 'Advanced Characterization', 'Major Project I', 'Industrial Training', 'Polymer Waste Management'],
    ('MMFT', 8): ['Smart Polymeric Materials', 'Plasma Treatment', 'Additive Manufacturing', 'Entrepreneurship', 'Major Project II', 'Seminar'],
    ('ME', 1): ['Engineering Mathematics I', 'Engineering Physics', 'Engineering Chemistry', 'Basic Electrical Engineering', 'Engineering Mechanics', 'Communication Skills'],
    ('ME', 2): ['Engineering Mathematics II', 'Programming for Problem Solving', 'Engineering Drawing & Graphics', 'Environmental Science', 'Workshop Technology', 'Basic Electronics'],
    ('ME', 3): ['Strength of Materials', 'Fluid Mechanics', 'Thermodynamics', 'Manufacturing Processes', 'Engineering Materials', 'Mathematics III'],
    ('ME', 4): ['Machine Design', 'Heat Transfer', 'Theory of Machines', 'Metrology & Measurements', 'Production Technology', 'CAD/CAM'],
    ('ME', 5): ['Design of Machine Members', 'Refrigeration & Air Conditioning', 'Textile Machinery I', 'Robotics', 'Automobile Engineering', 'Industrial Engineering'],
    ('ME', 6): ['Power Plant Engineering', 'Turbomachinery', 'Textile Machinery II', 'Operations Research', 'Mechatronics', 'Computational Fluid Dynamics'],
    ('ME', 7): ['IC Engines', 'Renewable Energy Systems', 'Hydraulics & Pneumatics', 'Additive Manufacturing', 'Major Project I', 'Industrial Training'],
    ('ME', 8): ['Quality Engineering', 'Maintenance Engineering', 'Composite Materials', 'Ergonomics', 'Major Project II', 'Seminar'],
    ('ECE', 1): ['Engineering Mathematics I', 'Engineering Physics', 'Engineering Chemistry', 'Basic Electrical Engineering', 'Engineering Mechanics', 'Communication Skills'],
    ('ECE', 2): ['Engineering Mathematics II', 'Programming for Problem Solving', 'Engineering Drawing & Graphics', 'Environmental Science', 'Basic Electronics', 'Workshop Technology'],
    ('ECE', 3): ['Electronic Devices & Circuits', 'Digital System Design', 'Network Theory', 'Signals & Systems', 'Analog Electronics', 'Mathematics III'],
    ('ECE', 4): ['Microprocessors & Microcontrollers', 'Control Systems', 'Communication Systems', 'Electromagnetic Fields', 'Linear ICs', 'Probability & Statistics'],
    ('ECE', 5): ['Digital Signal Processing', 'VLSI Design', 'Antenna & Wave Propagation', 'Embedded Systems', 'Power Electronics', 'Random Variables'],
    ('ECE', 6): ['Wireless Communication', 'Optical Communication', 'Radar Systems', 'CMOS VLSI', 'IoT & Applications', 'Satellite Communication'],
    ('ECE', 7): ['Microwave Engineering', 'Speech Processing', 'Nanoelectronics', 'RF Design', 'Major Project I', 'Industrial Training'],
    ('ECE', 8): ['Adaptive Signal Processing', 'Robotics', 'Biomedical Electronics', 'Photonics', 'Major Project II', 'Seminar'],
    ('CSE', 1): ['Engineering Mathematics I', 'Engineering Physics', 'Engineering Chemistry', 'Basic Electrical Engineering', 'Engineering Mechanics', 'Communication Skills'],
    ('CSE', 2): ['Engineering Mathematics II', 'Programming for Problem Solving', 'Engineering Drawing & Graphics', 'Environmental Science', 'Basic Electronics', 'Workshop Technology'],
    ('CSE', 3): ['Discrete Mathematics', 'Data Structures & Algorithms', 'Digital Electronics & Logic Design', 'Computer Organization & Architecture', 'Object Oriented Programming', 'Environmental Science'],
    ('CSE', 4): ['Design & Analysis of Algorithms', 'Operating Systems', 'Database Management Systems', 'Computer Networks', 'Software Engineering', 'Theory of Computation'],
    ('CSE', 5): ['Machine Learning', 'Compiler Design', 'Computer Graphics', 'Web Technologies', 'Artificial Intelligence', 'Data Mining'],
    ('CSE', 6): ['Deep Learning', 'Natural Language Processing', 'Cloud Computing', 'Cybersecurity', 'Big Data Analytics', 'Blockchain'],
    ('CSE', 7): ['Image Processing', 'Distributed Systems', 'Human Computer Interaction', 'Ethical Hacking', 'Major Project I', 'Industrial Training'],
    ('CSE', 8): ['Internet of Things', 'Quantum Computing', 'Software Testing', 'Agile Methodologies', 'Major Project II', 'Seminar'],
}

LABS = {
    ('TT', 1): ['Engineering Physics Lab', 'Engineering Chemistry Lab', 'Textile Fiber Identification Lab'],
    ('TT', 2): ['Programming Lab (C)', 'Engineering Drawing Lab', 'Fabric Manufacturing Lab I'],
    ('TT', 3): ['Yarn Manufacturing Lab I', 'Fabric Manufacturing Lab II', 'Textile Chemistry Lab I'],
    ('TT', 4): ['Yarn Manufacturing Lab II', 'Textile Testing Lab I', 'Fabric Structure Lab'],
    ('TT', 5): ['Textile Testing Lab II', 'Garment Manufacturing Lab', 'Fabric Design Lab'],
    ('TT', 6): ['Dyeing & Printing Lab', 'Apparel Production Lab', 'Quality Control Lab'],
    ('TT', 7): ['Nonwovens Lab', 'Major Project I'],
    ('TT', 8): ['Major Project II'],
    ('TC', 1): ['Engineering Physics Lab', 'Engineering Chemistry Lab', 'Organic Chemistry Lab I'],
    ('TC', 2): ['Programming Lab (C)', 'Physical Chemistry Lab', 'Analytical Chemistry Lab'],
    ('TC', 3): ['Textile Chemistry Lab I', 'Dye Chemistry Lab', 'Polymer Chemistry Lab'],
    ('TC', 4): ['Dyeing Lab I', 'Printing Lab I', 'Fabric Preparation Lab'],
    ('TC', 5): ['Dyeing Lab II', 'Printing Lab II', 'Textile Finishing Lab'],
    ('TC', 6): ['Advanced Dyeing Lab', 'Water & Effluent Testing Lab', 'Chemical Testing Lab'],
    ('TC', 7): ['Nanotech Lab', 'Major Project I'],
    ('TC', 8): ['Major Project II'],
    ('MMFT', 1): ['Engineering Physics Lab', 'Engineering Chemistry Lab', 'Polymer Science Lab I'],
    ('MMFT', 2): ['Programming Lab (C)', 'Polymer Science Lab II', 'Fiber Testing Lab I'],
    ('MMFT', 3): ['Melt Spinning Lab I', 'Polymer Processing Lab', 'Fiber Physics Lab'],
    ('MMFT', 4): ['Melt Spinning Lab II', 'Textured Yarn Lab', 'Polymer Characterization Lab'],
    ('MMFT', 5): ['Specialty Fiber Lab', 'Composite Fabrication Lab', 'Quality Testing Lab'],
    ('MMFT', 6): ['High Performance Fiber Lab', 'Bicomponent Spinning Lab', 'Rheology Lab'],
    ('MMFT', 7): ['Carbon Fiber Lab', 'Major Project I'],
    ('MMFT', 8): ['Major Project II'],
    ('ME', 1): ['Engineering Physics Lab', 'Engineering Chemistry Lab', 'Workshop Lab'],
    ('ME', 2): ['Programming Lab (C)', 'Engineering Drawing Lab', 'Workshop Lab II'],
    ('ME', 3): ['Strength of Materials Lab', 'Fluid Mechanics Lab', 'Thermodynamics Lab'],
    ('ME', 4): ['Machine Design Lab', 'Heat Transfer Lab', 'CAD/CAM Lab'],
    ('ME', 5): ['Refrigeration & AC Lab', 'Robotics Lab', 'Textile Machinery Lab I'],
    ('ME', 6): ['Power Plant Lab', 'Mechatronics Lab', 'Textile Machinery Lab II'],
    ('ME', 7): ['IC Engines Lab', 'Major Project I'],
    ('ME', 8): ['Major Project II'],
    ('ECE', 1): ['Engineering Physics Lab', 'Engineering Chemistry Lab', 'Basic Electrical Lab'],
    ('ECE', 2): ['Programming Lab (C)', 'Engineering Drawing Lab', 'Basic Electronics Lab'],
    ('ECE', 3): ['Electronic Devices Lab', 'Digital System Design Lab', 'Analog Electronics Lab'],
    ('ECE', 4): ['Microprocessors Lab', 'Communication Systems Lab', 'Linear ICs Lab'],
    ('ECE', 5): ['DSP Lab', 'VLSI Design Lab', 'Embedded Systems Lab'],
    ('ECE', 6): ['Wireless Communication Lab', 'Optical Communication Lab', 'IoT Lab'],
    ('ECE', 7): ['Microwave Lab', 'Major Project I'],
    ('ECE', 8): ['Major Project II'],
    ('CSE', 1): ['Engineering Physics Lab', 'Engineering Chemistry Lab', 'Basic Electrical Lab'],
    ('CSE', 2): ['Programming Lab (C)', 'Engineering Drawing Lab', 'Workshop Lab'],
    ('CSE', 3): ['Data Structures Lab', 'Computer Organization Lab', 'Web Designing Workshop'],
    ('CSE', 4): ['Operating Systems Lab', 'Java Programming Lab', 'Cyber Security Workshop'],
    ('CSE', 5): ['DBMS Lab', 'Web Technology Lab', 'Algorithm Lab'],
    ('CSE', 6): ['Software Engineering Lab', 'Compiler Design Lab', 'Computer Networks Lab'],
    ('CSE', 7): ['Artificial Intelligence Lab', 'Major Project I'],
    ('CSE', 8): ['Major Project II'],
}

classes = {}
for branch in BRANCHES:
    for sem in SEMESTERS:
        cls = Class.objects.create(name=branch, section=f'Sem {sem}', academic_year='2025-2026')
        classes[(branch, sem)] = cls

BRANCH_PREFIX = {'TT': 'TTI', 'TC': 'TCI', 'MMFT': 'MMI', 'ME': 'MEI', 'ECE': 'ECI', 'CSE': 'CSI'}

seen_codes = set()
for (branch, sem), subjects in SUBJECTS.items():
    cls = classes[(branch, sem)]
    prefix = BRANCH_PREFIX[branch]
    for i, sub in enumerate(subjects):
        code = f'{prefix}{sem*100 + i + 1}'
        while code in seen_codes:
            code = f'{prefix}{sem*100 + i + 1}_{i}'
        seen_codes.add(code)
        Subject.objects.create(name=sub, code=code, student_class=cls,
                               semester=sem, is_lab=False, max_marks=100, pass_marks=35)
for (branch, sem), labs in LABS.items():
    cls = classes[(branch, sem)]
    prefix = BRANCH_PREFIX[branch]
    for i, lab in enumerate(labs):
        code = f'{prefix}{sem*100 + 50 + i + 1}'
        while code in seen_codes:
            code = f'{prefix}{sem*100 + 50 + i + 1}_{i}'
        seen_codes.add(code)
        Subject.objects.create(name=lab, code=code, student_class=cls,
                               semester=sem, is_lab=True, max_marks=100, pass_marks=40)

male_names = ['Aarav','Vivaan','Aditya','Vihaan','Arjun','Pranav','Dhruv','Krishna','Shaurya','Reyansh','Atharv','Aryan','Ishan','Rohan','Amit','Vikram','Rahul','Akash','Manoj','Sunil','Rajesh']
female_names = ['Anaya','Diya','Ishita','Aadhya','Riya','Sara','Aanya','Saanvi','Kavya','Neha','Priya','Pooja','Anjali','Shreya','Tanya','Divya','Meera','Asha']
last_names = ['Sharma','Verma','Patel','Singh','Kumar','Gupta','Reddy','Joshi','Nair','Das',
              'Mehta','Choudhary','Malhotra','Saxena','Rao','Desai','Agarwal','Bhatt','Mishra','Kapoor']

today = timezone.localdate()
for (branch, sem), cls in sorted(classes.items()):
    count = 15
    for i in range(count):
        ln = random.choice(last_names)
        rn = f'{branch}{sem}{i+1:03d}'
        Student.objects.create(
            roll_number=rn,
            first_name=random.choice(first_names),
            last_name=ln,
            student_class=cls,
            date_of_birth=date(2002 + sem // 2 + random.randint(0,1), random.randint(1,12), random.randint(1,28)),
            gender=random.choice(['male','female']),
            contact_number=f'+91{random.randint(7000000000, 9999999999)}',
            email=f'{rn.lower()}@uptti.ac.in',
            address=f'{random.randint(1,999)}, Hostel Block, UPTTI Campus, Kanpur',
            father_name=f'{random.choice(male_names)} {ln}',
            mother_name=f'{random.choice(female_names)} {ln}',
            guardian_contact=f'+91{random.randint(7000000000, 9999999999)}',
        )

for (branch, sem), cls in sorted(classes.items()):
    Exam.objects.create(
        name=f'Midterm {branch} Sem {sem}',
        exam_type='midterm', student_class=cls,
        start_date=today - timedelta(days=30 + sem * 5),
        end_date=today - timedelta(days=25 + sem * 5),
        is_published=True,
    )
    Exam.objects.create(
        name=f'Final {branch} Sem {sem}',
        exam_type='final', student_class=cls,
        start_date=today - timedelta(days=15 + sem * 5),
        end_date=today - timedelta(days=10 + sem * 5),
        is_published=True,
    )

result_objects = []
for s in Student.objects.all():
    branch = s.student_class.name
    current_sem = int(s.student_class.section.replace('Sem ', ''))
    for sem in range(1, current_sem + 1):
        cls_key = (branch, sem)
        if cls_key not in classes:
            continue
        sem_class = classes[cls_key]
        exams = Exam.objects.filter(student_class=sem_class)
        subjects = Subject.objects.filter(student_class=sem_class)
        for exam in exams:
            for sub in subjects:
                int_m = random.randint(20, 35) if sub.is_lab else random.randint(15, 30)
                ext_m = random.randint(35, 60) if sub.is_lab else random.randint(40, 70)
                total = min(int_m + ext_m, sub.max_marks)
                pct = total * 100.0 / sub.max_marks if sub.max_marks else 0
                if pct >= 90: gr = 'A+'
                elif pct >= 80: gr = 'A'
                elif pct >= 70: gr = 'B+'
                elif pct >= 60: gr = 'B'
                elif pct >= 50: gr = 'C+'
                elif pct >= 40: gr = 'C'
                elif pct >= 33: gr = 'D'
                else: gr = 'F'
                result_objects.append(Result(student=s, exam=exam, subject=sub,
                    internal_marks=int_m, external_marks=ext_m, marks_obtained=total))

Result.objects.bulk_create(result_objects, batch_size=500)

# Update grades via SQL (bulk_create doesn't store CharField values with choices for some DB backends)
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("""
        UPDATE results r
        JOIN subjects s ON r.subject_id = s.id
        SET r.grade = CASE 
            WHEN (r.internal_marks + r.external_marks) * 100.0 / s.max_marks >= 90 THEN 'A+'
            WHEN (r.internal_marks + r.external_marks) * 100.0 / s.max_marks >= 80 THEN 'A'
            WHEN (r.internal_marks + r.external_marks) * 100.0 / s.max_marks >= 70 THEN 'B+'
            WHEN (r.internal_marks + r.external_marks) * 100.0 / s.max_marks >= 60 THEN 'B'
            WHEN (r.internal_marks + r.external_marks) * 100.0 / s.max_marks >= 50 THEN 'C+'
            WHEN (r.internal_marks + r.external_marks) * 100.0 / s.max_marks >= 40 THEN 'C'
            WHEN (r.internal_marks + r.external_marks) * 100.0 / s.max_marks >= 33 THEN 'D'
            ELSE 'F'
        END
    """)

attendance_objects = []
all_students = list(Student.objects.all()[:200])
for stu in all_students:
    for day_offset in range(20):
        d = today - timedelta(days=day_offset)
        if d.weekday() < 6:
            status = random.choices(['present','absent','late','leave'], weights=[70,15,10,5])[0]
            attendance_objects.append(Attendance(student=stu, student_class=stu.student_class, date=d, status=status))

Attendance.objects.bulk_create(attendance_objects, batch_size=500)

total_classes = Class.objects.count()
total_students = Student.objects.count()
total_subjects = Subject.objects.count()
total_exams = Exam.objects.count()
total_results = Result.objects.count()
total_attendance = Attendance.objects.count()
print(f'Done! Created {total_classes} classes, {total_subjects} subjects, {total_students} students, {total_exams} exams, {total_results} results, {total_attendance} attendance records.')
