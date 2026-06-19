from collections import defaultdict

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, FormView, ListView, TemplateView
from students.models import Class, Student
from .forms import BulkResultForm, ResultForm
from .models import Exam, Result, Subject


class ManageResultsView(LoginRequiredMixin, TemplateView):
    template_name = 'results/manage_results.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['classes'] = Class.objects.all()
        ctx['exam_form'] = ResultForm()
        return ctx


class GetSubjectsExamView(LoginRequiredMixin, View):
    def get(self, request):
        class_id = request.GET.get('class_id')
        exam_id = request.GET.get('exam_id')
        subject_id = request.GET.get('subject_id')
        subjects = Subject.objects.filter(student_class_id=class_id).values('id', 'name', 'max_marks')
        exams = Exam.objects.filter(student_class_id=class_id).values('id', 'name', 'exam_type')
        data = {
            'subjects': list(subjects),
            'exams': list(exams),
        }
        if exam_id and subject_id:
            results = Result.objects.filter(
                exam_id=exam_id, subject_id=subject_id
            ).values('student_id', 'marks_obtained', 'grade', 'grade_auto')
            data['results'] = list(results)
        return JsonResponse(data)


class SaveResultsView(LoginRequiredMixin, View):
    def post(self, request):
        exam_id = request.POST.get('exam')
        subject_id = request.POST.get('subject')
        marks_data = {k: v for k, v in request.POST.items() if k.startswith('marks_')}
        grade_data = {k: v for k, v in request.POST.items() if k.startswith('grade_')}
        grade_auto_data = {k: v for k, v in request.POST.items() if k.startswith('grade_auto_')}
        subject = get_object_or_404(Subject, id=subject_id)
        for key, value in marks_data.items():
            if value:
                student_id = int(key.replace('marks_', ''))
                grade = grade_data.get(f'grade_{student_id}', '')
                grade_auto = grade_auto_data.get(f'grade_auto_{student_id}', 'true') == 'true'
                defaults = {
                    'marks_obtained': float(value),
                    'grade': grade,
                    'grade_auto': grade_auto,
                }
                result, created = Result.objects.get_or_create(
                    student_id=student_id,
                    exam_id=exam_id,
                    subject_id=subject_id,
                    defaults=defaults,
                )
                if not created:
                    result.marks_obtained = float(value)
                    result.grade = grade
                    result.grade_auto = grade_auto
                    result.save()
        messages.success(request, 'Results saved successfully!')
        return redirect('results:manage')


class ClassResultSummaryView(LoginRequiredMixin, TemplateView):
    template_name = 'results/class_summary.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        class_id = self.request.GET.get('class', '')
        exam_id = self.request.GET.get('exam', '')
        ctx['classes'] = Class.objects.all()
        ctx['exams'] = Exam.objects.all()
        ctx['current_class'] = class_id
        ctx['current_exam'] = exam_id

        if class_id and exam_id:
            students = Student.objects.filter(student_class_id=class_id, is_deleted=False)
            subjects = Subject.objects.filter(student_class_id=class_id)
            summary = []
            for s in students:
                results = Result.objects.filter(student=s, exam_id=exam_id)
                total_marks = sum(r.marks_obtained for r in results)
                max_marks = sum(r.subject.max_marks for r in results)
                pct = round((total_marks / max_marks * 100), 2) if max_marks else 0
                failed = any(not r.is_pass for r in results)
                summary.append({
                    'student': s,
                    'results': results,
                    'total_marks': round(total_marks, 2),
                    'max_marks': max_marks,
                    'percentage': pct,
                    'failed': failed,
                    'grade': self.calculate_overall_grade(pct),
                })
            summary.sort(key=lambda x: x['percentage'], reverse=True)
            ctx['summary'] = summary
            ctx['subjects'] = subjects
            ctx['passed'] = sum(1 for s in summary if not s['failed'])
            ctx['failed_count'] = sum(1 for s in summary if s['failed'])
        return ctx

    def calculate_overall_grade(self, pct):
        if pct >= 90: return 'A+'
        if pct >= 80: return 'A'
        if pct >= 70: return 'B+'
        if pct >= 60: return 'B'
        if pct >= 50: return 'C+'
        if pct >= 40: return 'C'
        if pct >= 33: return 'D'
        return 'F'


class ReportCardView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'results/report_card.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        exam_id = self.request.GET.get('exam')
        if exam_id:
            ctx['exam'] = get_object_or_404(Exam, id=exam_id)
            ctx['results'] = Result.objects.filter(
                student=self.object, exam_id=exam_id
            ).select_related('subject')
            total = sum(r.marks_obtained for r in ctx['results'])
            max_m = sum(r.subject.max_marks for r in ctx['results'])
            ctx['total_marks'] = round(total, 2)
            ctx['max_marks'] = max_m
            ctx['percentage'] = round((total / max_m * 100), 2) if max_m else 0
        ctx['exams'] = Exam.objects.filter(student_class=self.object.student_class)
        return ctx
