from django.db import models
from django.utils.timezone import now
from django.conf import settings
from datetime import timedelta
# Create your models here.

class usertab(models.Model):
    username = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    password = models.CharField(max_length=500)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_block = models.BooleanField(default=False)
    refercode = models.CharField(max_length=500)
    referredby = models.CharField(null=True,max_length=500)
    img = models.ImageField(upload_to='user_img',default='user_img/default.png')



class noti(models.Model):
    title = models.CharField(max_length=36)
    body = models.CharField(max_length=120)
class balance(models.Model):
    user = models.ForeignKey(usertab,on_delete = models.CASCADE)
    blc = models.FloatField(default=0)
    referblc = models.FloatField(default=0)
    referbyblc = models.FloatField(default=0)
class payment(models.Model):
    brand = models.CharField(max_length=150)
class userurltable(models.Model):
    url = models.URLField(max_length=400)
    shorturl = models.URLField(max_length=5000,null=True)
    click = models.IntegerField(default=0)
    earning = models.FloatField(default=0)
    user = models.ForeignKey(usertab,on_delete = models.CASCADE,null=True)
class redeemtable(models.Model):
    def indiantime():
        return now() + timedelta(minutes = 330)
    user = models.ForeignKey(usertab,on_delete = models.CASCADE)
    paymentmode = models.ForeignKey(payment,on_delete=models.CASCADE)
    paddress = models.CharField(max_length=120)
    ifsc = models.CharField(max_length=120,null=True)
    amount = models.CharField(max_length=120)
    redeem_date = models.DateTimeField(default=indiantime )
    status = models.IntegerField(default=0)



class useraddress(models.Model):
    name = models.CharField(max_length=120)
    adr = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    zip = models.CharField(max_length=120)
    phone = models.CharField(max_length=120)
    user = models.ForeignKey(usertab,on_delete = models.CASCADE)
class codetable(models.Model):
    code = models.CharField(max_length=150)
class iptable(models.Model):
    ip = models.CharField(max_length=500)
    cookie = models.CharField(max_length=100,null=True)
    created_date = models.DateTimeField(default=now)

class static(models.Model):
    def indiantime():
        return now() + timedelta(minutes = 330)
    user = models.ForeignKey(usertab,on_delete = models.CASCADE)
    date = models.DateTimeField(default=indiantime )
    click = models.IntegerField(default=0)

class statictab(models.Model):
    def indiantime():
        date = now() + timedelta(minutes = 330)
        return date.date()
    user = models.ForeignKey(usertab,on_delete = models.CASCADE)
    date = models.DateField(default=indiantime)
    click = models.IntegerField(default=0)

class password_change(models.Model):
    user = models.ForeignKey(usertab,on_delete = models.CASCADE)
    key = models.CharField(max_length=128)

# class test(models.Model):
#     user = models.ForeignKey(usertab,on_delete = models.CASCADE)
#     key = models.CharField(max_length=128)