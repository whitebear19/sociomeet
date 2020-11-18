from django.urls import path
from django.urls import re_path
from django.contrib.auth import views as auth_views

from . import views
app_name = 'account'
urlpatterns = [   
    path('dashboard',view=views.dashboard, name='dashboard'),
    path('check_register',view=views.check_register, name='check_register'),
    path('check_login',view=views.check_login, name='check_login'),
    path('trending',view=views.trending, name='trending'),

    path('',view=views.index, name='index'),
    path('logout',view=views.logout, name='logout'),
    path('profile',view=views.profile, name='profile'),
    path('editprofile',view=views.editprofile, name='editprofile'),  
    path('faq',view=views.faq, name='faq'),  
    path('terms',view=views.terms, name='terms'),  
    path('privacy',view=views.privacy, name='privacy'),  
    path('company_profile',view=views.company_profile, name='company_profile'), 
    path('messages',view=views.messages, name='messages'),     
   
    path('user/<str:username>',view=views.view_user_profile, name='view_user_profile'),     
    path('userposts',view=views.userposts, name='userposts'),     
    path('viewconnections/<str:which>',view=views.viewconnections, name='viewconnections'),  
    path('viewconnections',view=views.viewconnection, name='viewconnection'),  
    
         

    path('notifications',view=views.notifications, name='notifications'),    
    path('upload_avatar',view=views.upload_avatar, name='upload_avatar'), 
    path('store_aboutme',view=views.store_aboutme, name='store_aboutme'), 
    path('store_sociallink',view=views.store_sociallink, name='store_sociallink'), 
    path('store_basicinfo',view=views.store_basicinfo, name='store_basicinfo'),

    path('set_follow',view=views.set_follow, name='set_follow'),  
    path('store_experience',view=views.store_experience, name='store_experience'),  
    path('delete_experience',view=views.delete_experience, name='delete_experience'),  
    path('store_education',view=views.store_education, name='store_education'),  
    path('delete_education',view=views.delete_education, name='delete_education'),  
    path('attachmentsview',view=views.attachmentsview, name='attachmentsview'),  
    path('get_attachs',view=views.get_attachs, name='get_attachs'),
    path('get_searchresult',view=views.get_searchresult, name='get_searchresult'),
    
    path('get_UserForInvite',view=views.get_UserForInvite, name='get_UserForInvite'),

    path('get_new_notification',view=views.get_new_notification, name='get_new_notification'),
    path('get_notification',view=views.get_notification, name='get_notification'),
    path('notification_set_read',view=views.notification_set_read, name='notification_set_read'),
    
    path('delete_notification',view=views.delete_notification, name='delete_notification'),
    
]