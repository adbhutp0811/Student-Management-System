from django import forms
from .models import Attendance


class AttendanceForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    student_class = forms.ModelChoiceField(
        queryset=None,
        empty_label='Select Class',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from students.models import Class
        self.fields['student_class'].queryset = Class.objects.all()


class BulkAttendanceForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    def __init__(self, *args, students=None, **kwargs):
        super().__init__(*args, **kwargs)
        if students:
            for student in students:
                self.fields[f'student_{student.id}'] = forms.ChoiceField(
                    choices=Attendance.STATUS_CHOICES,
                    initial='present',
                    widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
                    label=f'{student.first_name} {student.last_name}'
                )
