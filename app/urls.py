"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from app import views
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path(r"doctor/all", views.get_doctors, name="get_doctors"),
    path(r"calendar/appointments", views.get_appointments, name="get_appointments"),
    path(r"calendar/appointments/delete", views.delete_appointment, name="delete_appointment"),
    path(r"calendar/appointments/add", views.add_new_appointment, name="add_new_appointment")
]
