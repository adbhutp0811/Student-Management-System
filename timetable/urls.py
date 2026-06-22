from django.urls import path
from .views import TimetableView

app_name = 'timetable'
urlpatterns = [
    path('', TimetableView.as_view(), name='timetable'),
]
