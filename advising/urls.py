#own create file

from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Advising, name='advising'),
    path('delete/', views.deleteTaken, name='delete'),
    path('advisingbyfaculty/', views.AdvisingByFaculty, name='advising_by_faculty'),
    path('coursetaken/', views.CourseTake, name='course_taken'),
    path('deletebyfaculty/', views.deleteByFaculty, name='delete_by_faculty'),
    path('facultyschedule/', views.FacultySchedule, name='f_schedule'),
]
