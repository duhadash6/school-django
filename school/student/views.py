from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from home_auth.decorators import role_required
from .models import Student, Parent
import csv

@role_required(['admin', 'teacher', 'student'])
def student_list(request):
    students = Student.objects.all()
    context = {'student_list': students}
    return render(request, 'students/students.html', context)

@role_required(['admin'])
def add_student(request):
    if request.method == 'POST':
        # Récupérer les données de l'étudiant
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        student_class = request.POST.get('student_class')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        section = request.POST.get('section')
        student_image = request.FILES.get('student_image')

        # Récupérer les données du parent
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_mobile = request.POST.get('father_mobile')
        father_email = request.POST.get('father_email')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_mobile = request.POST.get('mother_mobile')
        mother_email = request.POST.get('mother_email')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')

        # Créer d'abord le parent
        parent = Parent.objects.create(
            father_name=father_name,
            father_occupation=father_occupation,
            father_mobile=father_mobile,
            father_email=father_email,
            mother_name=mother_name,
            mother_occupation=mother_occupation,
            mother_mobile=mother_mobile,
            mother_email=mother_email,
            present_address=present_address,
            permanent_address=permanent_address,
        )

        # Puis créer l'étudiant lié au parent
        student = Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            student_id=student_id,
            gender=gender,
            date_of_birth=date_of_birth,
            student_class=student_class,
            joining_date=joining_date,
            mobile_number=mobile_number,
            admission_number=admission_number,
            section=section,
            student_image=student_image,
            parent=parent,
        )

        messages.success(request, 'Student added Successfully')
        return redirect('student_list')

    return render(request, 'students/add-student.html')

@role_required(['admin'])
def edit_student(request, student_id):
    student = Student.objects.filter(student_id=student_id).first()
    parent = student.parent

    if request.method == 'POST':
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.student_id = request.POST.get('student_id')
        student.gender = request.POST.get('gender')
        student.date_of_birth = request.POST.get('date_of_birth')
        student.student_class = request.POST.get('student_class')
        student.joining_date = request.POST.get('joining_date')
        student.mobile_number = request.POST.get('mobile_number')
        student.admission_number = request.POST.get('admission_number')
        student.section = request.POST.get('section')
        
        if request.FILES.get('student_image'):
            student.student_image = request.FILES.get('student_image')

        parent.father_name = request.POST.get('father_name')
        parent.father_occupation = request.POST.get('father_occupation')
        parent.father_mobile = request.POST.get('father_mobile')
        parent.father_email = request.POST.get('father_email')
        parent.mother_name = request.POST.get('mother_name')
        parent.mother_occupation = request.POST.get('mother_occupation')
        parent.mother_mobile = request.POST.get('mother_mobile')
        parent.mother_email = request.POST.get('mother_email')
        parent.present_address = request.POST.get('present_address')
        parent.permanent_address = request.POST.get('permanent_address')

        parent.save()
        student.save()

        messages.success(request, 'Student updated Successfully')
        return redirect('student_list')

    context = {'student': student, 'parent': parent}
    return render(request, 'students/edit-student.html', context)

@role_required(['admin', 'teacher', 'student'])
def view_student(request, student_id):
    student = Student.objects.filter(student_id=student_id).first()
    context = {'student': student}
    return render(request, 'students/student-details.html', context)

@role_required(['admin'])
def delete_student(request, student_id):
    student = Student.objects.filter(student_id=student_id).first()
    if student and hasattr(student, 'parent'):
        student.parent.delete()
    messages.success(request, 'Student deleted Successfully')
    return redirect('student_list')

@role_required(['admin', 'teacher', 'student'])
def student_view_generic(request):
    students = Student.objects.all()
    return render(request, 'students/select_student.html', {'students': students, 'action': 'view'})

@role_required(['admin'])
def student_edit_generic(request):
    students = Student.objects.all()
    return render(request, 'students/select_student.html', {'students': students, 'action': 'edit'})

@role_required(['student'])
def student_dashboard(request):
    from subjects.models import Subject, Enrollment, Exam, ExamResult, Timetable
    from datetime import date, datetime

    user = request.user

    # Enrolled courses
    enrolled_ids = Enrollment.objects.filter(student=user).values_list('subject_id', flat=True)
    enrolled_count = enrolled_ids.count()
    total_subjects = Subject.objects.count()

    # Exams for enrolled subjects
    enrolled_exams = Exam.objects.filter(subject_id__in=enrolled_ids)
    total_exams = enrolled_exams.count()

    # Exam results
    results = ExamResult.objects.filter(student=user, exam__in=enrolled_exams)
    exams_attended = results.count()
    exams_passed = results.filter(marks_obtained__gte=50).count()

    # Today's timetable
    today_dow = str(datetime.now().weekday() + 1)  # model: 1=Mon ... 5=Fri
    if datetime.now().weekday() == 6:  # Sunday
        today_dow = '0'
    todays_classes = Timetable.objects.filter(
        subject_id__in=enrolled_ids, day=today_dow
    ).select_related('subject').order_by('start_time')

    # Upcoming exams (next 5)
    upcoming_exams = Exam.objects.filter(
        subject_id__in=enrolled_ids, exam_date__gte=date.today()
    ).select_related('subject').order_by('exam_date', 'start_time')[:5]

    context = {
        'enrolled_count': enrolled_count,
        'total_subjects': total_subjects,
        'total_exams': total_exams,
        'exams_attended': exams_attended,
        'exams_passed': exams_passed,
        'todays_classes': todays_classes,
        'upcoming_exams': upcoming_exams,
    }
    return render(request, 'students/student-dashboard.html', context)

@role_required(['admin', 'teacher'])
def export_students_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['Student ID', 'First Name', 'Last Name', 'Class', 'Date of Birth', 'Mobile', 'Admission No', 'Section', 'Father Name', 'Mother Name', 'Address'])

    students = Student.objects.select_related('parent').all()
    for s in students:
        writer.writerow([
            s.student_id, s.first_name, s.last_name,
            s.student_class, s.date_of_birth, s.mobile_number,
            s.admission_number, s.section,
            s.parent.father_name if s.parent else '',
            s.parent.mother_name if s.parent else '',
            s.parent.present_address if s.parent else '',
        ])

    return response