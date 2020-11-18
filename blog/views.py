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
from django.core.files import File


from blog.models import Posts,Likes,Comments,PostAttach,LikesComment,Replies,LikesReply,Views
from account.models import CustomUser,Follows,Experience,Education,Visiter,Notification
from chat.models import Room,Message
from groups.models import Group,GroupToUserInvite,FollowsGroup,LikeGroup,ViewsGroup
from pages.models import Page,PageToUserInvite,FollowsPage,LikePage,ViewsPage

import datetime
from datetime import timedelta
import random
import string
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from PIL import Image
from django.conf import settings

from account.views import get_client_ip,get_geolocation_for_ip,get_random_string,get_curuser,get_users,get_users_following,get_following,get_followers,get_different_time,get_date_str,get_time_str


PAGINATION_COUNT = 21

def get_date_ago(orgtime):
    result = 0
    curtime = datetime.datetime.now()
    datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
    date1 = orgtime.strftime('%Y-%m-%d %H:%M:%S.%f')
    date2 = curtime.strftime('%Y-%m-%d %H:%M:%S.%f')
    diff = datetime.datetime.strptime(date2, datetimeFormat)\
        - datetime.datetime.strptime(date1, datetimeFormat)  
    result = int(diff.days)
    return result

def get_selected_post(request):
    data = {} 
    try:
        id = request.GET.get('id')    
        post = Posts.objects.get(id=id)   
        user = request.user
        data = {}    
        attaches = []
        temps = PostAttach.objects.filter(post_id=id)
        for temp in temps:
            attaches.append(temp.attachname)
        data['post_id'] = id
        data['content'] = post.content
        data['visibleto'] = post.visibleto
        data['attach'] = attaches            
        return JsonResponse({'results':data})
    except:
        return JsonResponse({'results':data})

def add_like(request):
    try:
        user = request.user  
        post_id = request.GET.get('id')
        liked = Likes.objects.filter(user_id=user.id,post_id=post_id)
        if liked : 
            liked.delete()
        else :
            row = Likes(user_id=user.id,post_id=post_id)
            row.save()
            thisPost = Posts.objects.get(id=post_id)
            thisUser = CustomUser.objects.get(id=thisPost.user_id)
            
            if thisPost.content:
                subject = thisUser.first_name+' '+thisUser.last_name+ ' liked your post <a href="">' + thisPost.content + '</a>' 
            else:
                subject = thisUser.first_name+' '+thisUser.last_name+ ' liked your post <a href="">this post</a>' 

            body = ''
            row_noti = Notification(user_id=thisUser.id,subject=subject,body=body)
            row_noti.save()

        return JsonResponse({'response':True})
    except:
        return JsonResponse({'response':False})
def add_like_comment(request):
    try:
        user = request.user  
        comment_id = request.GET.get('id')
        liked = LikesComment.objects.filter(user_id=user.id,comment_id=comment_id)
        if liked : 
            liked.delete()
        else :
            row = LikesComment(user_id=user.id,comment_id=comment_id)
            row.save()
        return JsonResponse({'response':True})
    except:
        return JsonResponse({'response':False})

def add_like_reply(request):
    try:
        user = request.user  
        rid = request.GET.get('rid')
        liked = LikesReply.objects.filter(user_id=user.id,reply_id=rid)
        if liked : 
            liked.delete()
        else :
            row = LikesReply(user_id=user.id,reply_id=rid)
            row.save()
        return JsonResponse({'response':True})
    except:
        return JsonResponse({'response':False})


def delete_post(request):
    try:
        post_id = request.GET.get('id')
        PostAttach.objects.filter(post_id=post_id).delete() 
        Comments.objects.filter(post_id=post_id).delete()  
        Comments.objects.filter(post_id=post_id).delete()  
        Likes.objects.filter(post_id=post_id).delete() 

        row = Posts.objects.get(id=post_id)
        row.delete()
        return JsonResponse({'response':True})
    except:
        return redirect('/dashboard')
def delete_attach(request):
    id = request.GET.get('id')
    PostAttach.objects.get(id=id).delete()
    return JsonResponse({'response':True})

