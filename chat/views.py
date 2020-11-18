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
from account.models import CustomUser,Follows,Experience,Education,Visiter
from chat.models import Room,Message

from account.views import get_client_ip,get_geolocation_for_ip,get_random_string,get_curuser,get_users,get_users_following,get_following,get_followers,get_different_time,get_date_str,get_time_str


import datetime
from datetime import timedelta
import random
import string
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from PIL import Image


def get_all_room(request):
    rooms=[]
    try:                  
        search_word = request.GET.get('searchword')        
        user = request.user
        if search_word:
            userIDarray = []
            userstemp = CustomUser.objects.filter(first_name__contains=search_word)|CustomUser.objects.filter(last_name__contains=search_word)        
            for item in userstemp:
                userIDarray.append(item.id)
            userroomstemp = Room.objects.filter(who=user.id,whom__in=userIDarray)|Room.objects.filter(whom=user.id,who__in=userIDarray).order_by('-updated_at')
        else:
            userroomstemp = Room.objects.filter(who=user.id)|Room.objects.filter(whom=user.id).order_by('-updated_at')
        for room in userroomstemp:
            data = {}
            data['room_id']=room.id
            data['status']=room.status

            rows = Message.objects.filter(room_id=room.id,read='0').exclude(user_id=user.id)

            if rows.count() > 0:                 
                data['cnt_message'] = rows.count()                  
            else:
                data['cnt_message'] = ''

            if user.id == room.who:
                data['user_id']=room.whom
                cur_User = CustomUser.objects.get(id=room.whom)
                data['user_name'] = cur_User.username  
                data['full_name'] = cur_User.first_name +" "+ cur_User.last_name 
                                    
                if cur_User.avatar:
                    data['avatar'] = cur_User.avatar.url  
                else:
                    data['avatar']=""
                if room.accepted == '0': 
                    data['accepted']="0" 
                    data['message']=""
                    data['created_at']=""
                else:
                    data['accepted']=room.accepted                          
                    if Message.objects.filter(room_id=room.id):                           
                        data['message']=Message.objects.filter(room_id=room.id).order_by('-created_at').first().content
                        data['created_at']=get_different_time(Message.objects.filter(room_id=room.id).order_by('-created_at').first().created_at)
                    else:
                        data['message']=''
                        data['created_at']=""
            
            else:                
                data['user_id']=room.who
                cur_User = CustomUser.objects.get(id=room.who)
                data['user_name'] = cur_User.username  
                data['full_name'] = cur_User.first_name +" "+ cur_User.last_name 
                                    
                if cur_User.avatar:
                    data['avatar'] = cur_User.avatar.url  
                else:
                    data['avatar']=""
                if room.accepted == '0': 
                    data['accepted']="" 
                    data['message']=""
                    data['created_at']=""
                else:
                    data['accepted']=room.accepted                          
                    if Message.objects.filter(room_id=room.id):                           
                        data['message']=Message.objects.filter(room_id=room.id).order_by('-created_at').first().content
                        data['created_at']=get_different_time(Message.objects.filter(room_id=room.id).order_by('-created_at').first().created_at)
                    else:
                        data['message']=''
                        data['created_at']=""
            rooms.append(data)    
        return JsonResponse({'rooms':rooms})
    except:
        return JsonResponse({'rooms':rooms})


def get_new_message_global(request):
    user = request.user
    messages=[]
    try:
        roomtemp = Room.objects.filter(who=user.id)|Room.objects.filter(whom=user.id).order_by('-created_at')
        for room in roomtemp:
            rows = Message.objects.filter(room_id=room.id,read='0').exclude(user_id=user.id)
            if rows.count() > 0:
                data = {}
                count_message = rows.count()
                first_message = rows.order_by('-created_at').first()
                data['room_id'] = room.id
                data['full_name'] = CustomUser.objects.get(id=first_message.user_id).first_name+" "+CustomUser.objects.get(id=first_message.user_id).last_name
                if CustomUser.objects.get(id=first_message.user_id).avatar:
                    data['user_avatar'] = CustomUser.objects.get(id=first_message.user_id).avatar.url
                else:
                    data['user_avatar'] = ""
                data['cnt_message'] = count_message
                data['message'] = first_message.content
                messages.append(data)
        return JsonResponse({'messages':messages})
    except:
        return JsonResponse({'messages':messages})

