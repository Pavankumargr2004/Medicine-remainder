from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Medication, Reminder

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'description', 'dosage', 'dosage_unit', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'required': False}),
        }

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['time', 'frequency', 'days_of_week', 'date_of_month', 'notes']
        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'days_of_week': forms.TextInput(attrs={'placeholder': 'For weekly: 1,3,5 (Mon,Wed,Fri)'}),
            'date_of_month': forms.NumberInput(attrs={'placeholder': 'For monthly reminders'}),
        }