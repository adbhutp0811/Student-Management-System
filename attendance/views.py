from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, FormView, ListView, TemplateView
from students.models import Class, Student
from .forms import AttendanceForm, BulkAttendanceForm
from .models import Attendance


class MarkAttendanceView(LoginRequiredMixin, TemplateView):
    template_name = 'attendance/mark_attendance.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = AttendanceForm()
        ctx['classes'] = Class.objects.all()
        return ctx


class GetStudentsForClassView(LoginRequiredMixin, View):
    def get(self, request, class_id):
        date = request.GET.get('date', '')
        students = Student.objects.filter(student_class_id=class_id, is_deleted=False)
        existing = Attendance.objects.filter(date=date, student__student_class_id=class_id)
        existing_map = {a.student_id: a.status for a in existing}
        data = []
        for s in students:
            data.append({
                'id': s.id,
                'name': s.full_name,
                'roll': s.roll_number,
                'status': existing_map.get(s.id, 'present'),
                'photo': s.profile_photo.url if s.profile_photo else '',
            })
        return JsonResponse({'students': data})


class SaveAttendanceView(LoginRequiredMixin, View):
    def post(self, request):
        date = request.POST.get('date')
        class_id = request.POST.get('class_id')
        statuses = {k: v for k, v in request.POST.items() if k.startswith('status_')}
        student_ids = Student.objects.filter(
            student_class_id=class_id, is_deleted=False
        ).values_list('id', flat=True)
        for sid in student_ids:
            status = statuses.get(f'status_{sid}', 'present')
            Attendance.objects.update_or_create(
                student_id=sid,
                date=date,
                defaults={
                    'student_class_id': class_id,
                    'status': status,
                    'marked_by': request.user,
                }
            )
        messages.success(request, 'Attendance saved successfully!')
        return redirect('attendance:mark')


class AttendanceHistoryView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = 'attendance/attendance_history.html'
    context_object_name = 'records'
    paginate_by = 30

    def get_queryset(self):
        qs = Attendance.objects.select_related('student', 'student_class')
        student_id = self.request.GET.get('student_id', '')
        class_id = self.request.GET.get('class', '')
        month = self.request.GET.get('month', '')
        if student_id:
            qs = qs.filter(student_id=student_id)
        if class_id:
            qs = qs.filter(student_class_id=class_id)
        if month:
            year, m = month.split('-')
            qs = qs.filter(date__year=year, date__month=m)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['classes'] = Class.objects.all()
        ctx['students'] = Student.objects.filter(is_deleted=False)
        ctx['current_class'] = self.request.GET.get('class', '')
        ctx['current_student'] = self.request.GET.get('student_id', '')
        ctx['current_month'] = self.request.GET.get('month', '')
        return ctx


class AttendanceSummaryView(LoginRequiredMixin, TemplateView):
    template_name = 'attendance/attendance_summary.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        class_id = self.request.GET.get('class', '')
        month = self.request.GET.get('month', timezone.localdate().strftime('%Y-%m'))
        ctx['classes'] = Class.objects.all()
        ctx['current_class'] = class_id
        ctx['current_month'] = month
        students = Student.objects.filter(is_deleted=False)
        if class_id:
            students = students.filter(student_class_id=class_id)
        summary = []
        for s in students:
            records = Attendance.objects.filter(student=s)
            if month:
                year, m = month.split('-')
                records = records.filter(date__year=year, date__month=m)
            total = records.count()
            present = records.filter(status='present').count()
            absent = records.filter(status='absent').count()
            late = records.filter(status='late').count()
            leave = records.filter(status='leave').count()
            pct = round((present / total * 100)) if total else 0
            summary.append({
                'student': s,
                'total': total,
                'present': present,
                'absent': absent,
                'late': late,
                'leave': leave,
                'percentage': pct,
            })
        ctx['summary'] = summary
        return ctx
