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
    SiteData = data.Site()
    HexoData = data.Data()
    bloginfo = []
    postlist = HexoData.Blogs_Get_List()
    for post in postlist:
        pinfo = ['', '', '', '']
        path = SiteData.getwebconf('HexoDir') + '\\source\\_posts\\' + post
        with open(path, 'r') as f:
            for line in f.readlines():
                p2 = line
                if p2 == '---\n':
                    break
                elif p2[0:5] == 'title':
                    pinfo[0] = p2[7:]
                elif p2[0:6] == 'author':
                    pinfo[1] = p2[8:]
                elif p2[0:4] == 'date':
                    pinfo[3] = p2[6:]
            pinfo[2] =  post
            bloginfo.append(pinfo)

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/post/index.html',
        {
            'title':'所有文章',
            'ConfigFile': SiteData.getwebconf('ConfigFile'),
            'staticurl': SiteData.getwebconf('StaticFile'),
            'bloginfo': bloginfo,
            'HexoDir': SiteData.getwebconf('HexoDir'),
            'year':datetime.now().year,
        }
    )

def detail(request):
    SiteData = data.Site()
    HexoData = data.Data()
    fid = request.GET.get('id')
    type = request.GET.get('type')
    if type == 'published':
        path = SiteData.getwebconf('HexoDir') + '\\source\\_posts\\' + fid
    elif type == 'drafts':
        path = SiteData.getwebconf('HexoDir') + '\\source\\_drafts\\' + fid
    else:
        path = SiteData.getwebconf('HexoDir') + '\\source\\_posts\\' + fid
    pinfo = ['', '', '', '']
    istext = False
    text = ''
    with open(path, 'r') as f:
        for line in f.readlines():
            p2 = line
            if istext == True:
                text = text + p2
            else:
                if p2 == '---\n':
                    istext = True
                elif p2[0:5] == 'title':
                    pinfo[0] = p2[7:]
                elif p2[0:6] == 'author':
                    pinfo[1] = p2[8:]
                elif p2[0:4] == 'date':
                    pinfo[2] = p2[6:]

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/post/detail.html',
        {
            'title': pinfo[0],
            'ConfigFile': SiteData.getwebconf('ConfigFile'),
            'staticurl': SiteData.getwebconf('StaticFile'),
            'fid': fid,
            'pinfo': pinfo,
            'text': text,
            'type': type,
            'HexoDir': SiteData.getwebconf('HexoDir'),
            'year':datetime.now().year,
        }
    )

def add(request):
    SiteData = data.Site()
    HexoData = data.Data()
    author = HexoData.getconfig('author')

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/post/add.html',
        {
            'title':'写文章',
            'author': author,
            'staticurl': SiteData.getwebconf('StaticFile'),
            'year':datetime.now().year,
        }
    )

def drafts(request):
    SiteData = data.Site()
    HexoData = data.Data()
    bloginfo = []
    postlist = HexoData.Drafts_Get_List()
    for post in postlist:
        pinfo = ['', '', '', '']
        path = SiteData.getwebconf('HexoDir') + '\\source\\_drafts\\' + post
        with open(path, 'r') as f:
            for line in f.readlines():
                p2 = line
                if p2 == '---\n':
                    break
                elif p2[0:5] == 'title':
                    pinfo[0] = p2[7:]
                elif p2[0:6] == 'author':
                    pinfo[1] = p2[8:]
                elif p2[0:4] == 'date':
                    pinfo[3] = p2[6:]
            pinfo[2] =  post
            bloginfo.append(pinfo)

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/post/drafts.html',
        {
            'title':'草稿箱',
            'ConfigFile': SiteData.getwebconf('ConfigFile'),
            'staticurl': SiteData.getwebconf('StaticFile'),
            'bloginfo': bloginfo,
            'HexoDir': SiteData.getwebconf('HexoDir'),
            'year':datetime.now().year,
        }
    )

