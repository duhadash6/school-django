from django import forms
from .models import Subject

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_id', 'name', 'department', 'teacher']
        widgets = {
            'subject_id': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
        }