def get_content_list(request):
    posts = ''
    results = []
    pagenum = 0
    try:
        if not request.user.is_authenticated:
            return redirect('/login')

        user = request.user
        currentPage = request.GET.get('currentPage')
        where = request.GET.get('where')
        where1 = request.GET.get('where1')
        print(where1) 
        if where == 'profilepage' :                   
            posts = Posts.objects.filter(user_id=user.id).order_by('-created_at')
        elif where == 'dashboardpage' :
            useridarray=[]
            useridarray.append(user.id)
            userarray = Follows.objects.filter(who=user.id)
            for item in userarray :
                useridarray.append(item.whom)            
            posts = Posts.objects.filter(public='1',user_id__in=useridarray,group_id=0,page_id=0)|Posts.objects.filter(public='1',visibleto='1').order_by('-created_at')

        elif where == 'trending':            
            useridarray=[]
            useridarray.append(user.id)
            userarray = Follows.objects.filter(who=user.id)
            for item in userarray :
                useridarray.append(item.whom)            
            posts = Posts.objects.filter(public='1',user_id__in=useridarray,group_id=0,page_id=0)|Posts.objects.filter(public='1',visibleto='1').order_by('-created_at')

        elif request.GET.get('group_id'):
            group_id = request.GET.get('group_id')
            thisGroup = Group.objects.get(id=group_id)
            if thisGroup.user_id == user.id:
                posts = Posts.objects.filter(group_id=group_id).order_by('-created_at')
            else:
                if FollowsGroup.objects.filter(group_id=group_id,user_id=user.id):
                    posts = Posts.objects.filter(group_id=group_id).order_by('-created_at')

        elif request.GET.get('page_id'):
            page_id = request.GET.get('page_id')
            thisPage = Page.objects.get(id=page_id)
            if thisPage.user_id == user.id:
                posts = Posts.objects.filter(page_id=page_id).order_by('-created_at')
            else:
                if FollowsPage.objects.filter(page_id=page_id,user_id=user.id):
                    posts = Posts.objects.filter(page_id=page_id).order_by('-created_at')                    

        else:  
            posts = Posts.objects.filter(user_id=where).order_by('-created_at')        
        
        pagenum = math.ceil(posts.count()/PAGINATION_COUNT)
        paginator = Paginator(posts,PAGINATION_COUNT)   
        resultscollection = paginator.get_page(currentPage) 
    
        for item in resultscollection:
            data = {}
            if item.user_id == user.id:
                data['me'] = '1'
            else:
                data['me'] = '0'
            posteduser = CustomUser.objects.get(id=item.user_id)
            if posteduser.avatar.name :
                data['avatar'] = posteduser.avatar.name
            else :
                data['avatar'] = 'avatar/user.png'
            attaches = []
            temps = PostAttach.objects.filter(post_id=item.id)
            
            for temp in temps:
                attaches.append(temp.attachname)
                
            data['username'] = posteduser.username
            data['fullname'] = posteduser.first_name +" "+posteduser.last_name
            data['post_id'] = item.id
            data['views'] = item.views
            data['content'] = item.content
            data['attach'] = attaches
            data['attachname'] = ''
            data['created_at'] = get_different_time(item.created_at)
            data['likes'] = Likes.objects.filter(post_id=item.id).count()
            data['comments'] = Comments.objects.filter(post_id=item.id).count()
            data['liked'] = Likes.objects.filter(user_id=user.id,post_id=item.id).count()
            data['public'] = item.public

            if where == 'trending': 
                date_ago = get_date_ago(item.created_at)
                if date_ago < 2:
                    results.append(data)
            else:                 
                results.append(data)
        return JsonResponse({'results':results,'pagenum':pagenum})
    except:
        return JsonResponse({'results':results,'pagenum':pagenum})

def store_post(request):    
    try:
        post_id = request.POST.get('post_id')
        content = request.POST.get('content')
        if post_id:
            post = Posts.objects.get(id=post_id)
            post.content = content
            post.created_at = datetime.datetime.now()
            post.visibleto = request.POST.get('visibleto')
            post.save()

            attachname = request.POST.getlist('attachname[]')
            old_attach = PostAttach.objects.filter(post_id=post_id)
            for item in old_attach:
                item.post_id = 0
                item.save()
            if attachname:
                for item in attachname:  
                    if PostAttach.objects.filter(attachname=item).first():                        
                        attachrow = PostAttach.objects.filter(attachname=item).first()
                        attachrow.post_id = post_id
                        attachrow.save()  
                   
            return JsonResponse({'post_id':post_id})        
        else:
            user = request.user    
            attachname = request.POST.getlist('attachname[]')
            if request.POST.get('group_id'):
                row = Posts(content=content,user_id=user.id,group_id=request.POST.get('group_id'),visibleto=request.POST.get('visibleto'))
            elif request.POST.get('page_id'):
                row = Posts(content=content,user_id=user.id,page_id=request.POST.get('page_id'),visibleto=request.POST.get('visibleto'))
            else:
                row = Posts(content=content,user_id=user.id,visibleto=request.POST.get('visibleto'))
            row.save()
            post_id = row.id
            
            if attachname:
                for item in attachname:
                    attachrow = PostAttach.objects.filter(attachname=item).first()
                    attachrow.post_id = post_id
                    attachrow.save()  

            myallfollowers = Follows.objects.filter(whom=user.id)  
            if myallfollowers:
                for item in myallfollowers:                    
                    if content:
                        subject = user.first_name + ' ' + user.last_name+ ' posted <a href="">' + content + '</a>' 
                    else:
                        subject = user.first_name + ' ' + user.last_name+ ' posted <a href="">this post</a>' 

                    body = ''
                    row_noti = Notification(user_id=item.who,subject=subject,body=body)
                    row_noti.save()

            return JsonResponse({'post_id':post_id})
    except:
        return redirect('/dashboard')
