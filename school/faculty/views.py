from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from home_auth.decorators import role_required
from django.http import Http404
from django.template import TemplateDoesNotExist
from .models import Teacher, Department
from student.models import Student
from subjects.models import Subject, Enrollment, ExamResult
from django.db.models import F

@role_required(['admin'])
def admin_dashboard(request):
    # Real counts from the database
    student_count = Student.objects.count()
    teacher_count = Teacher.objects.count()
    department_count = Department.objects.count()
    subject_count = Subject.objects.count()

    # Recent students (last 5, ordered by joining date)
    recent_students = Student.objects.order_by('-joining_date')[:5]

    # Recent teachers (last 5, ordered by joining date)
    recent_teachers = Teacher.objects.select_related('department').order_by('-joining_date')[:5]

    # Recent Activities Feed
    activities = []
    
    # 1. New Enrollments
    enrollments = Enrollment.objects.select_related('student', 'subject').order_by('-created_at')[:5]
    for en in enrollments:
        activities.append({
            'date': en.created_at,
            'text': f"{en.student.first_name} {en.student.last_name} a rejoint le module de \"{en.subject.name}\"",
            'type': 'enroll'
        })
        
    # 2. Exam Results / Validations
    results = ExamResult.objects.select_related('student', 'exam__subject').order_by('-created_at')[:5]
    for res in results:
        activities.append({
            'date': res.created_at,
            'text': f"{res.student.first_name} {res.student.last_name} a validé son module de \"{res.exam.subject.name}\"",
            'type': 'validation'
        })
        
    # 3. New Students Joining (using joining_date as fallback or created_at if added)
    for st in recent_students:
        activities.append({
            'date': st.joining_date,
            'text': f"{st.first_name} {st.last_name} a rejoint l'école",
            'type': 'join'
        })

    # Sort all activities by date (handling mixed Date/DateTime properly with timezone awareness)
    from datetime import date, datetime
    from django.utils import timezone
    activities.sort(key=lambda x: x['date'] if isinstance(x['date'], datetime) else timezone.make_aware(datetime.combine(x['date'], datetime.min.time())), reverse=True)
    activities = activities[:10]  # Limit to 10 latest activities

    context = {
        'student_count': student_count,
        'teacher_count': teacher_count,
        'department_count': department_count,
        'subject_count': subject_count,
        'recent_students': recent_students,
        'recent_teachers': recent_teachers,
        'activities': activities,
    }
    return render(request, 'Home/index.html', context)

@role_required(['admin', 'teacher', 'student'])
def index(request):
    if getattr(request.user, 'is_admin', False):
        return redirect('admin_dashboard')
    elif getattr(request.user, 'is_teacher', False):
        return redirect('teacher_dashboard')
    elif getattr(request.user, 'is_student', False):
        return redirect('student_dashboard')
    return redirect('login')

@role_required(['admin', 'teacher', 'student'])
def inbox(request):
    return render(request, 'inbox.html')

@role_required(['admin', 'teacher', 'student'])
def profile(request):
    return render(request, 'profile.html')

@role_required(['admin', 'teacher', 'student'])
def dynamic_template(request, template_name):
    # This allows rendering any HTML template requested directly, useful for migration
    try:
        # Try finding it exactly as requested (e.g., if placed in templates/)
        return render(request, template_name)
    except TemplateDoesNotExist:
        try:
            # Check Home subdirectory where many templates seem to go
            return render(request, f'Home/{template_name}')
        except TemplateDoesNotExist:
            try:
                # Check students subdirectory
                return render(request, f'students/{template_name}')
            except TemplateDoesNotExist:
                raise Http404(f"Template {template_name} does not exist. Please make sure the file is in your templates folder.")

# --- Departments ---
@role_required(['admin', 'teacher', 'student'])
def department_list(request):
    departments = Department.objects.all()
    context = {'department_list': departments}
    return render(request, 'departments/departments.html', context)

@role_required(['admin'])
def add_department(request):
    if request.method == 'POST':
        department_id = request.POST.get('department_id')
        name = request.POST.get('name')
        head_of_department = request.POST.get('head_of_department')
        start_year = request.POST.get('start_year')
        students_capacity = request.POST.get('students_capacity')

        Department.objects.create(
            department_id=department_id,
            name=name,
            head_of_department=head_of_department,
            start_year=start_year,
            students_capacity=students_capacity
        )
        messages.success(request, 'Department added successfully')
        return redirect('department_list')
    return render(request, 'departments/add-department.html')

