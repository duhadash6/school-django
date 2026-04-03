from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
from .models import Subject, Exam, Enrollment, ExamResult, Timetable
from .forms import SubjectForm
from django.db.models import Q
from .forms import ExamForm, TimetableForm
from django.contrib.auth.decorators import login_required

@login_required
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subjects/subjects.html', {'subjects': subjects})

@login_required
def add_subject(request):
    if getattr(request.user, 'is_student', False):
        return render(request, 'Home/error_403.html')
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'subjects/add-subject.html', {'form': form})

@login_required
def edit_subject(request, subject_id):
    if getattr(request.user, 'is_student', False):
        return render(request, 'Home/error_403.html')
    subject = get_object_or_404(Subject, subject_id=subject_id)
    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm(instance=subject)
        
    return render(request, 'subjects/edit-subject.html', {'form': form, 'subject': subject})


@login_required
def delete_subject(request, subject_id):
    if getattr(request.user, 'is_student', False):
        return render(request, 'Home/error_403.html')
    subject = get_object_or_404(Subject, subject_id=subject_id)
    subject.delete()
    return redirect('subject_list')


@login_required
def subject_edit_portal(request):
    if getattr(request.user, 'is_student', False):
        return render(request, 'Home/error_403.html')
    subjects = Subject.objects.all()
    search_query = request.GET.get('search')
    
    if search_query:
        subjects = subjects.filter(
            Q(name__icontains=search_query) | 
            Q(subject_id__icontains=search_query)
        )
        
    return render(request, 'subjects/edit-subject-portal.html', {
        'subjects': subjects, 
        'search_query': search_query
    })


@login_required
def exam_list(request):
    if getattr(request.user, 'is_student', False):
        return render(request, 'Home/error_403.html')
    exams = Exam.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        exams = exams.filter(
            Q(name__icontains=search_query) |
            Q(exam_id__icontains=search_query) |
            Q(subject__name__icontains=search_query)
        )


    return render(request, 'subjects/exam_list.html', {'exams': exams, 'search_query': search_query})

@login_required
def add_exam(request):
    if getattr(request.user, 'is_student', False):
        return render(request, 'Home/error_403.html')
    if request.method == "POST":
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exam_list')
    else:
        form = ExamForm()
    return render(request, 'subjects/add_exam.html', {'form': form})


@login_required
def edit_exam(request, exam_id):
    if getattr(request.user, 'is_student', False):
        return render(request, 'Home/error_403.html')
    exam = get_object_or_404(Exam, exam_id=exam_id)
    if request.method == "POST":
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            return redirect('exam_list')
    else:
        form = ExamForm(instance=exam)
        
    return render(request, 'subjects/edit_exam.html', {'form': form, 'exam': exam})

@login_required
def delete_exam(request, exam_id):
    if getattr(request.user, 'is_student', False):
        return render(request, 'Home/error_403.html')
    exam = get_object_or_404(Exam, exam_id=exam_id)
    exam.delete()
    return redirect('exam_list')

@login_required
def grade_exam(request, exam_id):
    if getattr(request.user, 'is_student', False):
        return render(request, 'Home/error_403.html')
        
    exam = get_object_or_404(Exam, exam_id=exam_id)
    subject = exam.subject
    
    enrollments = Enrollment.objects.filter(subject=subject).select_related('student')
    students = [enrollment.student for enrollment in enrollments]
    
    if request.method == "POST":
        for student in students:
            marks_key = f"marks_{student.id}"
            comments_key = f"comments_{student.id}"
            
            marks = request.POST.get(marks_key)
            comments = request.POST.get(comments_key)
            
            if marks is not None and marks.strip() != '':
                ExamResult.objects.update_or_create(
                    student=student,
                    exam=exam,
                    defaults={
                        'marks_obtained': marks,
                        'comments': comments
                    }
                )
        return redirect('grade_exam', exam_id=exam.exam_id)
    
    results = ExamResult.objects.filter(exam=exam)
    results_dict = {result.student_id: result for result in results}
    
    student_data = []
    for student in students:
        result = results_dict.get(student.id)
        student_data.append({
            'student': student,
            'marks_obtained': result.marks_obtained if result else '',
            'comments': result.comments if result else ''
        })
        
    return render(request, 'subjects/grade_exam.html', {
        'exam': exam,
        'student_data': student_data
    })


