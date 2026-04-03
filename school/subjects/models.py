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


class Exam(models.Model):
    exam_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(
        Subject, 
        on_delete=models.CASCADE, 
        related_name='exams'
    )
    
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.name} - {self.subject.name}"


from django.conf import settings

class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='enrollments',
        limit_choices_to={'is_student': True}
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='enrollments')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ('student', 'subject')

    def __str__(self):
        return f"{self.student} enrolled in {self.subject}"


class ExamResult(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='exam_results',
        limit_choices_to={'is_student': True}
    )
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    comments = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ('student', 'exam')

    def __str__(self):
        return f"{self.student} - {self.exam}"

class Timetable(models.Model):
    DAYS_OF_WEEK = [
        ('0', 'Sunday'),
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
    ]
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='timetables')
    day = models.CharField(max_length=1, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.subject.name} on {self.get_day_display()} ({self.start_time} - {self.end_time})"