from django.db import models
import sys
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class Room(models.Model):
    id=models.AutoField(primary_key=True)    
    who = models.IntegerField(default='',null=True)
    whom = models.IntegerField(default='',null=True)    
    accepted = models.CharField(max_length=1,default='0',null=True)    
    status = models.CharField(max_length=1,default='',null=True)    
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)   
    updated_at = models.DateTimeField(blank=True,null=True)
    class Meta:
        db_table = 'room'

class Message(models.Model):
    id=models.AutoField(primary_key=True)    
    room_id = models.IntegerField(default='',null=True)
    user_id = models.IntegerField(default='',null=True) 
    content = models.TextField(max_length=1000,default='',null=True)     
    read = models.CharField(max_length=1,default='0',null=True)    
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)   
    class Meta:
        db_table = 'message'
