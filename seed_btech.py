import os, django, random
os.environ['DJANGO_SETTINGS_MODULE'] = 'student_management.settings'
django.setup()

from students.models import Class, Student
from results.models import Exam, Subject, Result
from attendance.models import Attendance
from django.utils import timezone
from datetime import date, timedelta

# Clean existing
Attendance.objects.all().delete()
Result.objects.all().delete()
Exam.objects.all().delete()
Subject.objects.all().delete()
Student.objects.all().delete()
Class.objects.all().delete()

BRANCHES = ['CSE', 'ECE', 'ME', 'CE', 'EE', 'IT']
SEMESTERS = list(range(1, 9))

SUBJECTS = {
    ('CSE', 1): ['Engineering Mathematics I', 'Engineering Physics', 'Engineering Chemistry', 'Basic Electrical Engineering', 'Engineering Mechanics', 'Communication Skills'],
    ('CSE', 2): ['Engineering Mathematics II', 'Programming for Problem Solving', 'Engineering Drawing & Graphics', 'Environmental Science', 'Basic Electronics', 'Workshop Technology'],
    ('CSE', 3): ['Discrete Mathematics', 'Data Structures & Algorithms', 'Digital Electronics & Logic Design', 'Computer Organization & Architecture', 'Object Oriented Programming', 'Environmental Science'],
    ('CSE', 4): ['Design & Analysis of Algorithms', 'Operating Systems', 'Database Management Systems', 'Computer Networks', 'Software Engineering', 'Theory of Computation'],
    ('CSE', 5): ['Machine Learning', 'Compiler Design', 'Computer Graphics', 'Web Technologies', 'Artificial Intelligence', 'Data Mining'],
    ('CSE', 6): ['Deep Learning', 'Natural Language Processing', 'Cloud Computing', 'Cybersecurity', 'Big Data Analytics', 'Blockchain'],
    ('CSE', 7): ['Image Processing', 'Distributed Systems', 'Human Computer Interaction', 'Ethical Hacking', 'Major Project I', 'Industrial Training'],
    ('CSE', 8): ['Internet of Things', 'Quantum Computing', 'Software Testing', 'Agile Methodologies', 'Major Project II', 'Seminar'],

    ('ECE', 1): ['Engineering Mathematics I', 'Engineering Physics', 'Engineering Chemistry', 'Basic Electrical Engineering', 'Engineering Mechanics', 'Communication Skills'],
    ('ECE', 2): ['Engineering Mathematics II', 'Programming for Problem Solving', 'Engineering Drawing & Graphics', 'Environmental Science', 'Basic Electronics', 'Workshop Technology'],
    ('ECE', 3): ['Electronic Devices & Circuits', 'Digital System Design', 'Network Theory', 'Signals & Systems', 'Analog Electronics', 'Mathematics III'],
    ('ECE', 4): ['Microprocessors & Microcontrollers', 'Control Systems', 'Communication Systems', 'Electromagnetic Fields', 'Linear ICs', 'Probability & Statistics'],
    ('ECE', 5): ['Digital Signal Processing', 'VLSI Design', 'Antenna & Wave Propagation', 'Embedded Systems', 'Power Electronics', 'Random Variables'],
    ('ECE', 6): ['Wireless Communication', 'Optical Communication', 'Radar Systems', 'CMOS VLSI', 'IoT & Applications', 'Satellite Communication'],
    ('ECE', 7): ['Microwave Engineering', 'Speech Processing', 'Nanoelectronics', 'RF Design', 'Major Project I', 'Industrial Training'],
    ('ECE', 8): ['Adaptive Signal Processing', 'Robotics', 'Biomedical Electronics', 'Photonics', 'Major Project II', 'Seminar'],

    ('ME', 1): ['Engineering Mathematics I', 'Engineering Physics', 'Engineering Chemistry', 'Basic Electrical Engineering', 'Engineering Mechanics', 'Communication Skills'],
    ('ME', 2): ['Engineering Mathematics II', 'Programming for Problem Solving', 'Engineering Drawing & Graphics', 'Environmental Science', 'Basic Electronics', 'Workshop Technology'],
    ('ME', 3): ['Strength of Materials', 'Fluid Mechanics', 'Thermodynamics', 'Manufacturing Processes', 'Engineering Materials', 'Mathematics III'],
    ('ME', 4): ['Machine Design', 'Heat Transfer', 'Theory of Machines', 'Metrology & Measurements', 'Production Technology', 'CAD/CAM'],
    ('ME', 5): ['Design of Machine Members', 'Refrigeration & Air Conditioning', 'Finite Element Methods', 'Robotics', 'Automobile Engineering', 'Industrial Engineering'],
    ('ME', 6): ['Power Plant Engineering', 'Turbomachinery', 'Mechanical Vibrations', 'Operations Research', 'Mechatronics', 'Computational Fluid Dynamics'],
    ('ME', 7): ['IC Engines', 'Renewable Energy Systems', 'Hydraulics & Pneumatics', 'Additive Manufacturing', 'Major Project I', 'Industrial Training'],
    ('ME', 8): ['Quality Engineering', 'Maintenance Engineering', 'Composite Materials', 'Ergonomics', 'Major Project II', 'Seminar'],

    ('CE', 1): ['Engineering Mathematics I', 'Engineering Physics', 'Engineering Chemistry', 'Basic Electrical Engineering', 'Engineering Mechanics', 'Communication Skills'],
    ('CE', 2): ['Engineering Mathematics II', 'Programming for Problem Solving', 'Engineering Drawing & Graphics', 'Environmental Science', 'Basic Electronics', 'Workshop Technology'],
    ('CE', 3): ['Strength of Materials', 'Fluid Mechanics', 'Building Materials', 'Surveying', 'Engineering Geology', 'Mathematics III'],
    ('CE', 4): ['Structural Analysis', 'Geotechnical Engineering', 'Transportation Engineering', 'Environmental Engineering', 'Concrete Technology', 'Hydraulics'],
    ('CE', 5): ['Design of Steel Structures', 'Foundation Engineering', 'Highway Engineering', 'Water Resources Engineering', 'Estimating & Costing', 'Construction Management'],
    ('CE', 6): ['Design of RCC Structures', 'Bridge Engineering', 'Waste Water Engineering', 'Irrigation Engineering', 'Remote Sensing', 'Earthquake Engineering'],
    ('CE', 7): ['Advanced Structural Design', 'Prestressed Concrete', 'Prefabricated Structures', 'Traffic Engineering', 'Major Project I', 'Industrial Training'],
    ('CE', 8): ['Smart Materials', 'Green Buildings', 'Harbor & Coastal Engineering', 'Construction Safety', 'Major Project II', 'Seminar'],

    ('EE', 1): ['Engineering Mathematics I', 'Engineering Physics', 'Engineering Chemistry', 'Basic Electrical Engineering', 'Engineering Mechanics', 'Communication Skills'],
    ('EE', 2): ['Engineering Mathematics II', 'Programming for Problem Solving', 'Engineering Drawing & Graphics', 'Environmental Science', 'Basic Electronics', 'Workshop Technology'],
    ('EE', 3): ['Network Theory', 'Electrical Machines I', 'Electromagnetic Theory', 'Analog Electronics', 'Mathematics III', 'Digital Electronics'],
    ('EE', 4): ['Electrical Machines II', 'Power Systems I', 'Control Systems', 'Measurements & Instruments', 'Digital Signal Processing', 'Power Electronics'],
    ('EE', 5): ['Power Systems II', 'Protection & Switchgear', 'Microcontrollers', 'Renewable Energy Systems', 'Electrical Drives', 'High Voltage Engineering'],
    ('EE', 6): ['Smart Grid', 'Power Quality', 'FACTS', 'Electrical Machine Design', 'Energy Management', 'Industrial Automation (PLC/SCADA)'],
    ('EE', 7): ['HVDC Transmission', 'Electric Vehicles', 'Power System Modeling', 'Restructured Power Systems', 'Major Project I', 'Industrial Training'],
    ('EE', 8): ['Power System Dynamics', 'Advanced Control Systems', 'Distribution Automation', 'Energy Audit', 'Major Project II', 'Seminar'],

    ('IT', 1): ['Engineering Mathematics I', 'Engineering Physics', 'Engineering Chemistry', 'Basic Electrical Engineering', 'Engineering Mechanics', 'Communication Skills'],
    ('IT', 2): ['Engineering Mathematics II', 'Programming for Problem Solving', 'Engineering Drawing & Graphics', 'Environmental Science', 'Basic Electronics', 'Workshop Technology'],
    ('IT', 3): ['Discrete Mathematics', 'Data Structures', 'Digital Logic', 'Computer Organization', 'Object Oriented Programming', 'Environmental Science'],
    ('IT', 4): ['Operating Systems', 'Database Management Systems', 'Computer Networks', 'Web Technologies', 'Software Engineering', 'Design & Analysis of Algorithms'],
    ('IT', 5): ['Java Programming', 'Data Mining', 'Cloud Computing', 'Information Security', 'Mobile Computing', 'Artificial Intelligence'],
    ('IT', 6): ['Big Data Analytics', 'Machine Learning', 'Cyber Forensics', 'Blockchain', 'Internet of Things', 'DevOps'],
    ('IT', 7): ['Data Science', 'Business Intelligence', 'Robotic Process Automation', 'Augmented Reality', 'Major Project I', 'Industrial Training'],
    ('IT', 8): ['Quantum Computing', 'Edge Computing', 'Computer Vision', 'Microservices Architecture', 'Major Project II', 'Seminar'],
}

