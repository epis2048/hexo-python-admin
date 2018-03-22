# encoding: utf-8  
"""
Definition of urls for DjangoWebProject1.
"""

from datetime import datetime
from django.conf.urls import url,handler404
import django.contrib.auth.views
from django.http import HttpResponse

import app.forms
import app.views
import app.common
import app.blogs
import app.pages
import app.admin



# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [

    url(r'^$', app.views.index, name='index'),
    url(r'^login$', app.views.login, name='login'),
    url(r'^ajax_login$', app.views.ajax_login, name='ajax_login'),

    #文章
    url(r'^blogs$', app.blogs.index, name='blog_index'),
    url(r'^drafts$', app.blogs.drafts, name='blog_drafts'),
    url(r'^blog_add$', app.blogs.add, name='blog_add'),
    url(r'^ajax_blog_add$', app.blogs.ajax_add, name='ajax_blog_add'),
    url(r'^ajax_blog_publish$', app.blogs.ajax_publish, name='ajax_blog_publish'),
    url(r'^ajax_blog_del$', app.blogs.ajax_del, name='ajax_blog_del'),
    url(r'^ajax_blog_tag_add$', app.blogs.ajax_tag_add, name='ajax_blog_tag_add'),
    url(r'^ajax_blog_tag_del$', app.blogs.ajax_tag_del, name='ajax_blog_tag_del'),
    url(r'^ajax_blog_cate_add$', app.blogs.ajax_cate_add, name='ajax_blog_cate_add'),
    url(r'^ajax_blog_cate_del$', app.blogs.ajax_cate_del, name='ajax_blog_cate_del'),

    #页面
    url(r'^pages$', app.pages.index, name='page_index'),
    url(r'^page_add$', app.pages.add, name='page_add'),
    url(r'^ajax_page_add$', app.pages.ajax_add, name='ajax_page_add'),
    url(r'^ajax_page_del$', app.pages.ajax_del, name='ajax_page_del'),

    #管理设置
    url(r'^admin_account$', app.admin.index, name='admin_index'),
    url(r'^admin_config$', app.admin.config, name='admin_config'),
    url(r'^ajax_admin_setpw$', app.admin.ajax_setpw, name='ajax_admin_setpw'),
    url(r'^ajax_admin_basic$', app.admin.ajax_basic, name='ajax_admin_basic'),

    #公用
    url(r'^detail$', app.common.detail, name='blog_detail'),
    url(r'^ajax_content$', app.common.ajax_content, name='ajax_blog_content'),
    url(r'^ajax_info$', app.common.ajax_info, name='ajax_blog_info'),

]

#handler500 = "app.views.notfound"
