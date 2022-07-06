from django.db import models
from django.contrib.auth.models import User


class UserLoggedInSession(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    city = models.CharField(max_length=255, default='')
    country = models.CharField(max_length=255, default='')
    region = models.CharField(max_length=255, default='')
    location = models.CharField(max_length=255, default='')
    timezone = models.CharField(max_length=255, default='')
    ip =  models.CharField(max_length=255, default='')
    user_agent =  models.CharField(max_length=255, default='')
    login_time = models.DateTimeField(auto_now_add=True)
    access_token = models.TextField(default='')
    refresh_token = models.TextField(default='')
