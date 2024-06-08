"""
URL configuration for process_scope project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from .views import (process_comp_per_country,index, calculate_harmonization_per_country, proces_page,
                    region_page, procesvalue_page, process_level3_percentage,
                    edit_process_value, update_process_value,
                    edit_region, update_region, add_region, create_region,add_region,
                    edit_process, update_process, add_process, create_process)

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('scope/', process_level3_percentage, name='process_comp_per_country'),
    path('har/', calculate_harmonization_per_country, name='calculate_harmonization_per_country'),
    path('value/', procesvalue_page, name='procesvalue_page'),
    path('proces/', proces_page, name='proces_page'),
    path('region/', region_page, name='region_page'),
    path('process/', process_level3_percentage, name='process_level3_percentage'),
    path('edit_process_value/<int:id>/', edit_process_value, name='edit_process_value'),
    path('update_process_value/', update_process_value, name='update_process_value'),
    path('edit_region/<int:id>/', edit_region, name='edit_region'),
    path('update_region/', update_region, name='update_region'),
    path('add_region/', add_region, name='add_region'),
    path('create_region/', create_region, name='create_region'),
    path('add_process/', add_process, name='add_process'),
    path('create_process/', create_process, name='create_process'),
    path('edit_process/<int:id>/', edit_process, name='edit_process'),
    path('update_process/', update_process, name='update_process'),


]

