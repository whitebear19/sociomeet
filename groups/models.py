from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class Group(models.Model):
    id=models.AutoField(primary_key=True)
    user_id = models.IntegerField(default='',)
    title = models.CharField(max_length=250,default='0', null=True)  
    avatar = models.ImageField(upload_to='group',default='', null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True)    
    class Meta:
        db_table = 'group'

class GroupToUserInvite(models.Model):
    id=models.AutoField(primary_key=True)
    group_id = models.IntegerField(default='',)
    user_id = models.IntegerField(default='',)
    status = models.CharField(max_length=1,default='0', null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True)    
    class Meta:
        db_table = 'grouptouserinvite'

class FollowsGroup(models.Model):
    id=models.AutoField(primary_key=True)
    group_id = models.IntegerField(default='',)
    user_id = models.IntegerField(default='',)    
    created_at = models.DateTimeField(auto_now_add=True,blank=True)    
    class Meta:
        db_table = 'followsgroup'

class LikeGroup(models.Model):
    id=models.AutoField(primary_key=True)
    group_id = models.IntegerField(default='',)
    user_id = models.IntegerField(default='',)    
    created_at = models.DateTimeField(auto_now_add=True,blank=True)    
    class Meta:
        db_table = 'likegroup'
        
class ViewsGroup(models.Model):
    id=models.AutoField(primary_key=True)    
    user_id = models.IntegerField(default='',null=True)
    group_id = models.IntegerField(default='',null=True)    
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)   
    class Meta:
        db_table = 'viewsgroup' 