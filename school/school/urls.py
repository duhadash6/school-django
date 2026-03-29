from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('faculty.urls')),
    path('student/', include('student.urls')),
    path('authentication/', include('home_auth.urls')),
    path('subjects/', include('subjects.urls')),
    path('holidays/', include('holidays.urls')),
]