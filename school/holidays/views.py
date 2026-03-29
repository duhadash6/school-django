from django.shortcuts import render, redirect
from .models import Holiday
from .forms import HolidayForm

def holiday_list(request):
    holidays = Holiday.objects.all()
    return render(request, 'holidays/holidays.html', {'holidays': holidays})

def add_holiday(request):
    if request.method == "POST":
        form = HolidayForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('holiday_list')
    else:
        form = HolidayForm()
    return render(request, 'holidays/add-holiday.html', {'form': form})