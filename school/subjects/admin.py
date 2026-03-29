from django.contrib import admin
from .models import Subject

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_id', 'name', 'department', 'teacher')
    list_filter = ('department', 'teacher')