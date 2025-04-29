from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Medication, Reminder
from .forms import UserRegisterForm, MedicationForm, ReminderForm
from django.contrib.auth import logout
from django.shortcuts import redirect


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'reminders/register.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('login') 

@login_required
def dashboard(request):
    medications = Medication.objects.filter(user=request.user)
    
    # Get current day's reminders
    today = timezone.now().date()
    day_of_week = today.isoweekday()  # 1-7 (Monday-Sunday)
    day_of_month = today.day
    
    today_reminders = []
    
    for med in medications:
        # For active medications only
        if med.start_date <= today and (med.end_date is None or med.end_date >= today):
            for reminder in med.reminders.all():
                add_reminder = False
                
                if reminder.frequency == 'daily':
                    add_reminder = True
                elif reminder.frequency == 'weekly' and reminder.days_of_week:
                    days = [int(d.strip()) for d in reminder.days_of_week.split(',')]
                    if day_of_week in days:
                        add_reminder = True
                elif reminder.frequency == 'monthly' and reminder.date_of_month:
                    if day_of_month == reminder.date_of_month:
                        add_reminder = True
                
                if add_reminder:
                    today_reminders.append({
                        'medication': med,
                        'time': reminder.time,
                        'notes': reminder.notes
                    })
    
    # Sort reminders by time
    today_reminders.sort(key=lambda x: x['time'])
    
    context = {
        'medications': medications,
        'today_reminders': today_reminders,
        'today': today
    }
    
    return render(request, 'reminders/dashboard.html', context)

class MedicationListView(LoginRequiredMixin, ListView):
    model = Medication
    template_name = 'reminders/medications_list.html'
    context_object_name = 'medications'
    
    def get_queryset(self):
        return Medication.objects.filter(user=self.request.user)

class MedicationCreateView(LoginRequiredMixin, CreateView):
    model = Medication
    form_class = MedicationForm
    template_name = 'reminders/medication_form.html'
    success_url = reverse_lazy('medications')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f'Medication {form.instance.name} has been added!')
        return response

class MedicationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Medication
    form_class = MedicationForm
    template_name = 'reminders/medication_form.html'
    success_url = reverse_lazy('medications')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Medication {form.instance.name} has been updated!')
        return response
    
    def test_func(self):
        medication = self.get_object()
        return self.request.user == medication.user

class MedicationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Medication
    template_name = 'reminders/medication_confirm_delete.html'
    success_url = reverse_lazy('medications')
    
    def test_func(self):
        medication = self.get_object()
        return self.request.user == medication.user
    
    def delete(self, request, *args, **kwargs):
        medication = self.get_object()
        messages.success(self.request, f'Medication {medication.name} has been deleted!')
        return super().delete(request, *args, **kwargs)

@login_required
def add_reminder(request, pk):
    medication = get_object_or_404(Medication, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.medication = medication
            reminder.save()
            messages.success(request, f'Reminder added for {medication.name}!')
            return redirect('medications')
    else:
        form = ReminderForm()
    
    return render(request, 'reminders/reminder_form.html', {
        'form': form,
        'medication': medication
    })
 # 'login' should be the name of your login URL pattern