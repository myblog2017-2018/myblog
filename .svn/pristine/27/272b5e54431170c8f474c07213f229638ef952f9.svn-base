"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'^write_blog$',write_blog),
    url(r'^n_blog$',n_blog),
    url(r'^e_blog$',e_blog),
    url(r'^listblog/$',listblog),
    url(r'^blog&id=(.+)$',blog),
    url(r'^myblog$',myblog),
    url(r'^edit$',edit),
    url(r'^comments&id=(.+)&page=(.+)$',comments),
    url(r'^search$',search),
]

handler403 = permission_denied
handler404 = page_not_found
handler500 = page_error