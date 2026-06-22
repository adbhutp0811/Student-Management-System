from django.db import models
from django.conf import settings


class Event(models.Model):
    CATEGORY_CHOICES = [
        ('academic', 'Academic'), ('cultural', 'Cultural'), ('sports', 'Sports'),
        ('technical', 'Technical'), ('workshop', 'Workshop'), ('seminar', 'Seminar'),
    ]
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    venue = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='academic')
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_upcoming = models.BooleanField(default=True)
    registration_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title
