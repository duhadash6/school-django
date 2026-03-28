import re

def update_faculty():
    with open('faculty/views.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Create admin_dashboard and index
    old_index = """@role_required(['admin'])
def index(request):
    return render(request, 'Home/index.html')"""
    
    new_index = """@role_required(['admin'])
def admin_dashboard(request):
    return render(request, 'Home/index.html')

@role_required(['admin', 'teacher', 'student'])
def index(request):
    if getattr(request.user, 'is_admin', False):
        return redirect('admin_dashboard')
    elif getattr(request.user, 'is_teacher', False):
        return redirect('teacher_dashboard')
    elif getattr(request.user, 'is_student', False):
        return redirect('student_dashboard')
    return redirect('login')"""

    content = content.replace(old_index, new_index)

    # Departments
    content = content.replace("@role_required(['admin'])\ndef department_list", "@role_required(['admin', 'teacher', 'student'])\ndef department_list")
    content = content.replace("@role_required(['admin'])\ndef view_department", "@role_required(['admin', 'teacher', 'student'])\ndef view_department")
    content = content.replace("@role_required(['admin'])\ndef department_view_generic", "@role_required(['admin', 'teacher', 'student'])\ndef department_view_generic")

    # Teachers
    content = content.replace("@role_required(['admin'])\ndef teacher_list", "@role_required(['admin', 'teacher', 'student'])\ndef teacher_list")
    content = content.replace("@role_required(['admin'])\ndef view_teacher", "@role_required(['admin', 'teacher', 'student'])\ndef view_teacher")
    content = content.replace("@role_required(['admin'])\ndef teacher_view_generic", "@role_required(['admin', 'teacher', 'student'])\ndef teacher_view_generic")
    
    content = content.replace("@role_required(['admin'])\ndef add_teacher", "@role_required(['admin', 'teacher'])\ndef add_teacher")
    content = content.replace("@role_required(['admin'])\ndef edit_teacher", "@role_required(['admin', 'teacher'])\ndef edit_teacher")
    content = content.replace("@role_required(['admin'])\ndef delete_teacher", "@role_required(['admin', 'teacher'])\ndef delete_teacher")
    content = content.replace("@role_required(['admin'])\ndef teacher_edit_generic", "@role_required(['admin', 'teacher'])\ndef teacher_edit_generic")

    with open('faculty/views.py', 'w', encoding='utf-8') as f:
        f.write(content)

def update_student():
    with open('student/views.py', 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace("@role_required(['admin', 'teacher'])\ndef student_list", "@role_required(['admin', 'teacher', 'student'])\ndef student_list")
    content = content.replace("@role_required(['admin', 'teacher'])\ndef view_student", "@role_required(['admin', 'teacher', 'student'])\ndef view_student")
    content = content.replace("@role_required(['admin', 'teacher'])\ndef student_view_generic", "@role_required(['admin', 'teacher', 'student'])\ndef student_view_generic")
    
    content = content.replace("@role_required(['admin', 'teacher'])\ndef add_student", "@role_required(['admin'])\ndef add_student")
    content = content.replace("@role_required(['admin', 'teacher'])\ndef edit_student", "@role_required(['admin'])\ndef edit_student")
    content = content.replace("@role_required(['admin', 'teacher'])\ndef delete_student", "@role_required(['admin'])\ndef delete_student")
    content = content.replace("@role_required(['admin', 'teacher'])\ndef student_edit_generic", "@role_required(['admin'])\ndef student_edit_generic")

    with open('student/views.py', 'w', encoding='utf-8') as f:
        f.write(content)

update_faculty()
update_student()
print("Updates complete.")
