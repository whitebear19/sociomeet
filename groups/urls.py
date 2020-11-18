
from django.urls import path
from django.urls import re_path
from django.contrib.auth import views as auth_views

from . import views
app_name = 'groups'
urlpatterns = [         
    path('dashboard',view=views.groupdashboard, name='groupdashboard'),
    path('create',view=views.create, name='create'),



    path('store_group',view=views.store_group, name='store_group'),  
    path('set_followgroup',view=views.set_followgroup, name='set_followgroup'),  
    path('detail/<str:group_id>',view=views.view_group_detail, name='view_group_detail'), 

    path('set_group_like',view=views.set_group_like, name='set_group_like'),     
      

      
]