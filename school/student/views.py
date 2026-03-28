from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Student, Parent

def student_list(request):
    students = Student.objects.all()
    context = {'student_list': students}
    return render(request, 'students/students.html', context)

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

def view_student(request, student_id):
    student = Student.objects.filter(student_id=student_id).first()
    context = {'student': student}
    return render(request, 'students/student-details.html', context)

def delete_student(request, student_id):
    student = Student.objects.filter(student_id=student_id).first()
    if student and hasattr(student, 'parent'):
        student.parent.delete()
    messages.success(request, 'Student deleted Successfully')
    return redirect('student_list')

def student_view_generic(request):
    student = Student.objects.first()
    if student:
        return redirect('view_student', student_id=student.student_id)
    return redirect('add_student')

def student_edit_generic(request):
    student = Student.objects.first()
    if student:
        return redirect('edit_student', student_id=student.student_id)
    return redirect('add_student')

def student_dashboard(request):
    return render(request, 'students/student-dashboard.html')