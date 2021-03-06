# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from django.shortcuts import render,render_to_response
from app.models import *
from django.db.models.aggregates import Count
from django import forms
from django.http import HttpResponse,HttpResponseServerError,HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from login.models import *
# Create your views here.
catagory_list = ['行业资讯','人工智能','大数据','数据库','编程语言','前端','容器技术','运维','安全']

def page_not_found(request):
    return render(request, '404.html')


def page_error(request):
    return render(request, '500.html')


def permission_denied(request):
    return render(request, '403.html')

def write_blog(request):
    username = request.COOKIES.get('username', '')
    catagory1 = catagory_list
    if not username:
        return HttpResponseRedirect('/blog/login')
    return render(request, 'write_blog.html', locals())

def n_blog(request):
    R = request.POST
    username = request.COOKIES.get('username', '')
    if not username:
        return HttpResponseServerError("请登录")
    try:
        title,editor,tag,catagory = R['title'],R['editor'],R['tag'],R['catagory']
    except:
        return HttpResponseServerError("请选择分类")
    try:
        t = Blog.objects.get(title=title)
        return HttpResponseServerError("标题重复，请换个标题")
    except:
        pass
    try:
        assert all([title,editor,tag])
    except:
        return HttpResponseServerError("缺少输入信息")

    tag_List = []
    for i in str(tag).split(','):
        tag_List.append(i)

    '''不存在分类则创建'''

    try:
        c = Catagory.objects.get(name=catagory)
    except:
        c = Catagory(name=catagory)
        c.save()
    '''获取分类ID'''
    ID = Catagory.objects.values('id').filter(name=c)[0]['id']

    try:
        b = Blog(title=title,author=username,content=editor,catagory_id=ID)
        b.save()
    except:
        return HttpResponseServerError("error")

    b = Blog.objects.get(title=title)

    for i in tag_List:
        t, _ = Tag.objects.get_or_create(name=i)
        if t not in b.tags.all():
            b.tags.add(t)
            b.save()

    return HttpResponse("hello")

def e_blog(request):
    R = request.POST
    blogid = R['ID']

    username = request.COOKIES.get('username', '')
    if not username:
        return HttpResponseServerError("请登录")
    try:
        title,editor,tag,catagory = R['title'],R['editor'],R['tag'],R['catagory']
    except:
        return HttpResponseServerError("请选择分类")
    '''
    try:
        t = Blog.objects.get(title=title)
        return HttpResponseServerError("标题重复，请换个标题")
    except:
        pass
    '''
    try:
        assert all([title,editor,tag])
    except:
        return HttpResponseServerError("缺少输入信息")
    print request.get_full_path()


    tag_List = []
    for i in str(tag).split(','):
        tag_List.append(i)



    try:
        c = Catagory.objects.get(name=catagory)
    except:
        c = Catagory(name=catagory)
        c.save()

    ID = Catagory.objects.values('id').filter(name=c)[0]['id']

    try:
        obj = Blog.objects.get(id=blogid)
        obj.title = title
        obj.content = editor
        obj.catagory_id = ID
        obj.save()
        #b = Blog(title=title,author=username,content=editor,catagory_id=ID)
        #b.save()
    except:
        return HttpResponseServerError("error")


    b = Blog.objects.get(id=blogid)
    #tags_before = blog.tags.all()
    #b.tags.remove(tags_before)

    for i in tag_List:
        t, _ = Tag.objects.get_or_create(name=i)
        if t not in b.tags.all():
            b.tags.add(t)
            b.save()

    return HttpResponse("hello")

