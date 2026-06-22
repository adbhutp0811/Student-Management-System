from django.db import models
from students.models import Student


class Hostel(models.Model):
    name = models.CharField(max_length=100)
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female'), ('coed', 'Co-Ed')]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='coed')
    warden = models.CharField(max_length=200, blank=True)
    contact = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    total_rooms = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=20)
    capacity = models.PositiveIntegerField(default=2)
    occupied = models.PositiveIntegerField(default=0)
    rent_per_month = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        unique_together = ('hostel', 'room_number')

    def __str__(self):
        return f'{self.hostel.name} - Room {self.room_number}'

    @property
    def is_available(self):
        return self.occupied < self.capacity


class RoomAllocation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='hostel_allocations')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='allocations')
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.student.roll_number} -> {self.room}'
