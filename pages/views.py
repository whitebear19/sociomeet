from django.shortcuts import render

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
import math
import requests
import time
import datetime
import json
import os 

from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy



from blog.models import Posts,Likes,Comments,PostAttach,LikesComment,Replies,LikesReply
from account.models import CustomUser,Follows,Experience,Education,Visiter,Notification
from chat.models import Room,Message

from account.views import get_client_ip,get_geolocation_for_ip,get_random_string,get_curuser,get_users,get_users_following,get_following,get_followers,get_different_time,get_date_str,get_time_str

from groups.models import Group,GroupToUserInvite,FollowsGroup
from pages.models import Page,PageToUserInvite,FollowsPage,LikePage,ViewsPage


import datetime
from datetime import timedelta
import random
import string
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from PIL import Image

def getpages(temppages,request,status):
    results = []
    user = request.user
    for item in temppages:
        data = {}
        data['id'] = item.id
        thisUser=CustomUser.objects.get(id=item.user_id)
        if thisUser.avatar:
            data['avatar'] = thisUser.avatar.url
        else:
            data['avatar'] = '/static/img/avatar.png'
        data['title'] = item.title
        data['followers'] = FollowsPage.objects.filter(page_id=item.id).count()
        data['likes'] = LikePage.objects.filter(page_id=item.id).count()
        data['posts'] = Posts.objects.filter(page_id=item.id).count()
        data['views'] = ViewsPage.objects.filter(page_id=item.id).count()
        if LikePage.objects.filter(user_id=user.id,page_id=item.id):
            data['liked'] = '1'
        else:
            data['liked'] = '0'
        if item.user_id == user.id:
            data['me'] = '1'
            data['followtxt'] = ''
        else:
            data['me'] = '0'
            if status == '2':
                data['followtxt'] = 'Follow'
            else:
                data['followtxt'] = 'Unfollow'
        results.append(data)
    return results

def pagedashboard(request):

    if not request.user.is_authenticated:
        return redirect('/login')
    user = request.user         
   
    users = []        
    users = get_users(request)   
    
    curuser = {}
    curuser = get_curuser(request,user.id)      
       
    userpages = []
    allpages = []
    followpages = []
    followpagesID = []
    followpagesIDtemp = FollowsPage.objects.filter(user_id=user.id)
    for item in followpagesIDtemp:
        followpagesID.append(item.page_id)
    
    mypagestemp = Page.objects.filter(user_id=user.id)
    allpagestemp = Page.objects.exclude(user_id=user.id).exclude(id__in=followpagesID)    
    followpagestemp = Page.objects.filter(id__in=followpagesID)

    status="0"
    userpages = getpages(mypagestemp,request,status)
    status="2"
    allpages = getpages(allpagestemp,request,status)
    status="1"
    followpages = getpages(followpagestemp,request,status)

    
    return render(request,'pages/dashboard.html',{'users':users,'curuser':curuser,'userpages':userpages,'allpages':allpages,'followpages':followpages}) 

def create(request):

    user = request.user 
    users = CustomUser.objects.exclude(id=user.id)
    return render(request,'pages/create.html',{'users':users}) 

