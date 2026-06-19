from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status', 'student_class')
    list_filter = ('date', 'status', 'student_class')
    search_fields = ('student__first_name', 'student__last_name', 'student__roll_number')
    date_hierarchy = 'date'
