from .models import Course
from django.contrib.auth.models import User
from django.shortcuts import render , redirect
from django.shortcuts import get_object_or_404 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CourseForm
from django.contrib import messages

def home(request):
    
    courses = Course.objects.all()
    context = {
        "courses" : courses
    }
    return render(request, 'courses/home.html',context) 

def course_detail(request, id):

    course = get_object_or_404(Course, id=id)

    context = {
        "course": course
    }

    return render(
        request,
        "courses/course_detail.html",
        context
    )

@login_required
def add_course(request):

    if request.method == "POST":

        form = CourseForm(request.POST)
        # from will automatically handle the validation and creation of the course object based on the form data. It will also handle the user association.
        # Course.objects.create(
        #     title=title,
        #     description=description,
        #     price=price ,
        #     user=request.user ,
        # )
        if form.is_valid():

            course = form.save(commit=False) # we are not saving the form yet, we are just creating an instance of the model

            course.user = request.user

            course.save() # now we are saving the form

            messages.success(request,"Course Added Successfully")

            return redirect('/')
        
    else:

        form = CourseForm()

    context = {
        'form': form
        }

    return render(request, "courses/add_course.html",context)

# @login_required
# def edit_course(request, id):   this is without using forms, we can use forms to make it easier and cleaner

#     course = get_object_or_404(Course, id=id)  

#     if request.method == "POST":

#         course.title = request.POST.get("title")
#         course.description = request.POST.get("description")
#         course.price = request.POST.get("price")

#         course.save()

#         return redirect('/')

#     context = {
#         "course": course
#     }

#     return render(
#         request,
#         "courses/edit_course.html",
#         context)

@login_required
def edit_course(request, id):  # using forms to make it easier and cleaner

    course = get_object_or_404(
        Course,
        id=id
    )

    if request.user != course.user:
        return redirect('/')

    if request.method == "POST":

        form = CourseForm(
            request.POST,
            instance=course
        )

        if form.is_valid():

            form.save() # here we didnt write form.save(commit=False) because we are not creating a new course, we are updating an existing course, so we dont need to set the user again
 
            messages.success(request,"Course Updated Successfully")

            return redirect('/')

    else:

        form = CourseForm(
            instance=course
        )

    context = {
        'form': form
    }

    return render(
        request,
        'courses/edit_course.html',
        context
    )

@login_required
def delete_course(request, id):

    course = get_object_or_404(
        Course,
        id=id
    )

    if request.user != course.user:
        return redirect('/')

    if request.method == "POST":

        course.delete()
        messages.success(request,"Course Deleted Successfully")

        return redirect('/')

    return render(
        request,
        "courses/delete_course.html",
        {"course": course})

def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:

            User.objects.create_user(
                username=username,
                password=password
            )

            return redirect('/')

    return render(
        request,
        'courses/register.html'
    )

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(request,"Login Successful")

            return redirect('/')

    return render(
        request,
        'courses/login.html')

def logout_view(request):

    logout(request)

    messages.success(request,"Logout Successful")

    return redirect('/')

# course = Course.objects.get(id=id)

@login_required
def dashboard(request):

    courses = request.user.course_set.all()

    context = {
        "courses": courses
    }

    return render(
        request,
        "courses/dashboard.html",
        context)

# if request.user != course.user:
#     return HttpResponse("You are not allowed to edit this course")