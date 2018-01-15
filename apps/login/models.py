# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50,unique=True)
    nickname = models.CharField(max_length=50,null=False,default="")
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)