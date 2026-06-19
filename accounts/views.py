from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, View
from django.contrib import messages
from django.db.utils import OperationalError, IntegrityError
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from .forms import LoginForm, UserRegisterForm
from .models import User
from students.models import Class, Student
from results.models import Exam


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('dashboard')

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except OperationalError:
            messages.error(request, 'Database not ready. Please try again.')
            return render(request, self.template_name, self.get_context_data())


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class StudentLoginView(View):
    template_name = 'accounts/student_login.html'

    def get(self, request):
        if request.session.get('student_id'):
            return redirect('accounts:student_portal')
        return render(request, self.template_name)

    def post(self, request):
        roll_number = request.POST.get('roll_number', '').strip()
        date_of_birth = request.POST.get('date_of_birth', '').strip()
        try:
            try:
                student = Student.objects.get(
                    roll_number=roll_number,
                    date_of_birth=date_of_birth,
                    is_deleted=False
                )
            except OperationalError:
                messages.error(request, 'Database not ready. Please try again.')
                return render(request, self.template_name)
            request.session['student_id'] = student.id
            request.session['student_name'] = student.full_name
            messages.success(request, f'Welcome, {student.full_name}!')
            return redirect('accounts:student_portal')
        except Student.DoesNotExist:
            messages.error(request, 'Invalid roll number or date of birth.')
            return render(request, self.template_name)


class StudentLogoutView(View):
    def get(self, request):
        request.session.pop('student_id', None)
        request.session.pop('student_name', None)
        messages.success(request, 'Logged out successfully.')
        return redirect('accounts:student_login')


class StudentPortalView(TemplateView):
    template_name = 'accounts/student_portal.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('student_id'):
            messages.error(request, 'Please login with your roll number and date of birth.')
            return redirect('accounts:student_login')
        try:
            Student.objects.get(id=request.session['student_id'], is_deleted=False)
        except Student.DoesNotExist:
            del request.session['student_id']
            del request.session['student_name']
            messages.error(request, 'Session expired. Please login again.')
            return redirect('accounts:student_login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        student = Student.objects.get(id=self.request.session['student_id'], is_deleted=False)
        from attendance.models import Attendance
        from results.models import Result
        ctx['student'] = student
        ctx['attendance_records'] = Attendance.objects.filter(student=student).order_by('-date')[:60]

        from django.db.models import Sum
        results = Result.objects.filter(student=student).select_related('exam', 'subject')
        ctx['results'] = results

        exam_groups = {}
        for r in results:
            exam_groups.setdefault(r.exam, []).append(r)
        for exam, rlist in exam_groups.items():
            total_obtained = sum(r.marks_obtained for r in rlist)
            total_max = sum(r.subject.max_marks for r in rlist)
            pct = round((total_obtained / total_max * 100), 2) if total_max else 0
            if pct >= 90: og = 'A+'
            elif pct >= 80: og = 'A'
            elif pct >= 70: og = 'B+'
            elif pct >= 60: og = 'B'
            elif pct >= 50: og = 'C+'
            elif pct >= 40: og = 'C'
            elif pct >= 33: og = 'D'
            else: og = 'F'
            rlist.append({
                'is_total_row': True,
                'total_obtained': round(total_obtained, 2),
                'total_max': total_max,
                'percentage': pct,
                'overall_grade': og,
            })
        ctx['exam_groups'] = exam_groups

        total_present = Attendance.objects.filter(student=student, status='present').count()
        total_days = Attendance.objects.filter(student=student).count()
        ctx['attendance_pct'] = round((total_present / total_days * 100)) if total_days else 0
        return ctx

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        student = Student.objects.get(
            id=request.session.get('student_id'),
            is_deleted=False
        )
        if student.profile_photo:
            messages.error(request, 'You can only upload a photo once. Contact admin to change it.')
            return redirect('accounts:student_portal')
        if request.FILES.get('profile_photo'):
            student.profile_photo = request.FILES['profile_photo']
            student.save()
            messages.success(request, 'Profile photo uploaded successfully!')
        else:
            messages.error(request, 'Please select a photo to upload.')
        return redirect('accounts:student_portal')


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from attendance.models import Attendance
        from django.utils import timezone
        today = timezone.localdate()
        try:
            total_students = Student.objects.filter(is_deleted=False).count()
            today_records = Attendance.objects.filter(date=today)
            today_total = today_records.count()
            today_present = today_records.filter(status='present').count()
            context['total_students'] = total_students
            context['today_attendance_pct'] = round((today_present / today_total * 100)) if today_total else 0
            context['today_total_attendance'] = today_total
            context['today_present'] = today_present
            context['classes_count'] = Class.objects.count()
            context['exams_count'] = Exam.objects.count()
        except OperationalError:
            context['total_students'] = 0
            context['today_attendance_pct'] = 0
            context['today_total_attendance'] = 0
            context['today_present'] = 0
            context['classes_count'] = 0
            context['exams_count'] = 0
        return context
