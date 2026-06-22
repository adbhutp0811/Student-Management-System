from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


class Club(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='clubs/', blank=True)
    category = models.CharField(max_length=100, blank=True)
    coordinator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='coordinated_clubs')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ClubMembership(models.Model):
    ROLE_CHOICES = [('member', 'Member'), ('coordinator', 'Coordinator'), ('vice_coordinator', 'Vice Coordinator')]
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='memberships')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='club_memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('club', 'student')

    def __str__(self):
        return f'{self.student.full_name} - {self.club.name}'


class ClubApplication(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='applications')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='club_applications')
    email = models.EmailField(blank=True, help_text='Student email for contact')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField(blank=True, help_text='Why do you want to join?')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('club', 'student')

    def __str__(self):
        return f'{self.student.full_name} -> {self.club.name} ({self.get_status_display()})'


class CellCoordinator(models.Model):
    cell = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='coordinators')
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200, help_text='e.g. Chief Coordinator, Faculty Coordinator')
    qualification = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True, validators=[RegexValidator(r'^\+?1?\d{9,15}$', message='Enter a valid phone number')])
    photo = models.ImageField(upload_to='coordinators/', blank=True)
    is_chief = models.BooleanField(default=False, help_text='Chief Coordinator / Head of the cell')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['cell', '-is_chief', 'order', 'name']

    def __str__(self):
        return f'{self.name} - {self.cell.name}'


class ClubEvent(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    venue = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.title} ({self.club.name})'
