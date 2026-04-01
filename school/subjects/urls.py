from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.subject_list, name='subject_list'),
    path('add/', views.add_subject, name='add_subject'),
    path('edit/<str:subject_id>/', views.edit_subject, name='edit_subject'),
    path('delete/<str:subject_id>/', views.delete_subject, name='delete_subject'),
    path('edit-portal/', views.subject_edit_portal, name='subject_edit_portal'),
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/add/', views.add_exam, name='add_exam'),
    path('exams/edit/<str:exam_id>/', views.edit_exam, name='edit_exam'),
    path('exams/delete/<str:exam_id>/', views.delete_exam, name='delete_exam'),
]