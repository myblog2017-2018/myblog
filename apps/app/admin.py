# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from app.models import *
from django.db import models
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# Register your models here.
#admin.site.register(models.Band)
#admin.site.register(models.Member)
admin.site.register([Catagory,Tag,Blog,Comment,Reply])