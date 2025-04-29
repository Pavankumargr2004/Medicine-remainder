from django.db import models
from django.contrib.auth.models import User

class Medication(models.Model):
    DOSAGE_UNITS = (
        ('mg', 'Milligrams'),
        ('g', 'Grams'),
        ('ml', 'Milliliters'),
        ('pill', 'Pill(s)'),
        ('tab', 'Tablet(s)'),
        ('cap', 'Capsule(s)'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    dosage = models.DecimalField(max_digits=10, decimal_places=2)
    dosage_unit = models.CharField(max_length=4, choices=DOSAGE_UNITS, default='mg')
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.dosage}{self.dosage_unit})"

class Reminder(models.Model):
    FREQUENCY_CHOICES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('as_needed', 'As Needed'),
    )
    
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, related_name='reminders')
    time = models.TimeField()
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='daily')
    days_of_week = models.CharField(max_length=20, blank=True, null=True, help_text="Comma separated days: 1-7 (Monday-Sunday)")
    date_of_month = models.PositiveSmallIntegerField(blank=True, null=True, help_text="Day of month for monthly reminders")
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.medication.name} - {self.time} ({self.frequency})"