@role_required(['admin'])
def edit_department(request, department_id):
    department = Department.objects.filter(department_id=department_id).first()
    if request.method == 'POST':
        department.name = request.POST.get('name')
        department.head_of_department = request.POST.get('head_of_department')
        department.start_year = request.POST.get('start_year')
        department.students_capacity = request.POST.get('students_capacity')
        department.save()
        messages.success(request, 'Department updated successfully')
        return redirect('department_list')
    
    context = {'department': department}
    return render(request, 'departments/edit-department.html', context)

@role_required(['admin', 'teacher', 'student'])
def view_department(request, department_id):
    department = Department.objects.filter(department_id=department_id).first()
    context = {'department': department}
    return render(request, 'departments/department-details.html', context)

@role_required(['admin'])
def delete_department(request, department_id):
    department = Department.objects.filter(department_id=department_id).first()
    if department:
        department.delete()
        messages.success(request, 'Department deleted successfully')
    return redirect('department_list')

# --- Teachers ---
@role_required(['admin', 'teacher', 'student'])
def teacher_list(request):
    teachers = Teacher.objects.all()
    context = {'teacher_list': teachers}
    return render(request, 'teachers/teachers.html', context)

@role_required(['admin'])
def add_teacher(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        teacher_id = request.POST.get('teacher_id')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        experience = request.POST.get('experience')
        email = request.POST.get('email')
        address = request.POST.get('address')
        avatar = request.FILES.get('avatar')
        
        department_name = request.POST.get('department_name')
        department = Department.objects.filter(name=department_name).first()

        Teacher.objects.create(
            first_name=first_name,
            last_name=last_name,
            teacher_id=teacher_id,
            gender=gender,
            date_of_birth=date_of_birth,
            joining_date=joining_date,
            mobile_number=mobile_number,
            experience=experience,
            email=email,
            address=address,
            avatar=avatar,
            department=department
        )
        messages.success(request, 'Teacher added successfully')
        return redirect('teacher_list')
    
    departments = Department.objects.all()
    context = {'departments': departments}
    return render(request, 'teachers/add-teacher.html', context)

@role_required(['admin'])
def edit_teacher(request, teacher_id):
    teacher = Teacher.objects.filter(teacher_id=teacher_id).first()
    if request.method == 'POST':
        teacher.first_name = request.POST.get('first_name')
        teacher.last_name = request.POST.get('last_name')
        teacher.gender = request.POST.get('gender')
        teacher.date_of_birth = request.POST.get('date_of_birth')
        teacher.joining_date = request.POST.get('joining_date')
        teacher.mobile_number = request.POST.get('mobile_number')
        teacher.experience = request.POST.get('experience')
        teacher.email = request.POST.get('email')
        teacher.address = request.POST.get('address')
        if request.FILES.get('avatar'):
            teacher.avatar = request.FILES.get('avatar')
            
        department_name = request.POST.get('department_name')
        if department_name:
            department = Department.objects.filter(name=department_name).first()
            teacher.department = department

        teacher.save()
        messages.success(request, 'Teacher updated successfully')
        return redirect('teacher_list')
        
    departments = Department.objects.all()
    context = {'teacher': teacher, 'departments': departments}
    return render(request, 'teachers/edit-teacher.html', context)

@role_required(['admin'])
def view_teacher(request, teacher_id):
    teacher = Teacher.objects.filter(teacher_id=teacher_id).first()
    context = {'teacher': teacher}
    return render(request, 'teachers/teacher-details.html', context)

@role_required(['admin'])
def delete_teacher(request, teacher_id):
    teacher = Teacher.objects.filter(teacher_id=teacher_id).first()
    if teacher:
        teacher.delete()
        messages.success(request, 'Teacher deleted successfully')
    return redirect('teacher_list')

# --- Generic Redirects ---
@role_required(['admin', 'teacher', 'student'])
def department_view_generic(request):
    departments = Department.objects.all()
    return render(request, 'departments/select_department.html', {'departments': departments, 'action': 'view'})

@role_required(['admin'])
def department_edit_generic(request):
    departments = Department.objects.all()
    return render(request, 'departments/select_department.html', {'departments': departments, 'action': 'edit'})
    
@role_required(['admin'])
def teacher_view_generic(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers/select_teacher.html', {'teachers': teachers, 'action': 'view'})
    
@role_required(['admin'])
def teacher_edit_generic(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers/select_teacher.html', {'teachers': teachers, 'action': 'edit'})

@role_required(['teacher'])
def teacher_dashboard(request):
    return render(request, 'teachers/teacher-dashboard.html')