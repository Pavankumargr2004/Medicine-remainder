from django.contrib import admin
from .models import Medication, Reminder

class ReminderInline(admin.TabularInline):
    model = Reminder
    extra = 1

class MedicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'dosage', 'dosage_unit', 'start_date', 'end_date')
    list_filter = ('user', 'dosage_unit', 'start_date')
    search_fields = ('name', 'description', 'user__username')
    inlines = [ReminderInline]

admin.site.register(Medication, MedicationAdmin)
admin.site.register(Reminder)
