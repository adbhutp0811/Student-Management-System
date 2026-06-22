from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        TEACHER = 'teacher', 'Teacher'
        STUDENT = 'student', 'Student'
        PARENT = 'parent', 'Parent'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.TEACHER)
    phone = models.CharField(max_length=15, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f'{self.get_full_name()} ({self.get_role_display()})'
