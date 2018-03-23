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
import yaml
import json
from django.urls import reverse
import sys
import time
import os

import public
import data



def index(request):
    if not public.checklogin(request):
        return HttpResponseRedirect('/login')
    SiteData = data.Site()
    path = SiteData.getwebconf('ConfigFile') + '/_config.yaml'
    config = []
    with open(path, 'r') as f:
        config = yaml.load(f)


    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/admin/index.html',
        {
            'title':'管理密码',
            'config': config,
            'staticurl': SiteData.getwebconf('StaticFile'),
            'year':datetime.now().year,
        }
    )

def config(request):
    if not public.checklogin(request):
        return HttpResponseRedirect('/login')
    SiteData = data.Site()
    path = SiteData.getwebconf('ConfigFile') + '/_config.yaml'
    config = []
    with open(path, 'r') as f:
        config = yaml.load(f)

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/admin/config.html',
        {
            'title':'系统配置',
            'config': config,
            'staticurl': SiteData.getwebconf('StaticFile'),
            'year':datetime.now().year,
        }
    )

def ajax_setpw(request):
    msg = ''
    success = False
    if not public.checklogin(request):
        return HttpResponseRedirect('/login')

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
    
    config['account']['password'] = password
    config['account']['username'] = username

    text = yaml.dump(config, default_flow_style=False)
    
    with open(path, 'w') as f:
        f.write(text.encode('utf-8'))
    
    success = True


    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/ajax.html',
        {
            'success':success,
            'msg':msg,
        }
    )

def ajax_basic(request):
    msg = ''
    success = False
    if not public.checklogin(request):
        return HttpResponseRedirect('/login')

    SiteData = data.Site()
    path = SiteData.getwebconf('ConfigFile') + '/_config.yaml'
    config = []
    with open(path, 'r') as f:
        config = yaml.load(f)
    
    admindir = unquote(str(request.POST.get('admindir'))).decode('utf-8')
    hexodir = unquote(str(request.POST.get('hexodir'))).decode('utf-8')
    staticurl = unquote(str(request.POST.get('staticurl'))).decode('utf-8')
    https = unquote(str(request.POST.get('https'))).decode('utf-8')
    
    config['basic']['admindir'] = admindir
    config['basic']['hexodir'] = hexodir
    config['basic']['staticurl'] = staticurl
    if https == 'True':
        config['https'] = True
    else:
        config['https'] = False

    text = yaml.dump(config, default_flow_style=False)
    
    with open(path, 'w') as f:
        f.write(text.encode('utf-8'))
    
    success = True


    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/ajax.html',
        {
            'success':success,
            'msg':msg,
        }
    )
