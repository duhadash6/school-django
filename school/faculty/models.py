from django.db import models

class Department(models.Model):
    department_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    head_of_department = models.CharField(max_length=100, blank=True)
    start_year = models.IntegerField()
    students_capacity = models.IntegerField()

    def __str__(self):
        return self.name

class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    teacher_id = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    date_of_birth = models.DateField()
    joining_date = models.DateField()
    mobile_number = models.CharField(max_length=15)
    experience = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to='teachers/', blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='teachers')
    
    email = models.EmailField(max_length=100, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.teacher_id})"
