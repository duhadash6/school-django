from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from django.template import TemplateDoesNotExist
from .models import Teacher, Department

def index(request):
    return render(request, 'Home/index.html')

def inbox(request):
    return render(request, 'inbox.html')

def profile(request):
    return render(request, 'profile.html')

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
def department_list(request):
    departments = Department.objects.all()
    context = {'department_list': departments}
    return render(request, 'departments/departments.html', context)

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

def view_department(request, department_id):
    department = Department.objects.filter(department_id=department_id).first()
    context = {'department': department}
    return render(request, 'departments/department-details.html', context)

def delete_department(request, department_id):
    department = Department.objects.filter(department_id=department_id).first()
    if department:
        department.delete()
        messages.success(request, 'Department deleted successfully')
    return redirect('department_list')

# --- Teachers ---
def teacher_list(request):
    teachers = Teacher.objects.all()
    context = {'teacher_list': teachers}
    return render(request, 'teachers/teachers.html', context)

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

def view_teacher(request, teacher_id):
    teacher = Teacher.objects.filter(teacher_id=teacher_id).first()
    context = {'teacher': teacher}
    return render(request, 'teachers/teacher-details.html', context)

def delete_teacher(request, teacher_id):
    teacher = Teacher.objects.filter(teacher_id=teacher_id).first()
    if teacher:
        teacher.delete()
        messages.success(request, 'Teacher deleted successfully')
    return redirect('teacher_list')

# --- Generic Redirects ---
def department_view_generic(request):
    first_dept = Department.objects.first()
    if first_dept: return redirect('view_department', department_id=first_dept.department_id)
    return redirect('department_list')

def department_edit_generic(request):
    first_dept = Department.objects.first()
    if first_dept: return redirect('edit_department', department_id=first_dept.department_id)
    return redirect('department_list')
    
def teacher_view_generic(request):
    first_teacher = Teacher.objects.first()
    if first_teacher: return redirect('view_teacher', teacher_id=first_teacher.teacher_id)
    return redirect('teacher_list')
    
def teacher_edit_generic(request):
    first_teacher = Teacher.objects.first()
    if first_teacher: return redirect('edit_teacher', teacher_id=first_teacher.teacher_id)
    return redirect('teacher_list')

def teacher_dashboard(request):
    return render(request, 'teachers/teacher-dashboard.html')