def listblog(request):
    #username = request.COOKIES.get('username', '')
    try:
        username = request.COOKIES.get('username', '')
        userinfo = User.objects.get(username=username)
    except:
        return HttpResponseRedirect('/blog/login')
    type = request.GET.get('type')
    category = request.GET.get('category')
    tagname = request.GET.get('tag')
    if type == 'all':
        blog = Blog.objects.all().order_by('-created')
    if type == 'category':
        blog = Blog.objects.filter(catagory__name__iexact=category).order_by('-created')
    if type == 'tag':
        tag = Tag.objects.get(name=tagname)
        blog = tag.blog_set.all().order_by('-created')
    if type == 'myblog':
        blog = Blog.objects.filter(author=username).all().order_by('-created')
    tag = Tag.objects.all()
    category_list = Catagory.objects.annotate(num_posts=Count('blog'))
    '''分页'''
    paginator = Paginator(blog,6)
    page = request.GET.get('page',1)
    currentPage = int(page)
    #currentPage = page
    try:
        print(page)
        blog = paginator.page(page)
    except PageNotAnInteger:
        blog = paginator.page(1)
    except EmptyPage:
        blog = paginator.page(paginator.num_pages)
    return render(request, 'listblog.html', locals())

class CommentForm(forms.Form):
    content = forms.CharField(required=True,max_length=150,
        widget=forms.Textarea
        (attrs={
        'rows': 10,
        'cols': 120,
        'class': 'form-group',
        'style': 'height: 20em;'}))

#@register.filter(name='filter')
#def change_textarea_to_return(source_string):
#    res=source_string.replace("\\r\\n","<br>")
#    return res

def blog(request,blogid):
    #username = request.COOKIES.get('username', '')
    try:
        username = request.COOKIES.get('username', '')
        userinfo = User.objects.get(username=username)
    except:
        return HttpResponseRedirect('/blog/login')
    tag = Tag.objects.all()
    blog = Blog.objects.all().order_by('-created')
    category_list = Catagory.objects.annotate(num_posts=Count('blog'))
    blogid = request.path.split('=')[1]
    myblog = Blog.objects.get(id=blogid)

    comment_user = User.objects.get(username=username)
    nickname =  comment_user.nickname
    '''获取评论'''
    comments = myblog.comment_set.all()
    '''发表评论'''
    obj = CommentForm()
    if request.method == 'POST':
        userinput = CommentForm(request.POST)
        if userinput.is_valid():
            data = userinput.clean()
        else:
            pass
            error_msg = userinput.errors
            #return render(request,'blog.html',{'obj': obj,'errors':error_msg, })
    #return render(request,'blog.html',{'obj':obj, })
        content = data['content']
    try:
        c = Comment(name=nickname,content=content,blog=myblog)
        c.save()
    except:
        pass
    '''评论分页'''
    '''获取博客的所有评论'''
    #comments = Comment.objects.filter(blog=myblog).all()
    '''
    paginator = Paginator(comments,5)
    page = request.GET.get('page',1)
    #currentPage = int(page)
    currentPage = page
    try:
        print(page)
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
        #return HttpResponseServerError("error")
        '''
    return render(request,'blog.html',locals())

def comments(request,blogid,page):
    try:
        username = request.COOKIES.get('username', '')
        userinfo = User.objects.get(username=username)
    except:
        return HttpResponseRedirect('/blog/login')
    myblog = Blog.objects.get(id=blogid)
    comments = myblog.comment_set.all().order_by('-created')
    # 生成paginator对象,定义每页显示10条记录
    paginator = Paginator(comments,5)

    # 从前端获取当前的页码数,默认为1
    #page = request.GET.get('page', 1)

    # 把当前的页码数转换成整数类型
    #currentPage = int(page)
    currentPage = int(page)
    try:
        print(page)
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    return render(request, 'comments.html', locals())

def myblog(request):
    try:
        username = request.COOKIES.get('username', '')
        userinfo = User.objects.get(username=username)
    except:
        return HttpResponseRedirect('/blog/login')
    action = request.GET.get('action')
    blog = Blog.objects.filter(author=username).all().order_by('-created')
    tag = Tag.objects.all()
    category_list = Catagory.objects.annotate(num_posts=Count('blog'))

    if action == 'edit':
        blogid = request.get_full_path().split('=')[2]

        return HttpResponseRedirect('/list/edit?action=edit&id=%s'%blogid)
    if action == 'dele':
        blogid = request.GET.get('id')
        try:
            Blog.objects.get(id=blogid).delete()
            return HttpResponseRedirect('/list/myblog')
        except:
            Blog.objects.filter(id=blogid).delete()
            return HttpResponseRedirect('/list/myblog')
    return render(request, 'myblog.html', locals())


