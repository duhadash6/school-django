from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.holiday_list, name='holiday_list'),
    path('add/', views.add_holiday, name='add_holiday'),
]