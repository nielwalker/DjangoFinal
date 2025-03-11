from django.contrib import admin
from django.urls import path, include
from lms import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),  # Home page

    # User Authentication
    path('user_registration/', views.user_registration, name="user_registration"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout_view, name="logout"),

    # Course Management
    path('course_info/', views.course_info, name="course_info"),
    path('course_details/<str:course_slug>/', views.course_details, name="course_details"),
    path('course_basic_details/<str:course_slug>/', views.course_basic_details, name="course_basic_details"),

    # Trainer Management
    path('trainer_registration/', views.trainer_registration, name="trainer_registration"),
    path('learn_as_trainer/', views.learn_as_trainer, name="learn_as_trainer"),

    # Include LMS URLs
    path('lms/', include(('lms.urls', 'lms'), namespace='lms')),  # Include LMS app's URLs
    path('', views.home, name='home'),
    path('user_registration/', views.user_registration, name='user_registration'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('course_info/', views.course_info, name='course_info'),
    path('course_details/<slug:course_slug>/', views.course_details, name='course_details'),
    path('course_basic_details/<slug:course_slug>/', views.course_basic_details, name='course_basic_details'),
    path('trainer_registration/', views.trainer_registration, name='trainer_registration'),
    path('learn_as_trainer/', views.learn_as_trainer, name='learn_as_trainer'),
    path('register_as_trainer/', views.register_as_trainer, name='register_as_trainer'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Ensure this URL pattern is included
]
