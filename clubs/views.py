from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, View
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.utils import timezone
from .models import Club, ClubMembership, ClubEvent, ClubApplication
from students.models import Student


CELL_CATEGORIES = ['Student Welfare', 'Career & Placement', 'Innovation & Entrepreneurship', 'Student Activities']

class ClubListView(ListView):
    model = Club
    template_name = 'clubs/club_list.html'
    context_object_name = 'clubs'

    def get_queryset(self):
        return Club.objects.filter(is_active=True).exclude(category__in=CELL_CATEGORIES)


class ClubDetailView(DetailView):
    model = Club
    template_name = 'clubs/club_detail.html'
    context_object_name = 'club'
    slug_field = 'pk'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        club = self.object
        ctx['member_count'] = club.memberships.count()
        ctx['pending_apps'] = club.applications.filter(status='pending').count()
        ctx['coordinators'] = club.coordinators.all()

        student_id = self.request.session.get('student_id')
        if student_id:
            student = Student.objects.filter(id=student_id).first()
            ctx['student'] = student
            ctx['is_member'] = club.memberships.filter(student_id=student_id).exists() if student else False
            if student:
                app = club.applications.filter(student=student).first()
                ctx['application'] = app
                ctx['has_applied'] = app is not None
                ctx['app_status'] = app.status if app else None
            else:
                ctx['application'] = None
                ctx['has_applied'] = False
                ctx['app_status'] = None
        else:
            ctx['student'] = None
            ctx['is_member'] = False
            ctx['application'] = None
            ctx['has_applied'] = False
            ctx['app_status'] = None
        return ctx


@method_decorator(csrf_protect, name='dispatch')
class ClubApplyView(View):
    def post(self, request, *args, **kwargs):
        club = get_object_or_404(Club, pk=kwargs['pk'])
        roll = request.POST.get('roll_number', '').strip()
        email = request.POST.get('email', '').strip()
        reason = request.POST.get('reason', '').strip()

        try:
            student = Student.objects.get(roll_number=roll, is_deleted=False)
        except Student.DoesNotExist:
            messages.error(request, 'Student not found with this roll number.')
            return redirect('clubs:club_detail', pk=club.pk)

        if ClubMembership.objects.filter(club=club, student=student).exists():
            messages.warning(request, f'You are already a member of {club.name}.')
            return redirect('clubs:club_detail', pk=club.pk)

        if ClubApplication.objects.filter(club=club, student=student).exists():
            messages.warning(request, f'You have already applied to {club.name}. Wait for review.')
            return redirect('clubs:club_detail', pk=club.pk)

        ClubApplication.objects.create(club=club, student=student, email=email, reason=reason)
        messages.success(request, f'Application submitted to {club.name}. Wait for approval.')
        return redirect('clubs:club_detail', pk=club.pk)



