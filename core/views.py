from urllib import request

from django.shortcuts import render, redirect, get_object_or_404  # type: ignore[import]
from .models import Student
from django.contrib.auth.decorators import login_required  # type: ignore[import]
from django.core.paginator import Paginator

def home(request):
    if request.method == "POST":
        name=request.POST["name"]
        roll=int(request.POST["roll"])
        subject=request.POST["subject"]
        marks=int(request.POST["marks"])
        
        students=Student.objects.create(name=name, roll=roll, subject=subject, marks=marks)

        return redirect('core_home')
    
    students = Student.objects.all()
    return render(request, 'core/home.html', {'students': students})


#@login_required

def dashboard(request):
    students = Student.objects.all().order_by("id")

    search = request.GET.get("search", "")
    if search:
        students = students.filter(name__icontains=search)

    # Get unique student roll numbers
    student_rolls = students.values_list(
        "roll", flat=True
    ).distinct().order_by("roll")

    # Paginate students, not subject records
    paginator = Paginator(student_rolls, 1)
    page_obj = paginator.get_page(request.GET.get("page"))

    # Get ALL subject records for students on this page
    page_students = Student.objects.filter(
        roll__in=page_obj.object_list
    ).order_by("id")

    return render(request, "core/dashboard.html", {
        "students": page_students,
        "page_obj": page_obj,
        "search": search,
    })
    

def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('dashboard')

def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    
    if request.method == "POST":
        student.name=request.POST["name"]
        student.roll=int(request.POST["roll"])
        student.marks=int(request.POST["marks"])
        student.subject=request.POST["subject"]
        student.save()
        return redirect('dashboard')
    return render(request, 'core/edit.html', {'student': student})

def student_detail(request,id):

    student = get_object_or_404(Student,id=id)

    return render(request,"student_detail.html",
        {
            "student": student
        }
    )
    