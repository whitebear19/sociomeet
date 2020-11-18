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

from groups.models import Group,GroupToUserInvite,FollowsGroup,LikeGroup,ViewsGroup
from pages.models import Page,PageToUserInvite,FollowsPage


import datetime
from datetime import timedelta
import random
import string
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from PIL import Image

def getgroups(tempgroups,request,status):
    results = []
    user = request.user
    for item in tempgroups:
        data = {}
        data['id'] = item.id
        thisUser=CustomUser.objects.get(id=item.user_id)
        if thisUser.avatar:
            data['avatar'] = thisUser.avatar.url
        else:
            data['avatar'] = '/static/img/avatar.png'
        data['title'] = item.title
        data['followers'] = FollowsGroup.objects.filter(group_id=item.id).count()
        data['likes'] = LikeGroup.objects.filter(group_id=item.id).count()
        data['posts'] = Posts.objects.filter(group_id=item.id).count()
        data['views'] = ViewsGroup.objects.filter(group_id=item.id).count()
        if LikeGroup.objects.filter(user_id=user.id,group_id=item.id):
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

def groupdashboard(request):

    if not request.user.is_authenticated:
        return redirect('/login')
    user = request.user         
   
    users = []        
    users = get_users(request)   
    
    curuser = {}
    curuser = get_curuser(request,user.id)      
       
    usergroups = []
    allgroups = []
    followgroups = []
    followgroupsID = []
    followgroupsIDtemp = FollowsGroup.objects.filter(user_id=user.id)
    for item in followgroupsIDtemp:
        followgroupsID.append(item.group_id)
    
    mygroupstemp = Group.objects.filter(user_id=user.id)
    allgroupstemp = Group.objects.exclude(user_id=user.id).exclude(id__in=followgroupsID)    
    followgroupstemp = Group.objects.filter(id__in=followgroupsID)
    status="0"
    usergroups = getgroups(mygroupstemp,request,status)
    status="2"
    allgroups = getgroups(allgroupstemp,request,status)
    status="1"
    followgroups = getgroups(followgroupstemp,request,status)

    return render(request,'groups/dashboard.html',{'users':users,'curuser':curuser,'usergroups':usergroups,'allgroups':allgroups,'followgroups':followgroups}) 

def create(request):

    user = request.user 
    users = CustomUser.objects.exclude(id=user.id)
    return render(request,'groups/create.html',{'users':users}) 

def view_group_detail(request,group_id):

    user = request.user 
    cur_group = {}
    cur_temp = Group.objects.get(id=group_id)
    cur_group['id'] = cur_temp.id
    if cur_temp.avatar:
        cur_group['back'] = cur_temp.avatar.url
    else:
        cur_group['back'] = '/static/img/no_banner.png'
    cur_group['title'] = cur_temp.title
    cur_group['followers'] = FollowsGroup.objects.filter(group_id=group_id).count()
    cur_group['likes'] = LikeGroup.objects.filter(group_id=group_id).count()    
    cur_group['posts'] = Posts.objects.filter(group_id=group_id).count()
    cur_group['views'] = ViewsGroup.objects.filter(group_id=group_id).count()

       
    if LikeGroup.objects.filter(user_id=user.id,group_id=group_id):
        cur_group['liked'] = '1'
    else:
        cur_group['liked'] = '0'




    if cur_temp.user_id == user.id:
        cur_group['me'] = '1'
        cur_group['followed'] = '0'
    else:
        cur_group['me'] = '0'
        if FollowsGroup.objects.filter(group_id=cur_temp.id,user_id=user.id):
            cur_group['followed'] = '1'
        else:
            cur_group['followed'] = '0'
    this_user = CustomUser.objects.get(id=cur_temp.user_id)
    if this_user.avatar:
        cur_group['avatar'] = this_user.avatar.url
    else:
        cur_group['avatar'] = '/static/img/avatar.png'

    users = CustomUser.objects.exclude(id=user.id)

    if ViewsGroup.objects.filter(user_id=user.id,group_id=group_id):
        pass
    else:
        row = ViewsGroup(user_id=user.id,group_id=group_id)
        row.save()

    allgroups = []    
    followgroupsID = []
    followgroupsIDtemp = FollowsGroup.objects.filter(user_id=user.id)
    for item in followgroupsIDtemp:
        followgroupsID.append(item.group_id)
        
    allgroupstemp = Group.objects.exclude(user_id=user.id).exclude(id__in=followgroupsID)    
    followgroupstemp = Group.objects.filter(id__in=followgroupsID) 
    status = '2'   
    allgroups = getgroups(allgroupstemp,request,status)  

    return render(request,'groups/details.html',{'users':users,'cur_group':cur_group,'groups':allgroups}) 


# ----------------ajax_part------------------------
def store_group(request):
    try:
        user = request.user
        title = request.POST.get('title') 
        invitetype = request.POST.get('invitetype') 
        row = Group(title=title,user_id=user.id,avatar=request.FILES.get('attach'))        
        row.save()
        group_id = row.id
        if(invitetype=='1'):
            usertemp = Follows.objects.filter(whom=user.id)            
            if usertemp:
                for item in usertemp:
                    invite = GroupToUserInvite(group_id=group_id,user_id=item.who)
                    invite.save()
        else:
            users_id = request.POST.get('users')
            if users_id:
                users_id = users_id.split(",")    
                for item in users_id:
                    if GroupToUserInvite.objects.filter(group_id=group_id,user_id=item):
                        pass
                    else:
                        invite = GroupToUserInvite(group_id=group_id,user_id=item)
                        invite.save()

        subject = 'New group "'+ title + '" created successfully.'  
        body = 'Your group is created successfully. Invite people to get more response, likes to your group posts.'
        row_noti = Notification(user_id=user.id,subject=subject,body=body)
        row_noti.save()

        data = True
        return JsonResponse({'results':data,'id':group_id})
    except:
        return JsonResponse({'results':False})

def set_followgroup(request):
    try:
        user = request.user
        id = request.POST.get('id') 
        if FollowsGroup.objects.filter(group_id=id,user_id=user.id):
            FollowsGroup.objects.get(group_id=id,user_id=user.id).delete()
        else: 
            if Group.objects.filter(id=id,user_id=user.id):
                pass
            else:
                row = FollowsGroup(group_id=id,user_id=user.id)        
                row.save()

                thisGroup = Group.objects.get(id=id)
                subject = user.first_name + ' ' + user.last_name + ' started following your group ' + thisGroup.title
                body = ''
                row_noti = Notification(user_id=thisGroup.user_id,subject=subject,body=body)
                row_noti.save()

        return JsonResponse({'results':True})
    except:
        return JsonResponse({'results':False})

def set_group_like(request):
    try:
        user = request.user
        id = request.GET.get('id') 
        if LikeGroup.objects.filter(group_id=id,user_id=user.id):
            LikeGroup.objects.get(group_id=id,user_id=user.id).delete()
        else:        
            row = LikeGroup(group_id=id,user_id=user.id)        
            row.save()

            thisGroup = Group.objects.get(id=id)
            subject = 'Congratulations! "' + user.first_name + ' ' + user.last_name + '" liked your group ' + thisGroup.title
            body = ''
            row_noti = Notification(user_id=thisGroup.user_id,subject=subject,body=body)
            row_noti.save()

        return JsonResponse({'results':True})
    except:
        return JsonResponse({'results':False})


