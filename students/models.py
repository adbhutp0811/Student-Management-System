from django.db import models
from django.core.validators import RegexValidator


class Class(models.Model):
    name = models.CharField(max_length=20)
    section = models.CharField(max_length=10, default='A')
    academic_year = models.CharField(max_length=9, default='2025-2026')

    class Meta:
        db_table = 'classes'
        ordering = ['name', 'section']
        unique_together = ('name', 'section')

    def __str__(self):
        return f'{self.name} - {self.section}'


class Student(models.Model):
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')]

    roll_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_class = models.ForeignKey(Class, on_delete=models.PROTECT, related_name='students')
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    contact_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')]
    )
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    father_name = models.CharField(max_length=200)
    mother_name = models.CharField(max_length=200, default='')
    guardian_contact = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')]
    )
    admission_date = models.DateField(auto_now_add=True)
    profile_photo = models.ImageField(upload_to='student_photos/', blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'students'
        ordering = ['roll_number']

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.roll_number})'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
