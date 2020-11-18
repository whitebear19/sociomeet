
from django.urls import path
from django.urls import re_path
from django.contrib.auth import views as auth_views

from . import views
app_name = 'jobs'
urlpatterns = [         
    path('dashboard',view=views.jobdashboard, name='jobdashboard'),
    path('userjobs',view=views.userjobs, name='userjobs'),
    path('create',view=views.create, name='create'),
    path('detail/<str:job_id>',view=views.view_job_detail, name='view_job_detail'), 
    
    path('store_job',view=views.store_job, name='store_job'), 
    path('get_content_list',view=views.get_content_list, name='get_content_list'),  
    path('get_postcode',view=views.get_postcode, name='get_postcode'),
]