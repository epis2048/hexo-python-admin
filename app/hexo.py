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
    path = SiteData.getwebconf('HexoDir') + '/_config.yml'
    line = ''
    title = ''
    subtitle = ''
    author = ''
    with open(path, 'r') as f:
        for line in f.readlines():
            p2 = line
            if p2[0:6] == 'title:':
                title = p2[7:]
            elif p2[0:9] == 'subtitle:':
                subtitle = p2[10:]
            elif p2[0:7] == 'author:':
                author = p2[8:]

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/hexo/index.html',
        {
            'title':'Hexo基础',
            'title2': title,
            'subtitle': subtitle,
            'author': author,
            'staticurl': SiteData.getwebconf('StaticFile'),
            'year':datetime.now().year,
        }
    )

def url(request):
    if not public.checklogin(request):
        return HttpResponseRedirect('/login')
    SiteData = data.Site()
    path = SiteData.getwebconf('HexoDir') + '/_config.yml'
    line = ''
    url = ''
    root = ''
    permalink = ''
    with open(path, 'r') as f:
        for line in f.readlines():
            p2 = line
            if p2[0:4] == 'url:':
                url = p2[5:]
            elif p2[0:5] == 'root:':
                root = p2[6:]
            elif p2[0:10] == 'permalink:':
                permalink = p2[11:]

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/hexo/url.html',
        {
            'title':'Hexo基础',
            'url': url,
            'root': root,
            'permalink': permalink,
            'staticurl': SiteData.getwebconf('StaticFile'),
            'year':datetime.now().year,
        }
    )

def theme(request):
    if not public.checklogin(request):
        return HttpResponseRedirect('/login')
    SiteData = data.Site()
    path = SiteData.getwebconf('HexoDir') + '/_config.yml'
    line = ''
    theme = ''
    with open(path, 'r') as f:
        for line in f.readlines():
            p2 = line
            if p2[0:6] == 'theme:':
                theme = p2[7:-1]
    
    path2 = SiteData.getwebconf('HexoDir') + '/themes/'
    allthemes = os.listdir(path2)

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/hexo/theme.html',
        {
            'title':'Hexo基础',
            'theme': theme,
            'allthemes': allthemes,
            'staticurl': SiteData.getwebconf('StaticFile'),
            'year':datetime.now().year,
        }
    )

def edit(request):
    if not public.checklogin(request):
        return HttpResponseRedirect('/login')
    type = request.GET.get('type')
    SiteData = data.Site()
    path = SiteData.getwebconf('HexoDir') + '/_config.yml'
    lines = ''
    line = ''
    theme = ''
    with open(path, 'r') as f:
        for line in f.readlines():
            p2 = line
            if p2[0:6] == 'theme:':
                theme = p2[7:-1]
            if type == 'site':
                lines += p2
    if type == 'theme':
        path_theme = SiteData.getwebconf('HexoDir') + '/themes/' + theme + '/_config.yml'
        with open(path_theme, 'r') as f:
            for line in f.readlines():
                lines += line


    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/hexo/edit.html',
        {
            'title':'Hexo基础',
            'type': type,
            'content': lines,
            'staticurl': SiteData.getwebconf('StaticFile'),
            'year':datetime.now().year,
        }
    )

def publish(request):
    if not public.checklogin(request):
        return HttpResponseRedirect('/login')
    
    SiteData = data.Site()
    path = SiteData.getwebconf('HexoDir') + '/hexo-deploy.sh'
    p2 = ''

    with open(path, 'r') as f:
        for line in f.readlines():
            p2 += line.decode('utf-8')

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/hexo/publish.html',
        {
            'title':'发布',
            'p2': p2,
            'staticurl': SiteData.getwebconf('StaticFile'),
            'year':datetime.now().year,
        }
    )

