from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import models as db_models
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.edit import DeleteView
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
from .forms import StudentForm
from .models import Class, Student


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 20

    def get_queryset(self):
        qs = Student.objects.filter(is_deleted=False)
        search = self.request.GET.get('search', '')
        class_id = self.request.GET.get('class', '')
        gender = self.request.GET.get('gender', '')
        if search:
            qs = qs.filter(
                db_models.Q(first_name__icontains=search) |
                db_models.Q(last_name__icontains=search) |
                db_models.Q(roll_number__icontains=search)
            )
        if class_id:
            qs = qs.filter(student_class_id=class_id)
        if gender:
            qs = qs.filter(gender=gender)
        return qs.select_related('student_class')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['classes'] = Class.objects.all()
        ctx['current_class'] = self.request.GET.get('class', '')
        ctx['current_gender'] = self.request.GET.get('gender', '')
        ctx['search'] = self.request.GET.get('search', '')
        return ctx


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'students/student_detail.html'
    context_object_name = 'student'

    def get_queryset(self):
        return Student.objects.filter(is_deleted=False).select_related('student_class')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from attendance.models import Attendance
        from results.models import Result
        student = self.object
        ctx['attendance_records'] = Attendance.objects.filter(student=student)[:30]
        ctx['results'] = Result.objects.filter(student=student).select_related('exam', 'subject')[:20]
        return ctx


class StudentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:list')
    success_message = 'Student added successfully!'


class StudentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:list')
    success_message = 'Student updated successfully!'

    def get_queryset(self):
        return Student.objects.filter(is_deleted=False)


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    success_url = reverse_lazy('students:list')
    template_name = 'students/student_confirm_delete.html'

    def get_queryset(self):
        return Student.objects.filter(is_deleted=False)

    def form_valid(self, form):
        self.object.is_deleted = True
        self.object.save()
        return super().form_valid(form)


class StudentAPIView(View):
    def get(self, request):
        class_id = request.GET.get('class', '')
        students = Student.objects.filter(is_deleted=False)
        if class_id:
            students = students.filter(student_class_id=class_id)
        data = {
            'students': [
                {
                    'id': s.id,
                    'name': s.full_name,
                    'roll': s.roll_number,
                }
                for s in students
            ]
        }
        return JsonResponse(data)
