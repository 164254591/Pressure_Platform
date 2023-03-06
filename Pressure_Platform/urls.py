"""Pressure_Platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.views.generic import TemplateView

from MyApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html')),
    path('login_account/', login_account),
    path('register_account/', register_account),
    path('get_echarts_data/', get_echarts_data),
    path('get_projects/', get_projects),
    path('add_project/', add_project),
    path('delete_project/', delete_project),
    path('get_project_detail/', get_project_detail),
    path('save_project/', save_project),
    path('upload_script_file/', upload_script_file),
    path('get_script_list/', get_script_list),
    path('get_tasks/', get_tasks),
    path('add_tasks/', add_tasks),
    path('stop_task/', stop_task),

]
