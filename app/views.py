# encoding: utf-8  
"""
Definition of views.
"""
#settings
import webset

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import template 
from urllib import unquote, urlencode
import requests
import hashlib
import json
import yaml
from django.urls import reverse

import public
import data




def index(request):
    SiteDate = data.Site()
    if not public.checklogin(request):
        return HttpResponseRedirect('/login')
    
    https = SiteDate.getwebconf('https')

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'首页',
            'ConfigFile': SiteDate.getwebconf('ConfigFile'),
            'https': https,
            'staticurl': SiteDate.getwebconf('StaticFile'),
            'HexoDir': SiteDate.getwebconf('HexoDir'),
            'year':datetime.now().year,
        }
    )

def login(request):
    SiteDate = data.Site()
    https = SiteDate.getwebconf('https')

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/login.html',
        {
            'title':'登录',
            'https': https,
            'staticurl': SiteDate.getwebconf('StaticFile'),
            'year':datetime.now().year,
        }
    )

def logout(request):
    response = HttpResponseRedirect(reverse('login'))
    response.delete_cookie('username')
    response.delete_cookie('password')
    return response

def ajax_login(request):
    msg = ''
    success = False

    SiteData = data.Site()
    path = SiteData.getwebconf('ConfigFile') + '/_config.yaml'
    config = []
    with open(path, 'r') as f:
        config = yaml.load(f)

    username = unquote(str(request.POST.get('username'))).decode('utf-8')
    password = unquote(str(request.POST.get('password'))).decode('utf-8')
    if password == '' or password == 'None':
        password = ''
    else:
        password = str(public.sha1pass(username, password))
    
    if str(username) == str(config['account']['username']):
        if str(password) == str(config['account']['password']):
            success = True
        else:
            msg = '密码错误'
    else:
        msg = '查无此人'
    
    assert isinstance(request, HttpRequest)
    response = render(
        request,
        'app/ajax.html',
        {
            'success':success,
            'msg':msg,
        }
    )
    response.set_cookie('username',username)
    response.set_cookie('password',password)
    return response
