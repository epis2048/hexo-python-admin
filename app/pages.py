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
    HexoData = data.Data()

    pagelist = HexoData.Pages_Get_List()
    pageinfo = []
    for page in pagelist:
        pinfo = ['', '', '']
        path = SiteData.getwebconf('HexoDir') + '\\source\\' + page + '\\index.md'
        if os.path.exists(path):
            with open(path, 'r') as f:
                for line in f.readlines():
                    p2 = line
                    if p2 == '---\n':
                        break
                    elif p2[0:5] == 'title':
                        pinfo[0] = p2[7:]
                    elif p2[0:4] == 'date':
                        pinfo[1] = p2[6:]
                pinfo[2] = page
            pageinfo.append(pinfo)


    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/page/index.html',
        {
            'title':'所有页面',
            'ConfigFile': SiteData.getwebconf('ConfigFile'),
            'staticurl': SiteData.getwebconf('StaticFile'),
            'pageinfo': pageinfo,
            'HexoDir': SiteData.getwebconf('HexoDir'),
            'year':datetime.now().year,
        }
    )

def add(request):
    if not public.checklogin(request):
        return HttpResponseRedirect('/login')
    SiteData = data.Site()
    HexoData = data.Data()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/page/add.html',
        {
            'title':'添加文章',
            'staticurl': SiteData.getwebconf('StaticFile'),
            'year':datetime.now().year,
        }
    )

def ajax_add(request):
    if not public.checklogin(request):
        return HttpResponseRedirect('/login')
    msg = ''
    success = False

    title = unquote(str(request.POST.get('title'))).decode('utf-8')
    filename = unquote(str(request.POST.get('filename'))).decode('utf-8')
    date = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )

    stext = 'title: ' + title +'\ndate: ' + date + '\n---\n'
    SiteData = data.Site()
    path = SiteData.getwebconf('HexoDir') + '\\source\\' + filename + '\\'
    path2 = SiteData.getwebconf('HexoDir') + '\\source\\' + filename + '\\index.md'

    if not os.path.exists(path):
        os.mkdir(path)

    with open(path2, 'w') as f:
        f.write(stext.encode('utf-8'))
    
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


def ajax_del(request):
    if not public.checklogin(request):
        return HttpResponseRedirect('/login')
    msg = ''
    success = False

    fid = unquote(str(request.POST.get('fid'))).decode('utf-8')
    SiteData = data.Site()
    path = SiteData.getwebconf('HexoDir') + '\\source\\' + fid + '\\'
    path2 = SiteData.getwebconf('HexoDir') + '\\source\\' + fid + '\\index.md'
    
    os.remove(path2)
    os.rmdir(path)
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