@login_required
def my_exams(request):
    if not getattr(request.user, 'is_student', False):
        return render(request, 'subjects/my_grades.html', {'error': 'Only students can view their exams.'})
        
    enrolled_subject_ids = Enrollment.objects.filter(student=request.user).values_list('subject_id', flat=True)
    exams = Exam.objects.filter(subject_id__in=enrolled_subject_ids).order_by('exam_date', 'start_time').select_related('subject')
    
    results = ExamResult.objects.filter(student=request.user, exam__in=exams)
    results_map = {res.exam_id: res for res in results}
    
    exam_data = []
    for exam in exams:
        exam_data.append({
            'exam': exam,
            'result': results_map.get(exam.id)
        })
    
    return render(request, 'subjects/my_exams.html', {'exam_data': exam_data})

@login_required
def my_grades(request):
    if not getattr(request.user, 'is_student', False):
        return render(request, 'subjects/my_grades.html', {'error': 'Only students can view their grades.'})
        
    results = ExamResult.objects.filter(student=request.user).select_related('exam', 'exam__subject')
    return render(request, 'subjects/my_grades.html', {'results': results})

@login_required
def enroll_subjects(request):
    if not getattr(request.user, 'is_student', False):
        return render(request, 'subjects/list_enroll.html', {'error': 'Only students can enroll in courses.'})
    
    all_subjects = Subject.objects.select_related('department', 'teacher')
    
    enrolled_subject_ids = Enrollment.objects.filter(student=request.user).values_list('subject__id', flat=True)
    
    return render(request, 'subjects/list_enroll.html', {
        'all_subjects': all_subjects,
        'enrolled_subject_ids': enrolled_subject_ids
    })

@login_required
def enroll_subject(request, subject_id):
    if not getattr(request.user, 'is_student', False):
        return redirect('enroll_subjects')
        
    subject = get_object_or_404(Subject, subject_id=subject_id)
    
    Enrollment.objects.get_or_create(
        student=request.user,
        subject=subject
    )
    
    return redirect('enroll_subjects')


@login_required
def visual_timetable(request):
    timetables = Timetable.objects.select_related('subject')
    events = []
    
    min_hour = 8
    max_hour = 18
    
    for t in timetables:
        if t.start_time.hour < min_hour:
            min_hour = t.start_time.hour
        end_h = t.end_time.hour + (1 if t.end_time.minute > 0 else 0)
        if end_h > max_hour:
            max_hour = end_h
        
        events.append({
            'title': f"{t.subject.name} - Room {t.room_number}",
            'startTime': t.start_time.strftime('%H:%M:%S'),
            'endTime': t.end_time.strftime('%H:%M:%S'),
            'daysOfWeek': [int(t.day)],
        })
    
    slot_min = f"{max(min_hour - 1, 0):02d}:00:00"
    slot_max = f"{min(max_hour + 1, 24):02d}:00:00"
    
    events_json = json.dumps(events)
    return render(request, 'subjects/timetable.html', {
        'events_json': events_json,
        'slot_min': slot_min,
        'slot_max': slot_max,
    })

@login_required
def add_timetable(request):
    if getattr(request.user, 'is_student', False):
        return render(request, 'Home/error_403.html')
        
    if request.method == "POST":
        form = TimetableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('visual_timetable')
    else:
        form = TimetableForm()
    return render(request, 'subjects/add_timetable.html', {'form': form})

@login_required
def export_timetable_json(request):
    timetables = Timetable.objects.select_related('subject')
    data = []
    for t in timetables:
        data.append({
            'subject': t.subject.name,
            'subject_id': t.subject.subject_id,
            'day': t.get_day_display(),
            'day_number': int(t.day),
            'start_time': t.start_time.strftime('%H:%M'),
            'end_time': t.end_time.strftime('%H:%M'),
            'room_number': t.room_number,
        })
    response = JsonResponse(data, safe=False, json_dumps_params={'indent': 2})
    response['Content-Disposition'] = 'attachment; filename="timetable.json"'
    return response
