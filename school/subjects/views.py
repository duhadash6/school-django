from django.shortcuts import render, redirect, get_object_or_404
from .models import Subject
from .forms import SubjectForm

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