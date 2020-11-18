from django.db import models
import sys
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), null=True,default='')
    avatar = models.ImageField(upload_to='avatar',default='', null=True)
    gender = models.CharField(max_length=20,default='', null=True)
    location = models.CharField(max_length=250,default='', null=True)
    connections = models.CharField(max_length=250,default='0', null=True)
    views = models.CharField(max_length=250,default='0', null=True)
    organization = models.CharField(max_length=250,default='', null=True)
    website = models.CharField(max_length=250,default='', null=True)
    jobtitle = models.CharField(max_length=250,default='', null=True)
    phone = models.CharField(max_length=250,default='', null=True)
    
    aboutme = models.TextField(default='', null=True)
    linkInstagram = models.CharField(max_length=250,default='', null=True)
    linkFacebook = models.CharField(max_length=250,default='', null=True)
    linkTwitter = models.CharField(max_length=250,default='', null=True)
    linkYoutube = models.CharField(max_length=250,default='', null=True)
    linkGithub = models.CharField(max_length=250,default='', null=True)
    birthYear = models.CharField(max_length=250,default='', null=True)
    birthMonth = models.CharField(max_length=250,default='', null=True)
    birthDay = models.CharField(max_length=250,default='', null=True)
    company = models.CharField(max_length=250,default='', null=True)
    position = models.CharField(max_length=250,default='', null=True)
    public_email = models.CharField(max_length=1,default='1', null=True)
    public_phone = models.CharField(max_length=1,default='1', null=True)
    public_birth = models.CharField(max_length=1,default='1', null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True)


class Follows(models.Model):
    id=models.AutoField(primary_key=True)    
    who = models.IntegerField(default='',null=True)
    whom = models.IntegerField(default='',null=True)    
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)   
    class Meta:
        db_table = 'follows'

class Experience(models.Model):
    id=models.AutoField(primary_key=True)   
    user_id = models.IntegerField(default='',null=True) 
    title = models.CharField(max_length=250,default='',null=True) 
    date_start = models.CharField(max_length=250,default='',null=True)
    date_end = models.CharField(max_length=250,default='',null=True)
    company = models.CharField(max_length=250,default='',null=True)
    position = models.CharField(max_length=250,default='',null=True)
    responsibilities = models.TextField(default='',null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)   
    class Meta:
        db_table = 'experience'

class Education(models.Model):
    id=models.AutoField(primary_key=True)   
    user_id = models.IntegerField(default='',null=True) 
    detial = models.CharField(max_length=250,default='',null=True) 
    date_start = models.CharField(max_length=250,default='',null=True)
    date_end = models.CharField(max_length=250,default='',null=True)
    school = models.CharField(max_length=250,default='',null=True)
    degree = models.CharField(max_length=250,default='',null=True)    
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)   
    class Meta:
        db_table = 'education'
   
class Visiter(models.Model):
    id=models.AutoField(primary_key=True)    
    who = models.IntegerField(default='',null=True)
    whom = models.IntegerField(default='',null=True)    
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)   
    class Meta:
        db_table = 'visiter'

class Notification(models.Model):
    id=models.AutoField(primary_key=True)    
    user_id = models.IntegerField(default=0,null=True) 
    subject = models.CharField(max_length=250,default='',null=True)    
    body = models.CharField(max_length=250,default='',null=True)    
    read = models.CharField(max_length=1,default='0',null=True)    
    condition = models.CharField(max_length=100,default='',null=True)
    

    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)   
    class Meta:
        db_table = 'notification'


     