classes = {}
for branch in BRANCHES:
    for sem in SEMESTERS:
        cls = Class.objects.create(name=branch, section=f'Sem {sem}', academic_year='2025-2026')
        classes[(branch, sem)] = cls

LABS = {
    # CSE labs as per AKTU curriculum
    ('CSE', 1): ['Engineering Physics Lab', 'Engineering Chemistry Lab', 'Basic Electrical Engineering Lab'],
    ('CSE', 2): ['Programming Lab (C)', 'Engineering Drawing & Graphics Lab', 'Workshop Lab'],
    ('CSE', 3): ['Data Structures Lab', 'Computer Organization Lab', 'Web Designing Workshop'],
    ('CSE', 4): ['Operating Systems Lab', 'Java Programming Lab', 'Cyber Security Workshop'],
    ('CSE', 5): ['Database Management System Lab', 'Web Technology Lab', 'Design & Analysis of Algorithm Lab'],
    ('CSE', 6): ['Software Engineering Lab', 'Compiler Design Lab', 'Computer Networks Lab'],
    ('CSE', 7): ['Artificial Intelligence Lab', 'Major Project I'],
    ('CSE', 8): ['Major Project II'],

    # ECE labs as per AKTU curriculum
    ('ECE', 1): ['Engineering Physics Lab', 'Engineering Chemistry Lab', 'Basic Electrical Engineering Lab'],
    ('ECE', 2): ['Programming Lab (C)', 'Engineering Drawing & Graphics Lab', 'Workshop Lab'],
    ('ECE', 3): ['Electronic Devices Lab', 'Digital System Design Lab', 'Analog Electronics Lab'],
    ('ECE', 4): ['Microprocessors Lab', 'Communication Systems Lab', 'Linear Integrated Circuits Lab'],
    ('ECE', 5): ['Digital Signal Processing Lab', 'VLSI Design Lab', 'Embedded Systems Lab'],
    ('ECE', 6): ['Wireless Communication Lab', 'Optical Communication Lab', 'IoT Lab'],
    ('ECE', 7): ['Microwave Engineering Lab', 'Major Project I'],
    ('ECE', 8): ['Major Project II'],

    # ME labs as per AKTU curriculum
    ('ME', 1): ['Engineering Physics Lab', 'Engineering Chemistry Lab', 'Workshop Lab'],
    ('ME', 2): ['Programming Lab (C)', 'Engineering Drawing & Graphics Lab', 'Workshop Lab'],
    ('ME', 3): ['Strength of Materials Lab', 'Fluid Mechanics Lab', 'Thermodynamics Lab'],
    ('ME', 4): ['Machine Design Lab', 'Heat Transfer Lab', 'CAD/CAM Lab'],
    ('ME', 5): ['Refrigeration & Air Conditioning Lab', 'Robotics Lab', 'Automobile Engineering Lab'],
    ('ME', 6): ['Power Plant Engineering Lab', 'Mechatronics Lab', 'Computational Fluid Dynamics Lab'],
    ('ME', 7): ['IC Engines Lab', 'Major Project I'],
    ('ME', 8): ['Major Project II'],

    # CE labs as per AKTU curriculum
    ('CE', 1): ['Engineering Physics Lab', 'Engineering Chemistry Lab', 'Workshop Lab'],
    ('CE', 2): ['Programming Lab (C)', 'Engineering Drawing & Graphics Lab', 'Workshop Lab'],
    ('CE', 3): ['Strength of Materials Lab', 'Fluid Mechanics Lab', 'Surveying Lab'],
    ('CE', 4): ['Structural Analysis Lab', 'Geotechnical Engineering Lab', 'Concrete Technology Lab'],
    ('CE', 5): ['Highway Engineering Lab', 'Water Resources Engineering Lab', 'Foundation Engineering Lab'],
    ('CE', 6): ['RCC Design Lab', 'Waste Water Engineering Lab', 'Remote Sensing Lab'],
    ('CE', 7): ['Advanced Structural Design Lab', 'Major Project I'],
    ('CE', 8): ['Major Project II'],

    # EE labs as per AKTU curriculum
    ('EE', 1): ['Engineering Physics Lab', 'Engineering Chemistry Lab', 'Basic Electrical Engineering Lab'],
    ('EE', 2): ['Programming Lab (C)', 'Engineering Drawing & Graphics Lab', 'Workshop Lab'],
    ('EE', 3): ['Network Theory Lab', 'Electrical Machines Lab I', 'Analog Electronics Lab'],
    ('EE', 4): ['Electrical Machines Lab II', 'Power Systems Lab', 'Measurements & Instruments Lab'],
    ('EE', 5): ['Microcontrollers Lab', 'Power Electronics Lab', 'Electrical Drives Lab'],
    ('EE', 6): ['Smart Grid Lab', 'PLC/SCADA Lab', 'Electrical Machine Design Lab'],
    ('EE', 7): ['Electric Vehicles Lab', 'Major Project I'],
    ('EE', 8): ['Major Project II'],

    # IT labs as per AKTU curriculum
    ('IT', 1): ['Engineering Physics Lab', 'Engineering Chemistry Lab', 'Basic Electrical Engineering Lab'],
    ('IT', 2): ['Programming Lab (C)', 'Engineering Drawing & Graphics Lab', 'Workshop Lab'],
    ('IT', 3): ['Data Structures Lab', 'Digital Logic Lab', 'Object Oriented Programming Lab'],
    ('IT', 4): ['Operating Systems Lab', 'Database Management Systems Lab', 'Computer Networks Lab', 'Web Technologies Lab'],
    ('IT', 5): ['Java Programming Lab', 'Data Mining Lab', 'Cloud Computing Lab'],
    ('IT', 6): ['Big Data Analytics Lab', 'Machine Learning Lab', 'IoT Lab'],
    ('IT', 7): ['Data Science Lab', 'Major Project I'],
    ('IT', 8): ['Major Project II'],
}

