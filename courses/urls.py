from django.urls import path
from .views import (home , course_detail , add_course , edit_course ,
                     delete_course , register, login_view, logout_view, dashboard)
urlpatterns = [
    path('', home),

    path(
        'course/<int:id>/',
          course_detail,
          name = 'course_detail'),

    path(
        'add_course/',
        add_course,
        name='add_course'),

    path(
    'course/<int:id>/edit/',
    edit_course,
    name='edit_course'),

    path(
    'course/<int:id>/delete/',
    delete_course,
    name='delete_course'),

    path(
    'register/',
    register,
    name='register'),

    path(
    'login/',
    login_view,
    name='login'),

    path(
    'logout/',
    logout_view,
    name='logout'),

    path(
    'dashboard/',
    dashboard,
    name='dashboard')

]