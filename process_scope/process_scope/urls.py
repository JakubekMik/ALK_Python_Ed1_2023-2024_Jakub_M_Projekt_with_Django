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
from .views import process_comp_per_country,index, calculate_harmonization_per_country, proces_page, region_page, procesvalue_page, process_level3_percentage

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('scope/', process_level3_percentage, name='process_comp_per_country'),
    path('har/', calculate_harmonization_per_country, name='calculate_harmonization_per_country'),
    path('value/', procesvalue_page, name='procesvalue_page'),
    path('proces/', proces_page, name='proces_page'),
    path('region/', region_page, name='region_page'),
    path('process/', process_level3_percentage, name='process_level3_percentage'),

]
