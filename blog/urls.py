from django.urls import path
from django.urls import re_path
from django.contrib.auth import views as auth_views

from . import views
app_name = 'blog'
urlpatterns = [               
    path('get_selected_post',view=views.get_selected_post, name='get_selected_post'),
    path('add_like',view=views.add_like, name='add_like'),  
    path('add_like_comment',view=views.add_like_comment, name='add_like_comment'),  
    path('add_like_reply',view=views.add_like_reply, name='add_like_reply'),
    path('delete_post',view=views.delete_post, name='delete_post'),
    path('delete_attach',view=views.delete_attach, name='delete_attach'),
    path('get_content_list',view=views.get_content_list, name='get_content_list'), 
    path('store_post',view=views.store_post, name='store_post'), 
    path('store_postattach',view=views.store_postattach, name='store_postattach'), 
    path('addcomment',view=views.addcomment, name='addcomment'), 
    path('addreply',view=views.addreply, name='addreply'),    
    path('deletecomment',view=views.deletecomment, name='deletecomment'), 
    path('deletereply',view=views.deletereply, name='deletereply'), 
    
    path('getcomments',view=views.getcomments, name='getcomments'), 
    path('getcomment',view=views.getcomment, name='getcomment'), 
    path('updatecomment',view=views.updatecomment, name='updatecomment'), 
    path('updatereply',view=views.updatereply, name='updatereply'), 
    
    path('getreplies',view=views.getreplies, name='getreplies'),
    path('getreply',view=views.getreply, name='getreply'),    
    path('set_private',view=views.set_private, name='set_private'), 
    path('set_view',view=views.set_view, name='set_view'), 

    path('store_gif',view=views.store_gif, name='store_gif'),    

    
]