def ajax_basic(request):
    if not public.checklogin(request):
        return HttpResponseRedirect('/login')
    msg = ''
    success = False

    title = unquote(str(request.POST.get('title'))).decode('utf-8')
    subtitle = unquote(str(request.POST.get('subtitle'))).decode('utf-8')
    author = unquote(str(request.POST.get('author'))).decode('utf-8')

    SiteData = data.Site()
    path = SiteData.getwebconf('HexoDir') + '/_config.yml'
    line = ''
    lines = ''

    with open(path, 'r') as f:
        for line in f.readlines():
            p2 = line.decode('utf-8')
            if p2[0:6] == 'title:':
                lines += 'title: ' + title + '\n'
            elif p2[0:9] == 'subtitle:':
                lines += 'subtitle: ' + subtitle + '\n'
            elif p2[0:7] == 'author:':
                lines += 'author: ' + author + '\n'
            else:
                lines += p2
    
    #msg = lines

    with open(path, 'w') as f:
        f.write(lines.encode('utf-8'))
    
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

def ajax_url(request):
    if not public.checklogin(request):
        return HttpResponseRedirect('/login')
    msg = ''
    success = False

    url = unquote(str(request.POST.get('url'))).decode('utf-8')
    root = unquote(str(request.POST.get('root'))).decode('utf-8')
    permalink = unquote(str(request.POST.get('permalink'))).decode('utf-8')

    SiteData = data.Site()
    path = SiteData.getwebconf('HexoDir') + '/_config.yml'
    line = ''
    lines = ''

    with open(path, 'r') as f:
        for line in f.readlines():
            p2 = line.decode('utf-8')
            if p2[0:4] == 'url:':
                lines += 'url: ' + url + '\n'
            elif p2[0:5] == 'root:':
                lines += 'root: ' + root + '\n'
            elif p2[0:10] == 'permalink:':
                lines += 'permalink: ' + permalink + '\n'
            else:
                lines += p2
    
    #msg = lines

    with open(path, 'w') as f:
        f.write(lines.encode('utf-8'))
    
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

def ajax_theme(request):
    if not public.checklogin(request):
        return HttpResponseRedirect('/login')
    msg = ''
    success = False

    theme = unquote(str(request.POST.get('theme'))).decode('utf-8')

    SiteData = data.Site()
    path = SiteData.getwebconf('HexoDir') + '/_config.yml'
    line = ''
    lines = ''

    with open(path, 'r') as f:
        for line in f.readlines():
            p2 = line.decode('utf-8')
            if p2[0:6] == 'theme:':
                lines += 'theme: ' + theme + '\n'
            else:
                lines += p2
    
    #msg = lines

    with open(path, 'w') as f:
        f.write(lines.encode('utf-8'))
    
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

def ajax_edit(request):
    if not public.checklogin(request):
        return HttpResponseRedirect('/login')
    msg = ''
    success = False

    type = request.GET.get('type')
    content = unquote(str(request.POST.get('content'))).decode('utf-8')

    SiteData = data.Site()
    if type == 'theme':
        path = SiteData.getwebconf('HexoDir') + '/_config.yml'
        with open(path, 'r') as f:
            for line in f.readlines():
                p2 = line
                if p2[0:6] == 'theme:':
                    theme = p2[7:-1]
                if type == 'site':
                    lines += p2
        path = SiteData.getwebconf('HexoDir') + '/themes/' + theme + '/_config.yml'
    elif type == 'site':
        path = SiteData.getwebconf('HexoDir') + '/_config.yml'
    
    with open(path, 'w') as f:
        f.write(content.encode('utf-8'))
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


def ajax_publish(request):
    if not public.checklogin(request):
        return HttpResponseRedirect('/login')
    
    msg = ''
    success = False
    SiteData = data.Site()
    path = SiteData.getwebconf('HexoDir')

    status = os.system('cd ' + path + ' && ' + 'hexo generate')
    msg = status

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/ajax.html',
        {
            'success':success,
            'msg':msg,
        }
    )

def ajax_delpublish(request):
    if not public.checklogin(request):
        return HttpResponseRedirect('/login')
    
    msg = ''
    success = False
    SiteData = data.Site()
    path = SiteData.getwebconf('HexoDir')

    status = os.system('cd ' + path + ' && ' + 'hexo clean')
    msg = status

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/ajax.html',
        {
            'success':success,
            'msg':msg,
        }
    )
