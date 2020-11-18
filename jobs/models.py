from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class Jobs(models.Model):
    id=models.AutoField(primary_key=True)
    title= models.CharField(default='',max_length=250)   
    description = models.TextField(max_length=10000)    
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    user_id = models.IntegerField(default='',)
    jobtype = models.CharField(default='',max_length=250,blank=True,null=True)
    remote = models.CharField(default='',max_length=250,blank=True,null=True)
    salary= models.CharField(default='',max_length=250,blank=True,null=True)
    period= models.CharField(default='',max_length=250,blank=True,null=True)
    travel = models.CharField(default='',max_length=250,blank=True,null=True)
    client = models.CharField(default='',max_length=250,blank=True,null=True)
    benefits = models.TextField(default='',max_length=1000,blank=True,null=True)
    workauth = models.TextField(default='',max_length=1000,blank=True,null=True)
    status= models.CharField(default='1',max_length=1,blank=True,null=True)    
    lat= models.CharField(default='',max_length=250,blank=True,null=True)    
    lng= models.CharField(default='',max_length=250,blank=True,null=True)    
    email= models.CharField(default='',max_length=250,blank=True,null=True)    
    phone= models.CharField(default='',max_length=250,blank=True,null=True)    
    url= models.CharField(default='',max_length=250,blank=True,null=True)
    reply= models.CharField(default='',max_length=1,blank=True,null=True)
    job_zip= models.CharField(default='',max_length=10,blank=True,null=True)
    job_city= models.CharField(default='',max_length=50,blank=True,null=True)
    job_state= models.CharField(default='',max_length=50,blank=True,null=True)
    job_country= models.CharField(default='',max_length=50,blank=True,null=True)
    location= models.CharField(default='',max_length=50,blank=True,null=True)
    class Meta:
        db_table = 'jobs'
