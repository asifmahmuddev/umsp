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
    path('studentlist/', views.StudentListView, name='student_list'),
    path('facultysignup/', FacultySignUpView.as_view(), name='faculty_signup'),
    path('facultylist/', views.FacultyListView, name='faculty_list'),
    path('department/', views.DeptView, name='department'),
    path('departmentlist/', views.DepartmentListView, name='department_list'),
    path('semester/', views.CreateSemesterView, name='create_semester'),
    path('semesterlist/', views.SemesterListView, name='semester_list'),
    path('courselist/', views.CourseListView, name='course_list'),
    path('register_course/', views.CreateCourseView.as_view(), name='register_course'),
    path('assign_course/', views.AssignCourseView, name='assign_course'),
    path('assigned_course_list/', views.AssignedCourseListView, name='assigned_course_list'),
    path('schedule/', views.Schedule, name='schedule'),
]
