# encoding: utf-8  
"""
Definition of views.
"""
#2nksettings
import webset
DBFILE = str(webset.DBFILE)
AUTHURL = str(webset.AUTHURL)
OAURL = str(webset.OAURL)
STATICURL = str(webset.STATICURL)
MGRURL = str(webset.MGRURL)
ISDEBUG = bool(webset.ISDEBUG)
WXCROPID = str(webset.WXCROPID)
LOGDBFILE = str(webset.LOGDBFILE)
IURL = str(webset.IURL)

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import pypyodbc
from django import template 
from urllib import unquote, urlencode
import requests
import hashlib
import json

import public



def contact(request):
    msg = ''
    success = False
    uid = ''
    email = ''
    qq = ''
    phone = ''
    try:
        uid = public.getuid(request)
        email = str(request.POST.get('email'))
        qq = str(request.POST.get('qq'))
        phone = str(request.POST.get('phone'))
        if str(phone) == 'None' or str(qq) == 'None' or str(email) == 'None':
            msg = '不可以留空！'
            success = False
        else:
            try:
                db=pypyodbc.win_connect_mdb(DBFILE)
                curser = db.cursor()
                sql = "update robot_member set email = ?, qq = ?, phone = ? where id = " + str(uid)
                curser.execute(sql,(email, qq, phone))
                db.commit()
                msg = ''
                success = True
            except:
                msg = '信息错误！'
                success = False
    except:
        msg = '缺少信息！'
        success = False
    
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/ajax.html',
        {
            'success':success,
            'msg':msg,
        }
    )

def profile(request):
    msg = ''
    success = False
    userdes = ''
    nickname = ''
    username = ''
    usershow = 1
    try:
        uid = public.getuid(request)
        userdes = unquote(str(request.POST.get('userdes'))).decode('utf-8')
        nickname = unquote(str(request.POST.get('nickname'))).decode('utf-8')
        usershow = int(request.POST.get('usershow'))
        if str(username) == 'None':
            msg = '不可以留空！'
            success = False
        else:
            try:
                db=pypyodbc.win_connect_mdb(DBFILE)
                curser = db.cursor()
                sql = "update robot_member set userdes = ?, nickname = ?, usershow = ? where id = " + str(uid)
                curser.execute(sql,(userdes, nickname, str(usershow)))
                db.commit()
                msg = ''
                success = True
            except:
                msg = '信息错误！'
                success = False
    except:
        msg = '缺少信息！'
        success = False
    
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/ajax.html',
        {
            'success':success,
            'msg':msg,
        }
    )

def password(request):
    msg = ''
    success = False
    oldpass = ''
    newpass = ''
    newpass2 = ''
    try:
        uid = public.getuid(request)
        oldpass = str(request.POST.get('oldpass'))
        newpass = str(request.POST.get('newpass'))
        newpass2 = str(request.POST.get('newpass2'))
        if oldpass == '' or newpass == '' or newpass2 == '':
            msg = '请检查您的输入！'
            success = False
        else:
            if newpass == newpass2:
                passold = public.sha1pass(uid, oldpass)
                db=pypyodbc.win_connect_mdb(DBFILE)
                curser = db.cursor()
                curser.execute("select top 1 userpass from robot_member_password where uid = "+uid+" order by id desc")
                result = curser.fetchall()
                for row in result:
                    passold2 = row[0]
                if passold == passold2:
                    password = public.sha1pass(uid, newpass)
                    sql = "insert into robot_member_password (uid, userpass) values (?, ?)"
                    curser.execute(sql,(uid, password))
                    db.commit()
                    msg = ''
                    success = True
                else:
                    msg = '旧密码不对'
                    success = False
            else:
                msg = '两次输入不一致'
                success = False
    except:
        msg = '缺少信息！'
        success = False
    
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/ajax.html',
        {
            'success':success,
            'msg':msg,
        }
    )

def username(request):
    msg = ''
    success = False
    userpass = ''
    username = ''
    try:
        uid = public.getuid(request)
        userpass = str(request.POST.get('userpass'))
        username = str(request.POST.get('username'))
        if userpass == '' or username == '':
            msg = '请检查您的输入！'
            success = False
        else:
            passold = public.sha1pass(uid, userpass)
            db=pypyodbc.win_connect_mdb(DBFILE)
            curser = db.cursor()
            curser.execute("select top 1 userpass from robot_member_password where uid = "+uid+" order by id desc")
            result = curser.fetchall()
            for row in result:
                passold2 = row[0]
            if passold == passold2:
                sql = "update robot_member set username = ?, [group] = ? where id = " + str(uid)
                curser.execute(sql,(username, ''))
                db.commit()
                msg = ''
                success = True
            else:
                msg = '旧密码不对'
                success = False
    except:
        msg = '缺少信息！'
        success = False
    
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/ajax.html',
        {
            'success':success,
            'msg':msg,
        }
    )
