import os
import django
from datetime import date, time
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school.settings")
django.setup()

from home_auth.models import CustomUser
from faculty.models import Department, Teacher
from subjects.models import Subject, Exam, Enrollment, ExamResult, Timetable

def populate():
    print("Creating Department...")
    dept, created = Department.objects.get_or_create(
        department_id="CS101",
        defaults={
            'name': 'Computer Science',
            'head_of_department': 'Dr. Alami',
            'start_year': 2000,
            'students_capacity': 200
        }
    )

    print("Creating Teacher...")
    teacher, created = Teacher.objects.get_or_create(
        teacher_id="T001",
        defaults={
            'first_name': 'Ayoub',
            'last_name': 'Chentouf',
            'gender': 'Male',
            'date_of_birth': date(1985, 5, 20),
            'joining_date': date(2015, 9, 1),
            'mobile_number': '0600000001',
            'experience': '10 Years',
            'department': dept,
            'email': 'ayoub.chentouf@example.com'
        }
    )
    t_user, created = CustomUser.objects.get_or_create(username='ayoub', defaults={'email': 'ayoub@example.com', 'is_teacher': True, 'first_name': 'Ayoub', 'last_name': 'Chentouf', 'is_authorized': True})
    if created:
        t_user.set_password('password123')
        t_user.save()

    print("Creating Subjects & Exams...")
    sub_math, _ = Subject.objects.get_or_create(subject_id="SUBJ-MATH1", defaults={'name': 'Mathematics 101', 'department': dept, 'teacher': teacher})
    exam_math, _ = Exam.objects.get_or_create(exam_id="EXAM-MATH101", defaults={
        'name': 'Midterm Calculus', 'subject': sub_math, 
        'exam_date': date(2026, 4, 15), 'start_time': time(9, 0), 'end_time': time(11, 0)
    })

    # Physics
    sub_phys, _ = Subject.objects.get_or_create(subject_id="SUBJ-PHYS1", defaults={'name': 'Physics 101', 'department': dept, 'teacher': teacher})
    exam_phys, _ = Exam.objects.get_or_create(exam_id="EXAM-PHYS101", defaults={
        'name': 'Mechanics Final', 'subject': sub_phys, 
        'exam_date': date(2026, 4, 18), 'start_time': time(14, 0), 'end_time': time(16, 0)
    })

    print("Creating Timetable Layouts...")
    Timetable.objects.get_or_create(subject=sub_math, day='1', start_time=time(9,0), end_time=time(11,0), room_number="101")
    Timetable.objects.get_or_create(subject=sub_math, day='3', start_time=time(9,0), end_time=time(11,0), room_number="101")

    Timetable.objects.get_or_create(subject=sub_phys, day='2', start_time=time(14,0), end_time=time(16,0), room_number="202")
    Timetable.objects.get_or_create(subject=sub_phys, day='4', start_time=time(14,0), end_time=time(16,0), room_number="202")

    print("Creating Moroccan Students...")
    students_data = [
        ('youssef', 'youssef@example.com', 'Youssef', 'Alaoui'),
        ('fatima', 'fatima@example.com', 'Fatima Zahra', 'Idrissi'),
        ('omar', 'omar@example.com', 'Omar', 'Bennis'),
        ('khadija', 'khadija@example.com', 'Khadija', 'Tazi'),
        ('amine', 'amine@example.com', 'Amine', 'El Fassi')
    ]

    for un, eml, fn, ln in students_data:
        student, created = CustomUser.objects.get_or_create(username=un, defaults={
            'email': eml, 'first_name': fn, 'last_name': ln, 'is_student': True, 'is_authorized': True
        })
        if created:
            student.set_password('password123')
            student.save()
            print(f"Created student: {fn} {ln}")

        Enrollment.objects.get_or_create(student=student, subject=sub_math)
        Enrollment.objects.get_or_create(student=student, subject=sub_phys)

        marks_m = round(random.uniform(10.0, 20.0), 2)
        ExamResult.objects.get_or_create(student=student, exam=exam_math, defaults={'marks_obtained': marks_m, 'comments': 'Excellent'})
        
        marks_p = round(random.uniform(8.0, 19.5), 2)
        ExamResult.objects.get_or_create(student=student, exam=exam_phys, defaults={'marks_obtained': marks_p, 'comments': 'Good work'})

    print("Success! Dummy data has been populated.")

if __name__ == '__main__':
    populate()
