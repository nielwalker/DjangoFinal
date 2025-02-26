from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.forms import inlineformset_factory, modelformset_factory
from django.http import Http404, HttpResponseRedirect, \
HttpResponse, HttpResponseForbidden
from django.urls import reverse

def course_info(request):
    user = request.user

    if request.method == 'POST':
        form = CourseInfoForm(request.POST, request.FILES)
        if form.is_valid():  # Form cleaning & Validation
            form = CourseInfoForm(request.POST, request.FILES)

            new_course = form.save()
            course_info = CourseInfo.objects.filter(id=new_course.id)

            for info in course_info:
                return HttpResponseRedirect(reverse('lms:course_details', args=(info.slug,)))

    form = CourseInfoForm(initial={"user": user, })

    course_info = CourseInfo.objects.filter(user=user)
    course_details = CourseDetails.objects.filter(user=user)
    trainer_registration_details = TrainerRegistration.objects.filter(user=user)

    for details in trainer_registration_details:
        if details.status == True:
            context = {
                "form": form,
                "course_info": course_info,
                "course_details": course_details,
            }
            return render(request, 'lms/course_info.html', context)
        else:
            return render(request, 'lms/learn_as_trainer.html')

def course_details(request, course_slug):
    course_info = CourseInfo.objects.get(slug=course_slug)

    context = {
        "course_slug": course_slug,
        "course_info": course_info,
    }
    return render(request, 'lms/course_details.html', context)


def course_basic_details(request, course_slug):
    user = request.user
    course_info = CourseInfo.objects.get(slug=course_slug)

    if request.method == 'POST':
        form = CourseDetailsForm(request.POST, request.FILES)
        if form.is_valid():  # Form cleaning & Validation
            form = CourseDetailsForm(request.POST, request.FILES)
            form.save()
            # return HttpResponseRedirect('/')

    form = CourseDetailsForm(initial={'course_info': course_info, 'user': user, })

    context = {
        "course_slug": course_slug,
        "course_info": course_info,
        "form": form,
    }
    return render(request, 'lms/course_basic_details.html', context)

def home(request):
    return render(request, 'lms/home.html')

def user_registration(request):
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        user_name = request.POST.get("user_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if User.objects.filter(username=user_name).exists():
            messages.error(request, 'Username Taken')
            return redirect('lms:user_registration')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email Taken')
            return redirect('lms:user_registration')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('lms:user_registration')
        else:
            user = User.objects.create_user(
                username=user_name,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password1
            )
            user.save()
            messages.success(request, 'User registered successfully')
            return redirect('lms:login')
    else:
        return render(request, 'lms/user_registration.html')

def login(request):
    if request.method == 'POST':
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")

        user = auth.authenticate(username=user_name, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('lms:dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('lms:login')
    else:
        return render(request, 'lms/login.html')
                      
def logout(request):
    auth.logout(request)
    return redirect('/')

def trainer_registration(request):
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        user_name = request.POST.get("user_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('lms:trainer_registration')
        elif password1 == password2:
            if User.objects.filter(username=user_name).exists():
                messages.info(request, 'Username Taken')
                return redirect('lms:trainer_registration')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('lms:trainer_registration')
            else:
                user = User.objects.create_user(
                    username=user_name,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password1
                    user.is_staff = True
                    user.save()
                    trainer_registration = TrainerRegistration.objects.create(user=user, status=False)
                    return redirect('lms:login')
                )
        else:
            print('Passwords do not match')
            return redirect('lms:trainer_registration')
        return redirect('/')
    else:
        return render(request, 'lms/trainer_registration.html')

def learn_as_trainer(request):
    user = request.user
    trainer_registration = TrainerRegistration.objects.create(user=user, status=False)
    user_info = User.objects.filter(username=user.username)
    for info in user_info:
        if info.username:
            user.is_staff = True
            user.save()
    return render(request, 'lms/learn_as_trainer.html')
