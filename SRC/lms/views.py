from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .forms import CourseInfoForm, CourseDetailsForm
from .models import CourseInfo, CourseDetails, TrainerRegistration
from django.http import HttpResponseRedirect
from django.urls import reverse

def course_info(request):
    user = request.user

    if request.method == 'POST':
        form = CourseInfoForm(request.POST, request.FILES)
        if form.is_valid():  # Form cleaning & Validation
            new_course = form.save()
            return HttpResponseRedirect(reverse('course_details.html', args=(new_course.slug,)))

    form = CourseInfoForm(initial={"user": user})

    course_info = CourseInfo.objects.filter(user=user)
    course_details = CourseDetails.objects.filter(user=user)
    trainer_registration_details = TrainerRegistration.objects.filter(user=user)

    for details in trainer_registration_details:
        if details.status:
            context = {
                "form": form,
                "course_info": course_info,
                "course_details": course_details,
            }
            return render(request, 'course_info.html', context)
        else:
            return render(request, 'learn_as_trainer.html')

def course_details(request, course_slug):
    course_info = CourseInfo.objects.get(slug=course_slug)

    context = {
        "course_slug": course_slug,
        "course_info": course_info,
    }
    return render(request, 'course_details.html', context)

def course_basic_details(request, course_slug):
    user = request.user
    course_info = CourseInfo.objects.get(slug=course_slug)

    if request.method == 'POST':
        form = CourseDetailsForm(request.POST, request.FILES)
        if form.is_valid():  # Form cleaning & Validation
            form.save()
            return HttpResponseRedirect(reverse('course_details.html', args=(course_slug,)))

    form = CourseDetailsForm(initial={'course_info': course_info, 'user': user})

    context = {
        "course_slug": course_slug,
        "course_info": course_info,
        "form": form,
    }
    return render(request, 'course_basic_details.html', context)

def home(request):
    return render(request, 'home.html')

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
            return redirect('user_registration.html')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email Taken')
            return redirect('user_registration.html')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('user_registration.html')
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
            return redirect('login.html')
    else:
        return render(request, 'user_registration.html')

def login(request):
    if request.method == 'POST':
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")

        user = auth.authenticate(username=user_name, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard.html')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login.html')
    else:
        return render(request, 'login.html')

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
            return redirect('trainer_registration.html')
        elif User.objects.filter(username=user_name).exists():
            messages.info(request, 'Username Taken')
            return redirect('trainer_registration.html')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email Taken')
            return redirect('trainer_registration.html')
        else:
            user = User.objects.create_user(
                username=user_name,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password1
            )
            user.is_staff = True
            user.save()
            TrainerRegistration.objects.create(user=user, status=False)
            return redirect('login.html')
    else:
        return render(request, 'trainer_registration.html')

def learn_as_trainer(request):
    user = request.user
    TrainerRegistration.objects.create(user=user, status=False)
    user.is_staff = True
    user.save()
    return render(request, 'learn_as_trainer.html')
