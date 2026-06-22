import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()
from django.db import connection

GENDER_MAP = {
    'Aadhya': 'female', 'Aanya': 'female', 'Aarav': 'male', 'Aditya': 'male',
    'Akash': 'male', 'Amit': 'male', 'Anaya': 'female', 'Anjali': 'female',
    'Arjun': 'male', 'Aryan': 'male', 'Asha': 'female', 'Atharv': 'male',
    'Dhruv': 'male', 'Divya': 'female', 'Diya': 'female', 'Ishan': 'male',
    'Ishita': 'female', 'Kavya': 'female', 'Krishna': 'male', 'Manoj': 'male',
    'Meera': 'female', 'Neha': 'female', 'Pooja': 'female', 'Pranav': 'male',
    'Priya': 'female', 'Rahul': 'male', 'Rajesh': 'male', 'Reyansh': 'male',
    'Riya': 'female', 'Rohan': 'male', 'Saanvi': 'female', 'Sai': 'male',
    'Sara': 'female', 'Shaurya': 'male', 'Shreya': 'female', 'Sunil': 'male',
    'Tanya': 'female', 'Vihaan': 'male', 'Vikram': 'male', 'Vivaan': 'male',
}

with connection.cursor() as c:
    for name, gender in GENDER_MAP.items():
        c.execute("UPDATE students SET gender = %s WHERE first_name = %s", [gender, name])
    print(f'Updated {c.rowcount} rows for {name}')

with connection.cursor() as c:
    c.execute("SELECT gender, COUNT(*) FROM students GROUP BY gender")
    for row in c.fetchall():
        print(f'{row[0]}: {row[1]}')
