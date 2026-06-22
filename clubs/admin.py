from django.contrib import admin, messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from django.db import IntegrityError
from .models import Club, ClubMembership, ClubEvent, ClubApplication, CellCoordinator


@admin.register(ClubApplication)
class ClubApplicationAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'roll_number', 'email', 'club', 'status', 'applied_on', 'reviewed_on')
    list_filter = ('status', 'club')
    search_fields = ('student__first_name', 'student__last_name', 'student__roll_number', 'club__name')
    actions = ['approve_applications', 'reject_applications']

    def student_name(self, obj):
        return obj.student.full_name
    student_name.short_description = 'Student'

    def roll_number(self, obj):
        return obj.student.roll_number
    roll_number.short_description = 'Roll No'

    def applied_on(self, obj):
        return obj.created_at.strftime('%d %b %Y')
    applied_on.short_description = 'Applied'

    def reviewed_on(self, obj):
        return obj.reviewed_at.strftime('%d %b %Y') if obj.reviewed_at else '-'
    reviewed_on.short_description = 'Reviewed'

    def _send_notification(self, app, subject, template, status):
        recipient = app.email or app.student.email
        if not recipient:
            return
        context = {'student': app.student, 'club': app.club, 'status': status}
        message = render_to_string(template, context)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL or None, [recipient], fail_silently=False)

    def approve_applications(self, request, queryset):
        pending = queryset.filter(status='pending')
        count = 0
        errors = []
        for app in pending:
            app_id = app.pk
            try:
                ClubApplication.objects.filter(pk=app_id).update(
                    status='approved',
                    reviewed_at=timezone.now(),
                    reviewed_by=request.user
                )
                ClubMembership.objects.get_or_create(
                    club_id=app.club_id,
                    student_id=app.student_id,
                    defaults={'role': 'member'}
                )
                try:
                    app.status = 'approved'
                    self._send_notification(
                        app,
                        f'Application Approved - {app.club.name}',
                        'clubs/emails/application_approved.txt',
                        'approved'
                    )
                except Exception as e:
                    errors.append(f'{app.student.full_name}: email error - {e}')
                count += 1
            except IntegrityError:
                errors.append(f'{app.student.full_name}: already a member')
                count += 1
            except Exception as e:
                errors.append(f'{app.student.full_name}: {e}')
        msg = f'{count} application(s) approved.'
        if errors:
            msg += f' Issues: {" | ".join(errors)}'
        self.message_user(request, msg, messages.SUCCESS if not errors else messages.WARNING)
    approve_applications.short_description = 'Approve selected applications'

    def reject_applications(self, request, queryset):
        pending = queryset.filter(status='pending')
        count = 0
        for app in pending:
            ClubApplication.objects.filter(pk=app.pk).update(
                status='rejected',
                reviewed_at=timezone.now(),
                reviewed_by=request.user
            )
            try:
                self._send_notification(
                    app,
                    f'Application Status - {app.club.name}',
                    'clubs/emails/application_rejected.txt',
                    'rejected'
                )
            except Exception as e:
                pass
            count += 1
        self.message_user(request, f'{count} application(s) rejected.', messages.INFO)
    reject_applications.short_description = 'Reject selected applications'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'club')


admin.site.register(Club)
admin.site.register(ClubMembership)
admin.site.register(ClubEvent)

@admin.register(CellCoordinator)
class CellCoordinatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'cell', 'designation', 'is_chief', 'order')
    list_filter = ('cell', 'is_chief')
    search_fields = ('name', 'cell__name')
    list_editable = ('order',)
