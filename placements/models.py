from django.db import models
from students.models import Student


class Company(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='placements/', blank=True)
    avg_package = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class PlacementDrive(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='drives')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    application_deadline = models.DateField()
    drive_date = models.DateField()
    eligibility_criteria = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-drive_date']

    def __str__(self):
        return f'{self.company.name} - {self.title}'


class PlacementApplication(models.Model):
    STATUS_CHOICES = [('applied', 'Applied'), ('shortlisted', 'Shortlisted'), ('selected', 'Selected'), ('rejected', 'Rejected')]
    drive = models.ForeignKey(PlacementDrive, on_delete=models.CASCADE, related_name='applications')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='placement_applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('drive', 'student')

    def __str__(self):
        return f'{self.student.roll_number} - {self.drive.company.name}'
