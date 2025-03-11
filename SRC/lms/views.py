from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from .forms import CourseInfoForm, CourseDetailsForm
from .models import CourseInfo, CourseDetails, TrainerRegistration
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import logging


logger = logging.getLogger(__name__)

@login_required
def logout_view(request):
    logger.info(f"User {request.user.username} has logged out.")
    auth.logout(request)
    return redirect('lms:home')

def course_info(request):
    user = request.user

    if request.method == 'POST':
        form = CourseInfoForm(request.POST, request.FILES)
        if form.is_valid():  # Form cleaning & Validation
            new_course = form.save()
            return HttpResponseRedirect(reverse('lms:course_details', args=[new_course.slug]))

    form = CourseInfoForm(initial={"user": user})

    course_info = CourseInfo.objects.filter(user=user)
    course_details = CourseDetails.objects.filter(user=user)
    trainer_registration_details = TrainerRegistration.objects.filter(user=user)

    for details in trainer_registration_details:
        if any(details.status for details in trainer_registration_details):
            context = {
                "form": form,
                "course_info": course_info,
                "course_details": course_details,
            }
            return render(request, 'lms/course_info.html', context)

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
            form.save()
            return HttpResponseRedirect(reverse('lms:course_details', args=[course_slug]))

    form = CourseDetailsForm(initial={'course_info': course_info, 'user': user})

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
            return render(request, 'lms/user_registration.html')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email Taken')
            return render(request, 'lms/user_registration.html')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'lms/user_registration.html')
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

def dashboard(request):
    total_users = User.objects.count()
    recent_users = User.objects.order_by('-date_joined')[:5]  # Get last 5 users

    context = {
        'total_users': total_users,
        'recent_users': recent_users,
    }
    return render(request, 'lms/dashboard.html', context)

def login(request):
    if request.method == 'POST':
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")

        user = auth.authenticate(username=user_name, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('lms:dashboard')  # Corrected redirect
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('lms:login')
    else:
        return render(request, 'lms/login.html')

def back_btn(request):
    return render(request, 'lms/home.html')

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
        elif User.objects.filter(username=user_name).exists():
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
            )
            user.is_staff = True
            user.save()
            TrainerRegistration.objects.create(user=user, status=False)
            return redirect('lms:login')
    else:
        return render(request, 'lms/trainer_registration.html')

def learn_as_trainer(request):
    user = request.user
    trainer, created = TrainerRegistration.objects.get_or_create(user=user)
    if created:
        trainer.status = False
        trainer.save()

    user.is_staff = True
    user.save()
    return render(request, 'lms/learn_as_trainer.html')

@login_required
def register_as_trainer(request):
    user = request.user
    if not user.is_staff:
        user.is_staff = True
        user.save()
        TrainerRegistration.objects.create(user=user, status=True)
        messages.success(request, 'You have been registered as a trainer.')
    else:
        messages.info(request, 'You are already registered as a trainer.')
    return redirect('lms:home')
