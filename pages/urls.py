from django.urls import path
from django.urls import re_path
from django.contrib.auth import views as auth_views

from . import views
app_name = 'pages'
urlpatterns = [   
    path('dashboard',view=views.pagedashboard, name='pagedashboard'),
    path('create',view=views.create, name='create'),

    path('store_page',view=views.store_page, name='store_page'),  
    path('set_followpage',view=views.set_followpage, name='set_followpage'),  
    path('detail/<str:page_id>',view=views.view_page_detail, name='view_page_detail'),  

    path('set_page_like',view=views.set_page_like, name='set_page_like'),     
        
]