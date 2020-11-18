from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class Posts(models.Model):
    id=models.AutoField(primary_key=True)
    content = models.TextField(max_length=10000)    
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    user_id = models.IntegerField(default='',)
    group_id = models.IntegerField(default='0',)
    page_id = models.IntegerField(default='0',)
    likes= models.IntegerField(default=0)
    views= models.IntegerField(default=0)
    public= models.CharField(default='1',max_length=1)    
    visibleto = models.CharField(default='1',max_length=1, null=True)  
    class Meta:
        db_table = 'posts'

class PostAttach(models.Model):
    id=models.AutoField(primary_key=True)
    post_id = models.IntegerField(default='',null=True)
    attach = models.FileField(upload_to='attach',default='', null=True)
    thumb = models.FileField(upload_to='thumb',default='', null=True)
    attachname = models.TextField(max_length=250,default='', null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True)    
    class Meta:
        db_table = 'postattach'

class GifImg(models.Model):
    id=models.AutoField(primary_key=True)    
    gifimg = models.FileField(upload_to='gif',default='', null=True)
    gifimgname = models.TextField(max_length=250,default='', null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True)    
    class Meta:
        db_table = 'gifimg'

class Likes(models.Model):
    id=models.AutoField(primary_key=True)    
    user_id = models.IntegerField(default='',null=True)
    post_id = models.IntegerField(default='',null=True)   
    created_at = models.DateTimeField(auto_now_add=True,blank=True) 
    class Meta:
        db_table = 'likes'

class LikesComment(models.Model):
    id=models.AutoField(primary_key=True)    
    user_id = models.IntegerField(default='',null=True)
    comment_id = models.IntegerField(default='',null=True)   
    created_at = models.DateTimeField(auto_now_add=True,blank=True) 
    class Meta:
        db_table = 'likescomment'

class LikesReply(models.Model):
    id=models.AutoField(primary_key=True)    
    user_id = models.IntegerField(default='',null=True)
    reply_id = models.IntegerField(default='',null=True)   
    created_at = models.DateTimeField(auto_now_add=True,blank=True) 
    class Meta:
        db_table = 'likesreply'

class Comments(models.Model):
    id=models.AutoField(primary_key=True)    
    user_id = models.IntegerField(default='',null=True)
    post_id = models.IntegerField(default='',null=True)
    content = models.TextField(default='',null=True) 
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)   
    class Meta:
        db_table = 'comments'

class Replies(models.Model):
    id=models.AutoField(primary_key=True)    
    user_id = models.IntegerField(default='',null=True)
    comment_id = models.IntegerField(default='',null=True)
    content = models.TextField(default='',null=True) 
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)   
    class Meta:
        db_table = 'replies' 

class Views(models.Model):
    id=models.AutoField(primary_key=True)    
    user_id = models.IntegerField(default='',null=True)
    post_id = models.IntegerField(default='',null=True)    
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)   
    class Meta:
        db_table = 'views' 