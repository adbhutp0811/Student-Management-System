from django.contrib import admin
from .models import Exam, Result, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'student_class', 'max_marks', 'pass_marks')
    list_filter = ('student_class',)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'exam_type', 'student_class', 'start_date', 'end_date', 'is_published')
    list_filter = ('exam_type', 'student_class', 'academic_year')


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'subject', 'marks_obtained', 'grade')
    list_filter = ('exam', 'subject', 'exam__student_class')
    search_fields = ('student__first_name', 'student__last_name')
