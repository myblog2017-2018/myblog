# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,render_to_response
from login.models import *
from django import forms
from django.http import HttpResponse,HttpResponseServerError,HttpResponseRedirect
import re
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def login(request):
    return render(request,'login.html',locals())
'''
def index(request):
    username = request.COOKIES.get('username', '')
    #password = request.COOKIES.get('password', '')
    request.session["username"] = username
    #request.session['password'] = password

    sss = request.session.get("username", "")
    #bbb = request.session.get("password", "")
    if username:
        return render(request, 'index.html', locals())
    else:
        return HttpResponseRedirect('login')
'''
def login_post(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            assert all([username,password])
        except:
            return HttpResponseServerError("请输入用户密码")
        try:
            user = User.objects.values('username').filter(username=username)[0]['username']
            pwd = User.objects.values('password').filter(username=username)[0]['password']
        except:
            return HttpResponseServerError("账号不存在")
        from django.contrib.auth.hashers import check_password
        if not check_password(password,pwd):
        #if password != pwd:
            return HttpResponseServerError("密码不正确")

        response = HttpResponseRedirect('/list/listblog/?type=all')
        response.set_cookie('username',username,36000)
        #response.set_cookie('password',password, 3600)
        return response
    #return render(request,'index.html',locals())

def regist_post(request):
    if request.method == 'POST':
        q = request.POST
        username,nickname,password,password1,email = q['username'],q['nickname'],q['password'],q['password1'],q['email']
        try:
            assert all([username,password,password1,email,password == password1])
        except:
            return HttpResponseServerError("字段必填&密码需要匹配")
        if username >= u'\u4e00' and username <= u'\u9fa5':
            return HttpResponseServerError("用户名不支持中文")
        try:
            User.objects.values('username').filter(username=username)[0]['username']
            return HttpResponseServerError("用户名已注册")
        except:
            pass
        try:
            User.objects.values('email').filter(email=email)[0]['email']
            return HttpResponseServerError("邮箱已注册")
        except:
            pass
    str = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
    if not re.match(str, email):
        return HttpResponseServerError("邮箱格式错误")
    try:
        from django.contrib.auth.hashers import make_password
        tmppass = make_password(password,'a','pbkdf2_sha256')
        sql = User(username=username,password=tmppass,email=email,nickname=nickname)
        sql.save()
        response = HttpResponseRedirect('/list/listblog/?type=all')
        response.set_cookie('username', username, 3600)
        #response.set_cookie('password', password, 3600)
        return response
    except:
        return HttpResponseServerError('内部错误')

def forget_post(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        try:
            user = User.objects.values('username').filter(username=username)[0]['username']
        except:
            return HttpResponseServerError("账号未注册")
        str = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
        if not re.match(str,email):
            return HttpResponseServerError("邮箱格式错误")
        if not username or not email:
            return HttpResponseServerError('必填项')
        try:
            User.objects.values('email').filter(email=email)[0]['email']
        except:
            return HttpResponseServerError("邮箱未注册")
        email_db = User.objects.values('email').filter(username=username)[0]['email']
        if email != email_db:
            return HttpResponseServerError("用户邮箱不匹配")
        import hashlib
        u = hashlib.sha1(username).hexdigest()
        e = hashlib.sha1(email).hexdigest()
        send_mail(
            '博客密码找回邮件',
            'http://182.254.146.59/blog/forget_reset/%s&%s'%(u,e),
            'xxxxx.com',
            [email],
            fail_silently=True
        )

        return HttpResponse("邮件已发送，请登录邮箱重置密码")

def forget_reset(request,user,email):
    return render(request,'forget_reset.html',locals())

def reset_post(request):
    username = request.POST['username']
    pass1 = request.POST['password1']
    pass2 = request.POST['password2']
    md5 = request.POST['test']
    if pass1 != pass2:
        return HttpResponseServerError("密码不一致")
    from django.contrib.auth.hashers import make_password
    import hashlib
    tmpPass = make_password(pass1, 'a', 'pbkdf2_sha256')
    u = hashlib.sha1(username).hexdigest()
    if u != md5:
        return HttpResponseServerError("请输入正确用户")
    try:
        User.objects.filter(username=username).update(password=tmpPass)
    except:
        return HttpResponseServerError("重置失败")

    return HttpResponse("data")
