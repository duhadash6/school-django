from django.shortcuts import render, redirect, get_object_or_404
from .models import Subject
from .forms import SubjectForm
from django.db.models import Q
from .models import Exam
from .forms import ExamForm

def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subjects/subjects.html', {'subjects': subjects})

def add_subject(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'subjects/add-subject.html', {'form': form})

def edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, subject_id=subject_id)
    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm(instance=subject)
        
    return render(request, 'subjects/edit-subject.html', {'form': form, 'subject': subject})


def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, subject_id=subject_id)
    subject.delete()
    return redirect('subject_list')


def subject_edit_portal(request):
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


def exam_list(request):
    exams = Exam.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        exams = exams.filter(
            Q(name__icontains=search_query) |
            Q(exam_id__icontains=search_query) |
            Q(subject__name__icontains=search_query)
        )


    return render(request, 'subjects/exam_list.html', {'exams': exams, 'search_query': search_query})

def add_exam(request):
    if request.method == "POST":
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exam_list')
    else:
        form = ExamForm()
    return render(request, 'subjects/add_exam.html', {'form': form})


def edit_exam(request, exam_id):
    exam = get_object_or_404(Exam, exam_id=exam_id)
    if request.method == "POST":
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            return redirect('exam_list')
    else:
        form = ExamForm(instance=exam)
        
    return render(request, 'subjects/edit_exam.html', {'form': form, 'exam': exam})

def delete_exam(request, exam_id):
    exam = get_object_or_404(Exam, exam_id=exam_id)
    exam.delete()
    return redirect('exam_list')
