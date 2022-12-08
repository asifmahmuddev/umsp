#own create file

from django.urls import path
from . import views
from .views import StudentSignUpView,FacultySignUpView
from django.contrib.auth import views as auth_view
urlpatterns = [
    path('', views.Homepage, name='home'),
    path('login/', auth_view.LoginView.as_view(template_name='home/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='home/logout.html'), name='logout'),
    path('profile/', views.Profile, name='profile'),
    path('studentsignup/', StudentSignUpView.as_view(), name='student_signup'),
    path('facultysignup/', FacultySignUpView.as_view(), name='faculty_signup'),
    path('department/', views.DeptView, name='department'),
    path('semester/', views.CreateSemesterView, name='create_semester'),
    path('advised_course/', views.AssignCourseView, name='advised_course'),
    path('schedule/', views.Schedule, name='schedule'),
]