def edit(request):
    try:
        username = request.COOKIES.get('username', '')
    except:
        return HttpResponseRedirect('/blog/login')
    blogid = request.get_full_path().split('=')[2]
    blog = Blog.objects.get(id=blogid)
    tags = blog.tags.all()
    catagory = blog.catagory.name
    catagory1 = catagory_list

    str = ''
    import string
    for i in tags:
        str += ','+i.name
    list = str.strip(string.punctuation)
    return render(request, 'edit.html', locals())


def search(request):
    import string
    from datetime import datetime
    try:
        username = request.COOKIES.get('username', '')
        userinfo = User.objects.get(username=username)
    except:
        return HttpResponseRedirect('/blog/login')
    keyword = request.GET.get('keyword')
    type = request.GET.get('type')
    startime = datetime.now()
    '''打开当前页面不输出任何结果,避免查询'''
    if not keyword:
        return render(request, 'search.html')
    '''特殊字符不能搜索'''
    ascii_letters = string.punctuation
    for i in keyword:
        if i in ascii_letters:
            return render(request, 'search.html')
    if type == 'content':
        blog = Blog.objects.filter(content__icontains=keyword)
        num = blog.count()
    if type == 'title':
        blog = Blog.objects.filter(title__icontains=keyword)
        num = blog.count()
    if type == 'catagory':
        try:
            catagory = Catagory.objects.get(name=keyword)
            blog = catagory.blog_set.all()
            num = blog.count()
        except:
            pass
    if type == 'tag':
        try:
            tag = Tag.objects.get(name=keyword)
            blog = tag.blog_set.all()
            num = blog.count()
        except:
            pass
    if type == 'author':
        blog = Blog.objects.filter(author__icontains=keyword)
        num = blog.count()

    endtime = datetime.now()

    searchtime = (endtime-startime).microseconds

    try:
        paginator = Paginator(blog,2)

        # 从前端获取当前的页码数,默认为1
        page = request.GET.get('page', 1)
        # 把当前的页码数转换成整数类型
        currentPage = int(page)
        try:
            blog = paginator.page(page)
        except PageNotAnInteger:
            blog = paginator.page(1)
        except EmptyPage:
            blog = paginator.page(paginator.num_pages)
    except:
        pass
    return render(request,'search.html',locals())

def userinfo(request):
    try:
        username = request.COOKIES.get('username', '')
        userinfo = User.objects.get(username=username)
    except:
        return HttpResponseRedirect('/blog/login')
    return render(request,'userinfo.html',locals())

def edituser(request):
    import hashlib
    from django.contrib.auth.hashers import make_password
    try:
        username = request.COOKIES.get('username', '')
    except:
        return HttpResponseRedirect('/blog/login')
    pwd_now = User.objects.get(username=username).password
    '''获取表单信息'''
    pwd_input = request.POST['password1']
    pwd_new = request.POST['password2']
    nickname = request.POST['nickname']
    email = request.POST['email']
    tmpass = make_password(pwd_input,'a','pbkdf2_sha256')
    if pwd_now != tmpass:
        return HttpResponseServerError("当期密码不正确")
    new_pass = make_password(pwd_new,'a','pbkdf2_sha256')

    if new_pass == tmpass:
        return HttpResponseServerError("原始密码与新密码一致")
    try:
        User.objects.filter(username=username).update(
            password=new_pass,nickname=nickname,email=email
        )
    except:
        return HttpResponseServerError("重置失败")
    return HttpResponse("hello")