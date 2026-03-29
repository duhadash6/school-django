from django.db import models
from faculty.models import Department, Teacher

class Subject(models.Model):
    subject_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    
    # Link to the Department
    department = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE, 
        related_name='subjects'
    )
    teacher = models.ForeignKey(
        Teacher, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='taught_subjects'
    )

    def __str__(self):
        return f"{self.name} ({self.subject_id})"