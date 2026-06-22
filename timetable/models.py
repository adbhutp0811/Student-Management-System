from django.db import models
from students.models import Class
from results.models import Subject


class TimeSlot(models.Model):
    DAY_CHOICES = [
        ('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday'),
    ]
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='time_slots')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='time_slots')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['day', 'start_time']

    def __str__(self):
        return f'{self.student_class} - {self.subject.name} ({self.get_day_display()})'
