# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# Create your models here.
class Catagory(models.Model):
    """
    博客分类
    """
    name = models.CharField(max_length=30,unique=True,verbose_name = u'名称')

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    """
    博客标签
    """
    name = models.CharField(max_length=16,verbose_name = u'名称')

    def __unicode__(self):
        return self.name

class Blog(models.Model):
    """
    博客
    """
    title = models.CharField(max_length=32,verbose_name = u'标题')
    author = models.CharField(max_length=16,verbose_name = u'作者')
    content = models.TextField(verbose_name = u'博客正文')
    created = models.DateTimeField(auto_now_add=True,verbose_name = u'发布时间')
    catagory = models.ForeignKey(Catagory,verbose_name = u'分类')
    tags = models.ManyToManyField(Tag,verbose_name = u'标签')

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    """
    评论
    """
    blog = models.ForeignKey(Blog,verbose_name='博客')
    name = models.CharField(max_length=16,verbose_name = u'称呼')
    content = models.CharField(max_length=240,verbose_name = u'内容')
    created = models.DateTimeField(auto_now_add=True,verbose_name = u'发布时间')

    def __unicode__(self):
        return self.content

class Reply(models.Model):
    """
    回复评论
    """
    comment = models.ForeignKey(Comment,verbose_name='回复评论')
    name = models.CharField(max_length=16,verbose_name = u'称呼')
    content = models.CharField(max_length=240,verbose_name = u'内容')
    created = models.DateTimeField(auto_now_add=True,verbose_name = u'发布时间')

    def __unicode__(self):
        return self.content