def get_new_message(request):
    messages=[]
    try:
        room_id = request.GET.get('room_id') 
        user = request.user        
               
        messagestemp = Message.objects.filter(read='0')
        for message in messagestemp:
            if int(message.user_id) == int(user.id):
                pass
            else:
                if message.read == "0":
                    data = {}
                    data['message_id'] = message.id
                    data['room_id'] = message.room_id
                    data['user_name'] = CustomUser.objects.get(id=message.user_id).username
                    if CustomUser.objects.get(id=message.user_id).avatar:
                        data['avatar']=CustomUser.objects.get(id=message.user_id).avatar.url  
                    else:
                        data['avatar']=""
                    data['message'] = message.content
                    data['created_at'] = get_different_time(message.created_at) 
                    if CustomUser.objects.get(id=message.user_id).username == user.username:
                        data['me'] = "1"
                    else:
                        data['me'] = "0"
                    messages.append(data)
                else:
                    pass
        return JsonResponse({'messages':messages})
    except:
        return JsonResponse({'messages':messages})

def request_chat(request):
    try:
        user = request.user
        whom = request.GET.get('id') 
        is_room = Room.objects.filter(who=user.id,whom=whom)|Room.objects.filter(who=whom,whom=user.id)
        if is_room.count() > 0:
            return JsonResponse({'results':True})
        else:           
            row = Room(who=user.id,whom=whom)
            row.save()
            return JsonResponse({'results':True})       
    except:
        return JsonResponse({'results':False})

def store_message(request):
    try:
        room_id=request.GET.get('room_id')
        if Room.objects.get(id=room_id).status == '1':        
            message = request.GET.get('message')
            user = request.user
            row = Message(room_id=room_id,user_id=user.id,content=message)
            row.save()
            cur_Room = Room.objects.get(id=room_id)
            cur_Room.updated_at = datetime.datetime.now()
            cur_Room.save()
            return JsonResponse({'results':True})
        else:
            return JsonResponse({'results':False})
    except:
        return JsonResponse({'results':False})

def set_read(request):
    try:
        room_id=request.GET.get('room_id')        
        user = request.user
        messages = Message.objects.filter(room_id=room_id)
        for item in messages:
            if int(item.user_id) == int(user.id):
                pass
            else:
                item.read = "1"
                item.save()
        return JsonResponse({'results':True})
    except:
        return JsonResponse({'results':False})

def get_stored_message(request):
    messages=[]
    try:
        room_id = request.GET.get('room_id')  
        user = request.user
        cur_RoomCheck = Room.objects.get(id=room_id)
        if (cur_RoomCheck.who == user.id) or (cur_RoomCheck.whom == user.id):
            if cur_RoomCheck.accepted == '0' and cur_RoomCheck.whom == user.id:
                cur_RoomCheck.accepted = '1'
                cur_RoomCheck.save()
            unReadMsg = Message.objects.filter(room_id=room_id,read='0')
            for item in unReadMsg:
                item.read = '1'
                item.save()
                            
            messagestemp = Message.objects.filter(room_id=room_id)
            for message in messagestemp:
                data = {}
                data['message_id'] = message.id
                data['user_name'] = CustomUser.objects.get(id=message.user_id).username
                if CustomUser.objects.get(id=message.user_id).avatar:
                    data['avatar']=CustomUser.objects.get(id=message.user_id).avatar.url  
                else:
                    data['avatar']=""
                data['message'] = message.content
                data['created_at'] = get_different_time(message.created_at) 
                data['time'] = get_time_str(message.created_at)
                data['date'] = get_date_str(message.created_at)
                if CustomUser.objects.get(id=message.user_id).username == user.username:
                    data['me'] = "1"
                else:
                    data['me'] = "0"
                messages.append(data)
            return JsonResponse({'messages':messages})
        else:
            return JsonResponse({'messages':messages})
    except:
        return JsonResponse({'messages':messages})
