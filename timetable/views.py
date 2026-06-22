from django.views.generic import TemplateView
from students.models import Class
from .models import TimeSlot


class TimetableView(TemplateView):
    template_name = 'timetable/timetable.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['classes'] = Class.objects.all()
        selected_class_id = self.request.GET.get('class_id')
        if selected_class_id:
            ctx['selected_class'] = Class.objects.get(id=selected_class_id)
            ctx['time_slots'] = TimeSlot.objects.filter(student_class_id=selected_class_id)
        else:
            ctx['time_slots'] = TimeSlot.objects.none()
        ctx['days'] = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        return ctx
