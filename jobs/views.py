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
from pages.models import Page,PageToUserInvite,FollowsPage
from jobs.models import Jobs


import datetime
from datetime import timedelta
import random
import string
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from PIL import Image


PAGINATION_COUNT = 31

def get_date_ago(orgtime):
    result = 0
    curtime = datetime.datetime.now()
    datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
    date1 = orgtime.strftime('%Y-%m-%d %H:%M:%S.%f')
    date2 = curtime.strftime('%Y-%m-%d %H:%M:%S.%f')
    diff = datetime.datetime.strptime(date2, datetimeFormat)\
        - datetime.datetime.strptime(date1, datetimeFormat)        
    if(int(diff.days) < 1):
        curDate = curtime.strftime('%d')
        orgDate = orgtime.strftime('%d')
        if curDate == orgDate:
            result = 0
        
    elif (int(diff.days) < 4):
        result = 3
    elif (int(diff.days) < 8):
        result = 7
    elif (int(diff.days) < 15):
        result = 14
    elif (int(diff.days) < 31):
        result = 30
    else:
        result = 99
    return result

def jobdashboard(request):

    if not request.user.is_authenticated:
        return redirect('/login')
    user = request.user
    

    return render(request,'jobs/dashboard.html',{}) 
def userjobs(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    user = request.user
    

    return render(request,'jobs/userjobs.html',{}) 

def create(request):

    user = request.user     

    return render(request,'jobs/create.html',{}) 

def view_job_detail(request,job_id):
    try:

        job = Jobs.objects.get(id=job_id)
        thisuser = CustomUser.objects.get(id=job.user_id)
        data = {} 
        data['id'] = job.id
        data['title'] = job.title
        data['jobtype'] = job.jobtype
        data['remote'] = job.remote
        data['created_at'] = job.created_at.strftime('%d/%Y/%m')
        data['salary'] = job.salary
        data['period'] = job.period
        data['postedby'] = thisuser.first_name + " " + thisuser.last_name
        data['travel'] = job.travel
        data['client'] = job.client
        data['description'] = job.description
        data['benefits'] = job.benefits
        data['workauth'] = job.workauth
        return render(request,'jobs/details.html',{'job':data})
    except:
        return redirect('/job/dashboard')



# ----------------ajax_part------------------------

def store_job(request):
    try:
        user = request.user
        title = request.POST.get('job_title')
        description = request.POST.get('job_description')    
        email = request.POST.get('email')    
        phone = request.POST.get('phone')
        url = request.POST.get('url')
        reply = request.POST.get('reply')
        client = request.POST.get('client')
        location = request.POST.get('location')
        jobtype = request.POST.get('jobtype')
        remote = request.POST.get('remote')
        travel = request.POST.get('travel')
        salary = request.POST.get('salary')
        period = request.POST.get('period')
        benefits = request.POST.get('benefits')
        workauth = request.POST.get('workauth')
        job_zip = request.POST.get('job_zip')
        job_city = request.POST.get('job_city')
        job_state = request.POST.get('job_state')
        job_country = request.POST.get('job_country')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        row = Jobs(title=title,description=description,jobtype=jobtype,email=email,phone=phone,url=url,reply=reply,client=client,location=location,remote=remote,travel=travel,salary=salary,period=period,benefits=benefits,workauth=workauth,job_zip=job_zip,job_city=job_city,job_state=job_state,job_country=job_country,lat=lat,lng=lng,user_id=user.id)
        row.save()
        all_users = CustomUser.objects.exclude(id=user.id)
        if all_users:
            for item in all_users:
                if item.jobtitle:
                    print(item.jobtitle)
                    sub_string = item.jobtitle.split(" ")
                    print(sub_string)
                    for sub in sub_string:                    
                        if (sub in title) or (sub in description):
                            subject = 'New job posted by "' + user.first_name + user.last_name + '"' 
                            body = '<a href="#">' + title + '</a>'
                            row_noti = Notification(user_id=item.id,subject=subject,body=body)
                            row_noti.save()
                            break
        
        return JsonResponse({'results':True})
    except:
        return JsonResponse({'results':False})

def get_content_list(request):
    where = request.GET.get('where')
    jobs = ''
    results = []
    pagenum = 0
    jobtype = ''
    remote = ''
    dateposted = ''
    
    try:
        
        user = request.user
        currentPage = request.GET.get('currentPage')
        jobtype = request.GET.get('jobtype')
        remote = request.GET.get('remote')
        dateposted = request.GET.get('dateposted')

        if where=='1':
            if remote and jobtype:
                jobs = Jobs.objects.filter(jobtype=jobtype,remote=remote).order_by('-created_at') 
            elif remote:
                jobs = Jobs.objects.filter(remote=remote).order_by('-created_at') 
            elif jobtype:
                jobs = Jobs.objects.filter(jobtype=jobtype).order_by('-created_at') 
            else:
                jobs = Jobs.objects.all().order_by('-created_at')
        else:
            if remote and jobtype:
                jobs = Jobs.objects.filter(user_id=user.id,jobtype=jobtype,remote=remote).order_by('-created_at') 
            elif remote:
                jobs = Jobs.objects.filter(user_id=user.id,remote=remote).order_by('-created_at') 
            elif jobtype:
                jobs = Jobs.objects.filter(user_id=user.id,jobtype=jobtype).order_by('-created_at') 
            else:
                jobs = Jobs.objects.filter(user_id=user.id).order_by('-created_at')
                
        pagenum = math.ceil(jobs.count()/PAGINATION_COUNT)
        paginator = Paginator(jobs,PAGINATION_COUNT)   
        resultscollection = paginator.get_page(currentPage) 
    
        for item in resultscollection:
            data = {}                            
            data['id'] = item.id
            if CustomUser.objects.get(id=item.user_id):
                thisuser = CustomUser.objects.get(id=item.user_id)
                if thisuser.avatar:
                    data['avatar'] = thisuser.avatar.url
                else:
                    data['avatar'] = '/static/img/user.png'
            data['title'] = item.title
            data['client'] = item.client
            data['location'] = item.job_city+","+item.job_state+","+item.job_country
            data['date'] = item.created_at.strftime('%Y-%m-%d')
            data['salary'] = item.salary
            data['period'] = item.period  

            if dateposted:    
                date_ago = get_date_ago(item.created_at)      
                
                if int(dateposted) < 1: 
                    if date_ago < 1:                   
                        results.append(data)
                elif int(dateposted) < 4:
                    if date_ago < 4:  
                        results.append(data)
                elif int(dateposted) < 8:
                    if date_ago < 8:  
                        results.append(data)
                elif int(dateposted) < 15:
                    if date_ago < 15:  
                        results.append(data)
                elif int(dateposted) < 31:
                    if date_ago < 31:  
                        results.append(data)
            else:
                results.append(data)

        return JsonResponse({'results':results,'pagenum':pagenum})
    except:
        return JsonResponse({'results':results,'pagenum':pagenum})

def get_postcode(request):
    zipcode = ''
    try:
        ipaddress = get_client_ip(request)         
        geo_info = get_geolocation_for_ip(ipaddress)
        results=json.dumps(geo_info) 
        results=json.loads(results)        
        if results['zip']:
            zipcode = results['zip']
        return JsonResponse({'results':True,'zipcode':zipcode})
    except:
        return JsonResponse({'results':False,'zipcode':zipcode})