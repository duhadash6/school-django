from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('add/', views.add_student, name='add_student'),
    path('students/<str:student_id>/', views.view_student, name='view_student'),
    path('edit/<str:student_id>/', views.edit_student, name='edit_student'),
    path('delete/<str:student_id>/', views.delete_student, name='delete_student'),
    path('view-generic/', views.student_view_generic, name='student_view_generic'),
    path('edit-generic/', views.student_edit_generic, name='student_edit_generic'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
]