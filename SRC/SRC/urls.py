"""
URL configuration for SRC project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from lms.templates import *
from lms.views import *

app_name = 'lms'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name="home"),
    path('user_registration/', user_registration, name="user_registration"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('course_info/', course_info, name="course_info"),
    path('course_details/<str:course_slug>/', course_details, name="course_details"),
    path('course_basic_details/<str:course_slug>/', course_basic_details, name="course_basic_details"),
    path('trainer_registration/', trainer_registration, name="trainer_registration"),
    path('learn_as_trainer/', learn_as_trainer, name="learn_as_trainer"),
]
