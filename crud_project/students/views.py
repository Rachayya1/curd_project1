from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.contrib import messages
from django.core.paginator import Paginator

def student_list(request):
    query = request.GET.get('q', '')
    students = Student.objects.filter(name__icontains=query) if query else Student.objects.all()
    paginator = Paginator(students, 5)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'students/list.html', {'page_obj': page_obj, 'query': query})

def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully.")
            return redirect('student_list')
        else:
            messages.error(request, "Form has errors.")
    else:
        form = StudentForm()
    return render(request, 'students/form.html', {'form': form})

def student_update(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully.")
            return redirect('student_list')
        else:
            messages.error(request, "Form has errors.")
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/form.html', {'form': form})

def student_delete(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    messages.success(request, "Student deleted.")
    return redirect('student_list')
