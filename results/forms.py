from django import forms
from .models import Exam, Result, Subject


class ResultForm(forms.Form):
    exam = forms.ModelChoiceField(
        queryset=Exam.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class BulkResultForm(forms.Form):
    def __init__(self, *args, students=None, subject=None, exam=None, **kwargs):
        super().__init__(*args, **kwargs)
        if students and subject:
            for student in students:
                existing = Result.objects.filter(
                    student=student, subject=subject, exam=exam
                ).first()
                val = existing.marks_obtained if existing else ''
                self.fields[f'marks_{student.id}'] = forms.FloatField(
                    required=False,
                    initial=val,
                    min_value=0,
                    max_value=subject.max_marks,
                    widget=forms.NumberInput(attrs={
                        'class': 'form-control form-control-sm marks-input',
                        'placeholder': f'Max: {subject.max_marks}',
                        'data-max': subject.max_marks,
                    }),
                    label=f'{student.first_name} {student.last_name} ({student.roll_number})',
                )
