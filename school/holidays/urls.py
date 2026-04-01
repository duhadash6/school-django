from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.holiday_list, name='holiday_list'),
    path('add/', views.add_holiday, name='add_holiday'),
    path('edit/<str:holiday_id>/', views.edit_holiday, name='edit_holiday'),
    path('delete/<str:holiday_id>/', views.delete_holiday, name='delete_holiday'),
    path('calendar/', views.holiday_calendar, name='holiday_calendar'),
]