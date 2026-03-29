from django import forms
from .models import Holiday

class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'holiday_id': forms.TextInput(attrs={'class': 'form-control'}),
        }