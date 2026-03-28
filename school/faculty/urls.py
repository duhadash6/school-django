from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student/', include('student.urls')),
    
    # Departments
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.add_department, name='add_department'),
    path('departments/edit/<str:department_id>/', views.edit_department, name='edit_department'),
    path('departments/view/<str:department_id>/', views.view_department, name='view_department'),
    path('departments/delete/<str:department_id>/', views.delete_department, name='delete_department'),
    
    # Teachers
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/add/', views.add_teacher, name='add_teacher'),
    path('teachers/edit/<str:teacher_id>/', views.edit_teacher, name='edit_teacher'),
    path('teachers/view/<str:teacher_id>/', views.view_teacher, name='view_teacher'),
    path('teachers/delete/<str:teacher_id>/', views.delete_teacher, name='delete_teacher'),
    
    # Generic Redirects
    path('departments/view/', views.department_view_generic, name='department_view_generic'),
    path('departments/edit/', views.department_edit_generic, name='department_edit_generic'),
    path('teachers/view/', views.teacher_view_generic, name='teacher_view_generic'),
    path('teachers/edit/', views.teacher_edit_generic, name='teacher_edit_generic'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
]