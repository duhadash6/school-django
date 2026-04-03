from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser

def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST.get('role') 
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered. Please log in or use a different email.')
            return render(request, 'Home/register.html')

        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )

        if role == 'student':
            user.is_student = True
        elif role == 'teacher':
            user.is_teacher = True
        elif role == 'admin':
            user.is_admin = True

        user.save()

        # Auto-create a Student profile when signing up as a student
        if user.is_student:
            from student.models import Student, Parent
            parent, _ = Parent.objects.get_or_create(
                father_name='N/A',
                mother_name='N/A',
                defaults={
                    'father_mobile': '', 'father_email': '',
                    'father_occupation': '',
                    'mother_mobile': '', 'mother_email': '',
                    'mother_occupation': '',
                    'present_address': 'N/A',
                    'permanent_address': 'N/A',
                }
            )
            from datetime import date
            Student.objects.create(
                first_name=first_name,
                last_name=last_name,
                student_id=f"STU-{user.id}",
                gender='Male',
                date_of_birth=date(2000, 1, 1),
                student_class='N/A',
                joining_date=date.today(),
                mobile_number='',
                admission_number=f"ADM-{user.id}",
                section='N/A',
                parent=parent,
            )

        login(request, user)
        messages.success(request, 'Signup successful!')
        if user.is_admin:
            return redirect('index')
        elif user.is_teacher:
            return redirect('teacher_dashboard')
        elif user.is_student:
            return redirect('student_dashboard')
        return redirect('login')

    return render(request, 'Home/register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            if user.is_admin:
                return redirect('index')
            elif user.is_teacher:
                return redirect('teacher_dashboard')
            elif user.is_student:
                return redirect('student_dashboard')
            else:
                return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')
            
    return render(request, 'Home/login.html')


def logout_view(request):
    # Consommer les anciens messages pour qu'ils ne s'empilent pas (ex: "Login successful!")
    list(messages.get_messages(request))
    
    logout(request)
    messages.success(request, 'Logged out successfully. Please log in to continue.')
    return redirect('login')


def forgot_password_view(request):
    return render(request, 'Home/forgotpassword.html')

def reset_password_view(request, token):
    return render(request, 'Home/resetpassword.html', {'token': token})