def ajax_content(request):
    success = False
    msg = ''
    #reload(sys)
    #sys.setdefaultencoding('utf-8')
    SiteData = data.Site()
    fid = unquote(str(request.POST.get('fid'))).decode('utf-8')
    value = request.POST.get('value')
    type = request.GET.get('type')
    if type == 'published':
        path = SiteData.getwebconf('HexoDir') + '\\source\\_posts\\' + fid
    elif type == 'drafts':
        path = SiteData.getwebconf('HexoDir') + '\\source\\_drafts\\' + fid
    else:
        path = SiteData.getwebconf('HexoDir') + '\\source\\_posts\\' + fid
    ftitle = ''
    with open(path, 'r+') as f:
        for line in f.readlines():
            ftitle += line
            if line == '---\n':
                break
    content = ftitle.decode('utf-8') + value.decode('utf-8')
    with open(path, 'wb') as f:
        f.write(unquote(content.encode('utf-8')))
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

def ajax_info(request):
    msg = ''
    success = False
    title = unquote(str(request.POST.get('title'))).decode('utf-8')
    author = unquote(str(request.POST.get('author'))).decode('utf-8')
    time = unquote(str(request.POST.get('time'))).decode('utf-8')
    SiteData = data.Site()
    HexoData = data.Data()
    fid = unquote(str(request.POST.get('fid'))).decode('utf-8')
    type = request.GET.get('type')
    if type == 'published':
        path = SiteData.getwebconf('HexoDir') + '\\source\\_posts\\' + fid
    elif type == 'drafts':
        path = SiteData.getwebconf('HexoDir') + '\\source\\_drafts\\' + fid
    else:
        path = SiteData.getwebconf('HexoDir') + '\\source\\_posts\\' + fid

    lines = []
    with open(path, 'r') as f:
        for line in f.readlines():
            lines.append(line.decode('utf-8'))
    i = 0

    
    for i in range(len(lines)):
        if lines[i][0:5] == 'title':
            lines[i] = 'title: ' + title + '\n'
            i += 1
        elif lines[i][0:6] == 'author':
            lines[i] = 'author: ' + author + '\n'
            i += 1
        elif lines[i][0:4] == 'date':
            lines[i] = 'date: ' + time + '\n'
            i += 1
        elif lines[i] == '---\n':
            break
    s=''.join(lines)
    msg = s
    
    with open(path, 'w') as f:
        f.write(s.encode('utf-8'))
    
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

def ajax_add(request):
    msg = ''
    success = False

    title = unquote(str(request.POST.get('title'))).decode('utf-8')
    author = unquote(str(request.POST.get('author'))).decode('utf-8')
    filename = unquote(str(request.POST.get('filename'))).decode('utf-8')
    date = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )

    stext = 'title: ' + title +'\nauthor: ' + author + '\ndate: ' + date + '\ntags: []\ncategories: []\n---\n'
    SiteData = data.Site()
    path = SiteData.getwebconf('HexoDir') + '\\source\\_drafts\\' + filename

    with open(path, 'w') as f:
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

def ajax_publish(request):
    msg = ''
    success = False
    lines = ''

    fid = unquote(str(request.POST.get('fid'))).decode('utf-8')
    SiteData = data.Site()
    path = SiteData.getwebconf('HexoDir') + '\\source\\_drafts\\' + fid
    path2 = SiteData.getwebconf('HexoDir') + '\\source\\_posts\\' + fid

    with open(path, 'r') as f:
        for line in f.readlines():
            lines += line.decode('utf-8')
    with open(path2, 'w') as f:
        f.write(lines.encode('utf-8'))
    os.remove(path)
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
    msg = ''
    success = False

    fid = unquote(str(request.POST.get('fid'))).decode('utf-8')
    SiteData = data.Site()
    type = request.GET.get('type')
    if type == 'published':
        path = SiteData.getwebconf('HexoDir') + '\\source\\_posts\\' + fid
    elif type == 'drafts':
        path = SiteData.getwebconf('HexoDir') + '\\source\\_drafts\\' + fid
    else:
        path = SiteData.getwebconf('HexoDir') + '\\source\\_posts\\' + fid
    
    os.remove(path)
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