BRANCH_PREFIX = {'CSE': 'BCS', 'ECE': 'BEC', 'ME': 'BME', 'CE': 'BCE', 'EE': 'BEE', 'IT': 'BIT'}

seen_codes = set()
for (branch, sem), subjects in SUBJECTS.items():
    cls = classes[(branch, sem)]
    prefix = BRANCH_PREFIX[branch]
    for i, sub in enumerate(subjects):
        if sem <= 2:
            code = f'{prefix}{sem}{i+1:02d}'
        else:
            code = f'{prefix}{sem*100 + i + 1}'
        while code in seen_codes:
            code = f'{prefix}{sem*100 + i + 1}_{i}'
        seen_codes.add(code)
        Subject.objects.create(name=sub, code=code, student_class=cls,
                               semester=sem, is_lab=False,
                               max_marks=100, pass_marks=35)
for (branch, sem), labs in LABS.items():
    cls = classes[(branch, sem)]
    prefix = BRANCH_PREFIX[branch]
    for i, lab in enumerate(labs):
        code = f'{prefix}{sem*100 + 50 + i + 1}'
        while code in seen_codes:
            code = f'{prefix}{sem*100 + 50 + i + 1}_{i}'
        seen_codes.add(code)
        Subject.objects.create(name=lab, code=code, student_class=cls,
                               semester=sem, is_lab=True,
                               max_marks=100, pass_marks=40)

