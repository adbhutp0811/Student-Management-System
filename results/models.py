from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from students.models import Class, Student


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='subjects')
    is_language = models.BooleanField(default=False)
    max_marks = models.IntegerField(default=100)
    pass_marks = models.IntegerField(default=33)

    class Meta:
        db_table = 'subjects'
        unique_together = ('code', 'student_class')
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.student_class})'


class Exam(models.Model):
    EXAM_TYPES = [
        ('unit_test', 'Unit Test'),
        ('midterm', 'Midterm'),
        ('final', 'Final'),
        ('practical', 'Practical'),
    ]

    name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='exams')
    start_date = models.DateField()
    end_date = models.DateField()
    academic_year = models.CharField(max_length=9, default='2025-2026')
    is_published = models.BooleanField(default=False)

    class Meta:
        db_table = 'exams'
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.name} ({self.student_class})'


GRADE_CHOICES = [
    ('A+', 'A+'), ('A', 'A'), ('B+', 'B+'), ('B', 'B'),
    ('C+', 'C+'), ('C', 'C'), ('D', 'D'), ('F', 'F'),
]


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='results')
    marks_obtained = models.FloatField(
        validators=[MinValueValidator(0)]
    )
    grade = models.CharField(max_length=2, blank=True, choices=GRADE_CHOICES)
    grade_auto = models.BooleanField(default=True, help_text='Auto-calculate grade from marks')
    remarks = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'results'
        unique_together = ('student', 'exam', 'subject')
        ordering = ['subject__name']

    def __str__(self):
        return f'{self.student} - {self.subject} - {self.marks_obtained}'

    def save(self, *args, **kwargs):
        if self.grade_auto or not self.grade:
            self.grade = self.calculate_grade()
        super().save(*args, **kwargs)

    def calculate_grade(self):
        pct = (self.marks_obtained / self.subject.max_marks) * 100 if self.subject.max_marks else 0
        if pct >= 90:
            return 'A+'
        if pct >= 80:
            return 'A'
        if pct >= 70:
            return 'B+'
        if pct >= 60:
            return 'B'
        if pct >= 50:
            return 'C+'
        if pct >= 40:
            return 'C'
        if pct >= 33:
            return 'D'
        return 'F'

    @property
    def percentage(self):
        if self.subject.max_marks:
            return round((self.marks_obtained / self.subject.max_marks) * 100, 2)
        return 0

    @property
    def is_pass(self):
        return self.marks_obtained >= self.subject.pass_marks
