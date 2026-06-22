from django.contrib import admin
from .models import Class, Student


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'academic_year')
    list_filter = ('name', 'section')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'first_name', 'last_name', 'student_class', 'gender', 'is_deleted')
    list_filter = ('student_class', 'gender', 'is_deleted')
    search_fields = ('first_name', 'last_name', 'roll_number')
    actions = ['soft_delete']

    @admin.action(description='Soft delete selected students')
    def soft_delete(self, request, queryset):
        queryset.update(is_deleted=True)
