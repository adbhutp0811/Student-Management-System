from django.core.management.base import BaseCommand
from students.models import Student


NAME_GENDER_MAP = {
    # Male names
    'Aarav': 'male', 'Abhinav': 'male', 'ABHINAV': 'male', 'Abhishek': 'male',
    'ABHISHEK': 'male', 'Adbhut': 'male', 'ADBHUT': 'male', 'Aditya': 'male',
    'Akash': 'male', 'Akshat': 'male', 'AKSHAT': 'male', 'Alankrit': 'male',
    'ALANKRIT': 'male', 'Aman': 'male', 'AMAN': 'male', 'Amit': 'male',
    'Anuj': 'male', 'ANUJ': 'male', 'Anurag': 'male', 'ANURAG': 'male',
    'Arjun': 'male', 'Arpit': 'male', 'ARPIT': 'male', 'Aryan': 'male',
    'Ashish': 'male', 'ASHISH': 'male', 'Ashu': 'male', 'Atharv': 'male',
    'Avinash': 'male', 'AVINASH': 'male', 'Ayush': 'male', 'Dhruv': 'male',
    'Ishan': 'male', 'Manoj': 'male', 'Krishna': 'male', 'Pranav': 'male',
    'Rahul': 'male', 'Rajesh': 'male', 'Reyansh': 'male', 'Rohan': 'male',
    'Sai': 'male', 'Shaurya': 'male', 'Sunil': 'male', 'Vihaan': 'male',
    'Vikram': 'male', 'Vivaan': 'male',
    # Female names
    'Aadhya': 'female', 'Aanya': 'female', 'Anaya': 'female', 'Anjali': 'female',
    'Anshika': 'female', 'Asha': 'female', 'Divya': 'female', 'Diya': 'female',
    'Ishita': 'female', 'Kavya': 'female', 'Meera': 'female', 'Miracle': 'female',
    'Neha': 'female', 'Pooja': 'female', 'Priya': 'female', 'Riya': 'female',
    'Saanvi': 'female', 'Sara': 'female', 'Shreya': 'female', 'Tanya': 'female',
}


def infer_gender_from_name(first_name):
    name = first_name.strip()
    if not name:
        return None
    direct = NAME_GENDER_MAP.get(name)
    if direct:
        return direct
    title_name = name.title()
    direct = NAME_GENDER_MAP.get(title_name)
    if direct:
        return direct
    lower = name.lower()
    if lower.endswith(('a', 'i', 'e', 'y')):
        return 'female'
    return 'male'


class Command(BaseCommand):
    help = 'Infer and update student gender based on first name'

    def handle(self, *args, **options):
        students = Student.objects.all()
        updated = 0
        skipped = 0
        for s in students:
            inferred = infer_gender_from_name(s.first_name)
            if inferred and s.gender != inferred:
                old = s.gender
                s.gender = inferred
                s.save(update_fields=['gender'])
                self.stdout.write(f"  {s.first_name} {s.last_name}: {old} -> {inferred}")
                updated += 1
            else:
                skipped += 1
        self.stdout.write(self.style.SUCCESS(
            f"Done. Updated: {updated}, Skipped (already correct/unknown): {skipped}"
        ))
