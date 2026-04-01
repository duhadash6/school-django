from django.shortcuts import render, redirect, get_object_or_404
from .models import Holiday
from .forms import HolidayForm
import json

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


def edit_holiday(request, holiday_id):
    holiday = get_object_or_404(Holiday, holiday_id=holiday_id)
    if request.method == 'POST':
        form = HolidayForm(request.POST, instance=holiday)
        if form.is_valid():
            form.save()
            return redirect('holiday_list')
    else:
        form = HolidayForm(instance=holiday)
    return render(request, 'holidays/edit-holiday.html', {'form': form, 'holiday': holiday})

def delete_holiday(request, holiday_id):
    holiday = get_object_or_404(Holiday, holiday_id=holiday_id)
    holiday.delete()
    return redirect('holiday_list')


def holiday_calendar(request):
    holidays = Holiday.objects.all()
    holiday_events = []
    for holiday in holidays:
        holiday_events.append({
            'title': holiday.name,
            'start': holiday.start_date.strftime("%Y-%m-%d"),
            'end': holiday.end_date.strftime("%Y-%m-%d"),
            'backgroundColor': '#ffbc34', # PreSkool warning/yellow color
            'borderColor': '#ffbc34',
            'textColor': 'white',
        })
        
    # Convert Python dictionary to a JSON string
    events_json = json.dumps(holiday_events)
    
    return render(request, 'holidays/holiday_calendar.html', {'events_json': events_json})