def view_page_detail(request,page_id):

    user = request.user 
    cur_page = {}
    cur_temp = Page.objects.get(id=page_id)
    cur_page['id'] = cur_temp.id
    if cur_temp.avatar:
        cur_page['back'] = cur_temp.avatar.url
    else:
        cur_page['back'] = '/static/img/no_banner.png'
    cur_page['title'] = cur_temp.title
    

    cur_page['followers'] = FollowsPage.objects.filter(page_id=page_id).count()
    cur_page['likes'] = LikePage.objects.filter(page_id=page_id).count()    
    cur_page['posts'] = Posts.objects.filter(page_id=page_id).count()
    cur_page['views'] = ViewsPage.objects.filter(page_id=page_id).count()

       
    if LikePage.objects.filter(user_id=user.id,page_id=page_id):
        cur_page['liked'] = '1'
    else:
        cur_page['liked'] = '0'



    if cur_temp.user_id == user.id:
        cur_page['me'] = '1'
        cur_page['followed'] = '0'
    else:
        cur_page['me'] = '0'
        if FollowsPage.objects.filter(page_id=cur_temp.id,user_id=user.id):
            cur_page['followed'] = '1'
        else:
            cur_page['followed'] = '0'
    this_user = CustomUser.objects.get(id=cur_temp.user_id)
    if this_user.avatar:
        cur_page['avatar'] = this_user.avatar.url
    else:
        cur_page['avatar'] = '/static/img/avatar.png'

    users = CustomUser.objects.exclude(id=user.id)

    if ViewsPage.objects.filter(user_id=user.id,page_id=page_id):
        pass
    else:
        row = ViewsPage(user_id=user.id,page_id=page_id)
        row.save()

    allpages = []    
    followpagesID = []
    followpagesIDtemp = FollowsPage.objects.filter(user_id=user.id)
    for item in followpagesIDtemp:
        followpagesID.append(item.page_id)
        
    allpagestemp = Page.objects.exclude(user_id=user.id).exclude(id__in=followpagesID)    
    followpagestemp = Page.objects.filter(id__in=followpagesID)   
    status = '2'  
    allpages = getpages(allpagestemp,request,status)  

    return render(request,'pages/details.html',{'users':users,'cur_page':cur_page,'pages':allpages}) 


# ----------------ajax_part------------------------
def store_page(request):
    try:
        user = request.user
        title = request.POST.get('title') 
        invitetype = request.POST.get('invitetype') 
        row = Page(title=title,user_id=user.id,avatar=request.FILES.get('attach'))        
        row.save()
        page_id = row.id
        if(invitetype=='1'):
            usertemp = Follows.objects.filter(whom=user.id)            
            if usertemp:
                for item in usertemp:
                    invite = PageToUserInvite(page_id=page_id,user_id=item.who,)
                    invite.save()
        else:
            users_id = request.POST.get('users')
            if users_id:
                users_id = users_id.split(",")    
                for item in users_id:
                    invite = PageToUserInvite(page_id=page_id,user_id=item,)
                    invite.save()

        subject = 'New page "'+ title + '" created successfully.'  
        body = 'Your page is created successfully. Invite people to get more response, likes to your page posts.'
        row_noti = Notification(user_id=user.id,subject=subject,body=body)
        row_noti.save()

        data = True
        return JsonResponse({'results':data,'id':page_id})
    except:
        return JsonResponse({'results':False})

def set_followpage(request):
    try:
        user = request.user
        id = request.POST.get('id') 
        if FollowsPage.objects.filter(page_id=id,user_id=user.id):
            FollowsPage.objects.get(page_id=id,user_id=user.id).delete()
        else: 
            if Page.objects.filter(id=id,user_id=user.id):
                pass
            else:
                row = FollowsPage(page_id=id,user_id=user.id)        
                row.save()

                thisPage = Page.objects.get(id=id)
                subject = user.first_name + ' ' + user.last_name + ' started following your page ' + thisPage.title
                body = ''
                row_noti = Notification(user_id=thisPage.user_id,subject=subject,body=body)
                row_noti.save()

        return JsonResponse({'results':True})
    except:
        return JsonResponse({'results':False})

def set_page_like(request):
    try:
        user = request.user
        id = request.GET.get('id') 
        if LikePage.objects.filter(page_id=id,user_id=user.id):
            LikePage.objects.get(page_id=id,user_id=user.id).delete()
        else:        
            row = LikePage(page_id=id,user_id=user.id)        
            row.save()

            thisPage = Page.objects.get(id=id)
            subject = 'Congratulations! "' + user.first_name + ' ' + user.last_name + '" liked your page ' + thisPage.title
            body = ''
            row_noti = Notification(user_id=thisPage.user_id,subject=subject,body=body)
            row_noti.save()

        return JsonResponse({'results':True})
    except:
        return JsonResponse({'results':False})