def store_postattach(request):   
    attachname = '' 
    try:
        user = request.user    
        attachname = request.FILES.get('attach').name
        row = PostAttach(post_id=0,attach=request.FILES.get('attach'),attachname=attachname)
        row.save()    
        attachname = str(row.attach) 
        row.attachname = attachname
        row.thumb = request.FILES.get('attach')        
        row.save()        
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        CONTENT_DIR = os.path.join(BASE_DIR, 'content')
        CONTENT_DIR = os.path.join(CONTENT_DIR, 'media')
        CONTENT_DIR = os.path.join(CONTENT_DIR, 'thumb')
        filename = attachname.split('/')[1]
       
        # print(CONTENT_DIR)
        # img = Image.open(CONTENT_DIRfilename)
        return JsonResponse({'attachname':attachname})
    except:
        return JsonResponse({'attachname':attachname})

def store_gif(request):
    attachname = '' 
    try:
        user = request.user    
        name = request.GET.get('name')  
        attachname ='gif/'+name
        row = PostAttach(post_id=0,attachname=attachname)
        row.save()  
        
        return JsonResponse({'attachname':attachname})
    except:
        return JsonResponse({'attachname':attachname})

def addcomment(request):
    try:
        user=request.user  
        post_id = request.GET.get('post_id')      
        row = Comments(user_id=user.id,post_id=post_id,content=request.GET.get('content'))
        row.save()

        thisPost = Posts.objects.get(id=post_id)
        thisUser = CustomUser.objects.get(id=thisPost.user_id)
        if thisPost.group_id:
            thisGroup = Group.objects.get(id=thisPost.group_id)
            subject = user.first_name+' '+user.last_name+ ' commented on your group <a href="">' + thisGroup.title + '</a>'
        elif thisPost.page_id:
            thisPage = Page.objects.get(id=thisPost.page_id)
            subject = user.first_name+' '+user.last_name+ ' commented on your page <a href="">' + thisPage.title + '</a>'
        else:
            if thisPost.content:
                subject = thisUser.first_name+' '+thisUser.last_name+ ' commented to your post <a href="">' + thisPost.content + '</a>' 
            else:
                subject = thisUser.first_name+' '+thisUser.last_name+ ' commented to your post <a href="">this post</a>' 

        body = request.GET.get('content')
        row_noti = Notification(user_id=thisUser.id,subject=subject,body=body)
        row_noti.save()


        return JsonResponse({'results':True,'cid':row.id,'pid':post_id})
    except:
        return JsonResponse({'results':False})


def addreply(request):
    try:
        user=request.user  
        comment_id = request.GET.get('comment_id')      
        row = Replies(user_id=user.id,comment_id=comment_id,content=request.GET.get('content'))
        row.save()
        thisComment = Comments.objects.get(id=comment_id)
        thisUser = CustomUser.objects.get(id=thisComment.user_id)
        thisPost = Posts.objects.get(id=thisComment.post_id)
        if thisPost.content:
            subject = thisUser.first_name+' '+thisUser.last_name+ ' replied to your post <a href="">' + thisPost.content + '</a>' 
        else:
            subject = thisUser.first_name+' '+thisUser.last_name+ ' replied to your post <a href="">this post</a>' 

        body = request.GET.get('content')
        row_noti = Notification(user_id=thisUser.id,subject=subject,body=body)
        row_noti.save()

        return JsonResponse({'results':True,'rid':row.id,'cid':comment_id})
    except:
        return JsonResponse({'results':False})

