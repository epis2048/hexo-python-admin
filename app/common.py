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
from goto import with_goto
import sys
import time
import os

import public
import data


@with_goto
def detail(request):
    if not public.checklogin(request):
        return HttpResponseRedirect('/login')
    SiteData = data.Site()
    HexoData = data.Data()
    fid = request.GET.get('id')
    type = request.GET.get('type')
    if type == 'published':
        path = SiteData.getwebconf('HexoDir') + '\\source\\_posts\\' + fid
    elif type == 'drafts':
        path = SiteData.getwebconf('HexoDir') + '\\source\\_drafts\\' + fid
    elif type == 'page':
        path = SiteData.getwebconf('HexoDir') + '\\source\\' + fid + '\\index.md'
    else:
        path = SiteData.getwebconf('HexoDir') + '\\source\\_posts\\' + fid
    pinfo = ['', '', '', '']
    istext = False
    text = ''
    istag = False
    iscate = False
    tags = []
    catecories = []
    with open(path, 'r') as f:
        for line in f.readlines():
            p2 = line
            if istext == True:
                text = text + p2
            elif istag == True:
                if p2[0:4] == '  - ':
                    tags.append(p2[4:-1])
                else:
                    istag = False
                    goto .adjust
            elif iscate == True:
                if p2[0:4] == '  - ':
                    catecories.append(p2[4:-1])
                else:
                    #pass
                    iscate = False
                    goto .adjust
            else:
                label .adjust
                if p2 == '---\n':
                    istext = True
                elif p2[0:5] == 'title':
                    pinfo[0] = p2[7:-1]
                elif p2[0:6] == 'author':
                    pinfo[1] = p2[8:-1]
                elif p2[0:4] == 'date':
                    pinfo[2] = p2[6:-1]
                elif p2[0:4] == 'tags':
                    istag = True
                elif p2[0:10] == 'categories':
                    iscate = True

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
            'tags': tags,
            'catecories': catecories,
            'HexoDir': SiteData.getwebconf('HexoDir'),
            'year':datetime.now().year,
        }
    )

def ajax_content(request):
    if not public.checklogin(request):
        return HttpResponseRedirect('/login')
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
    elif type == 'page':
        path = SiteData.getwebconf('HexoDir') + '\\source\\' + fid + '\\index.md'
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
    if not public.checklogin(request):
        return HttpResponseRedirect('/login')
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
    elif type == 'page':
        path = SiteData.getwebconf('HexoDir') + '\\source\\' + fid + '\\index.md'
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