male_names = ['Aarav','Vivaan','Aditya','Vihaan','Arjun','Pranav','Dhruv','Krishna','Shaurya','Reyansh','Atharv','Aryan','Ishan','Rohan','Amit','Vikram','Rahul','Akash','Manoj','Sunil','Rajesh']
female_names = ['Anaya','Diya','Ishita','Aadhya','Riya','Sara','Aanya','Saanvi','Kavya','Neha','Priya','Pooja','Anjali','Shreya','Tanya','Divya','Meera','Asha']
last_names = ['Sharma','Verma','Patel','Singh','Kumar','Gupta','Reddy','Joshi','Nair','Das',
              'Mehta','Choudhary','Malhotra','Saxena','Rao','Desai','Agarwal','Bhatt','Mishra','Kapoor']

today = timezone.localdate()
students = []
roll = 1
for (branch, sem), cls in sorted(classes.items()):
    count = 20
    for i in range(count):
        ln = random.choice(last_names)
        s = Student.objects.create(
            roll_number=f'{branch}{sem}{roll:03d}',
            first_name=random.choice(first_names),
            last_name=ln,
            student_class=cls,
            date_of_birth=date(2002 + sem // 2 + random.randint(0,1), random.randint(1,12), random.randint(1,28)),
            gender=random.choice(['male','female']),
            contact_number=f'+91{random.randint(7000000000, 9999999999)}',
            email=f'student{roll}@btech.edu',
            address=f'{random.randint(1,999)}, Hostel Block, Campus',
            father_name=f'{random.choice(male_names)} {ln}',
            mother_name=f'{random.choice(female_names)} {ln}',
            guardian_contact=f'+91{random.randint(7000000000, 9999999999)}',
        )
        students.append(s)
        roll += 1

for (branch, sem), cls in sorted(classes.items()):
    Exam.objects.create(
        name=f'Midterm {branch} Sem {sem}',
        exam_type='midterm',
        student_class=cls,
        start_date=today - timedelta(days=30 + sem * 5),
        end_date=today - timedelta(days=25 + sem * 5),
        is_published=True,
    )

for s in Student.objects.all():
    branch = s.student_class.name
    current_sem = int(s.student_class.section.replace('Sem ', ''))
    for sem in range(1, current_sem + 1):
        cls_key = (branch, sem)
        if cls_key not in classes:
            continue
        exam = Exam.objects.get(student_class=classes[cls_key])
        subjects = Subject.objects.filter(student_class=classes[cls_key])
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
                marks_obtained=total
            )

for stu in Student.objects.all()[:500]:
    for day_offset in range(30):
        d = today - timedelta(days=day_offset)
        if d.weekday() < 6:
            status = random.choices(['present','absent','late','leave'], weights=[70,15,10,5])[0]
            Attendance.objects.create(student=stu, student_class=stu.student_class, date=d, status=status)

total_classes = Class.objects.count()
total_students = Student.objects.count()
total_subjects = Subject.objects.count()
total_exams = Exam.objects.count()
total_results = Result.objects.count()
total_attendance = Attendance.objects.count()
print(f'Done! Created {total_classes} classes, {total_subjects} subjects, {total_students} students, {total_exams} exams, {total_results} results, {total_attendance} attendance records.')