def deletecomment(request):
    try:
        user=request.user        
        row = Comments.objects.get(id=request.GET.get('cid'))
        row.delete()
        return JsonResponse({'results':True})
    except:
        return JsonResponse({'results':False})

def deletereply(request):

    try:
        user=request.user        
        row = Replies.objects.get(id=request.GET.get('rid'))
        row.delete()
        return JsonResponse({'results':True})
    except:
        return JsonResponse({'results':False})

def getcomments(request):
    comments=[]
    try:
        user=request.user        
        commentstemp = Comments.objects.filter(post_id=request.GET.get('pid')).order_by('-created_at')
        for item in commentstemp:
            data={}
            data['user_id'] = item.user_id
            thisUser = CustomUser.objects.get(id=item.user_id)
            data['full_name'] = thisUser.first_name +" "+ thisUser.last_name
            data['created_at'] = get_different_time(item.created_at) 
            if thisUser.avatar:
                data['avatar']=thisUser.avatar.url  
            else:
                data['avatar']=""
            data['content'] = item.content
            if item.user_id == user.id:
                data['me'] = '1'
            else:
                data['me'] = '0'
            data['cid'] = item.id
            data['pid'] = item.post_id
            if LikesComment.objects.filter(user_id=user.id,comment_id=item.id).count():
                data['mylike'] = '1'
            else:
                data['mylike'] = '0'
            data['likes'] = LikesComment.objects.filter(comment_id=item.id).count()
            data['replies'] = Replies.objects.filter(comment_id=item.id).count()
            comments.append(data)

        return JsonResponse({'comments':comments})
    except:
        return JsonResponse({'comments':comments})

def getcomment(request):
    data = ''
    try:
        cid = request.GET.get('cid')
        data = Comments.objects.get(id=cid).content
        return JsonResponse({'data':data})
    except:
        return JsonResponse({'data':data})

def updatecomment(request):    
    try:
        cid = request.GET.get('cid')
        row = Comments.objects.get(id=cid)
        row.content = request.GET.get('content')
        row.save()
        return JsonResponse({'results':True})
    except:
        return JsonResponse({'results':False})

def updatereply(request):    
    try:
        rid = request.GET.get('rid')
        row = Replies.objects.get(id=rid)
        row.content = request.GET.get('content')
        row.save()
        return JsonResponse({'results':True})
    except:
        return JsonResponse({'results':False})

def getreply(request):
    data = ''
    try:
        rid = request.GET.get('rid')
        data = Replies.objects.get(id=rid).content
        return JsonResponse({'data':data})
    except:
        return JsonResponse({'data':data})



def getreplies(request):
    replies=[]
    try:
        user=request.user        
        repliestemp = Replies.objects.filter(comment_id=request.GET.get('cid')).order_by('-created_at')
        
        for item in repliestemp:
            data={}
            data['user_id'] = item.user_id
            thisUser = CustomUser.objects.get(id=item.user_id)
            if thisUser.avatar:
                data['avatar']=thisUser.avatar.url  
            else:
                data['avatar']=""
            data['content'] = item.content
            if item.user_id == user.id:
                data['me'] = '1'
            else:
                data['me'] = '0'

            if LikesReply.objects.filter(user_id=user.id,reply_id=item.id).count():
                data['mylike'] = '1'
            else:
                data['mylike'] = '0'

            data['full_name'] = thisUser.first_name +" "+ thisUser.last_name
            data['created_at'] = get_different_time(item.created_at)
            data['likes'] = LikesReply.objects.filter(reply_id=item.id).count()
            data['rid'] = item.id
            data['cid'] = item.comment_id
            replies.append(data)

        return JsonResponse({'replies':replies})
    except:
        return JsonResponse({'replies':replies})

def set_private(request):
    try:
        user = request.user  
        post_id = request.GET.get('id')
        row = Posts.objects.get(id=post_id)
        if row.public == '1':
            row.public = '0'
            row.save()
            return JsonResponse({'response':True,'status':'0'})
        else:
            row.public = '1'
            row.save()
            return JsonResponse({'response':True,'status':'1'})
    except:
        return JsonResponse({'response':False})

def set_view(request):
    try:
        pid = request.GET.get('pid')
        user = request.user  
        if Views.objects.filter(user_id=user.id,post_id=pid):
            pass
        else:
            row=Views(user_id=user.id,post_id=pid)
            row.save()
            thispost = Posts.objects.get(id=pid)
            thispost.views = thispost.views + 1
            thispost.save()
        return JsonResponse({'response':True})
    except:
        return JsonResponse({'response':False})