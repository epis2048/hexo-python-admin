# encoding: utf-8  

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

def checkadmin(request):
    db=pypyodbc.win_connect_mdb(DBFILE)
    curser = db.cursor()
    try:
        scode = request.COOKIES["user_scode"]
    except:
        return True
    getscode = ''
    curser.execute("select * from robot_member_scode where scode = '"+scode+"' order by id desc")
    result = curser.fetchall()
    for row in result:
        getscode = row[2]
        scodetime = row[4]
    if getscode == '':
        return True
    else:
        sec = (datetime.now() - scodetime).seconds
        if sec >= 1800:
            return False
        else:
            return False

def checkscode(request):
    scode = request.COOKIES["user_scode"]
    db=pypyodbc.win_connect_mdb(DBFILE)
    curser = db.cursor()
    curser.execute("select * from robot_member_scode where scode = '"+scode+"' order by id desc")
    result = curser.fetchall()
    for row in result:
        scodetime = row[4]
    sec = (datetime.now() - scodetime).seconds
    if sec >= 1800:
        return True
    else:
        dt = datetime.now()
        d2 = str(dt.year) + '/' + str(dt.month) + '/' + str(dt.day) + ' ' + str(dt.hour) + ':' + str(dt.minute) + ':' + str(dt.second)
        curser.execute("update robot_member_scode set lastview = '" + str(d2) + "' where scode = '"+scode+"' ")
        db.commit()
        return False

def getlastdata(table, where, field):
    if where == '':
        where = where
    else:
        where = " where " + where
    db=pypyodbc.win_connect_mdb(DBFILE)
    curser = db.cursor()
    sql = "select top 1 " + field + " from " + table + where + " order by id desc"
    curser.execute(sql)
    result = curser.fetchall()
    t = ''
    for row in result:
        t = row[0]
    return t

def sha1pass(uid, upass):
    uidmd5 = hashlib.md5(str(uid)).hexdigest()
    uidmd5 = uidmd5[0:16]
    upasssha1 = hashlib.sha1(upass).hexdigest()
    step1 = hashlib.sha1(uidmd5 + upasssha1).hexdigest()
    step2 = hashlib.sha1(step1).hexdigest()
    return step2

def getwxtoken(tokenname):
    db=pypyodbc.win_connect_mdb(DBFILE)
    curser = db.cursor()
    sql = "select top 1 str, updatatime, secret from robot_wx_accesstoken where tokenname = '" + tokenname + "' "
    curser.execute(sql)
    result = curser.fetchall()
    t1 = ''
    t2 = ''
    secret = ''
    for row in result:
        t1 = row[0]
        t2 = row[1]
        secret = row[2]
    sec = (datetime.now() - t2).seconds
    day = (datetime.now() - t2).days
    if int(sec) < 7100 and day < 0.9:
        return str(t1)
    else:
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + WXCROPID + "&corpsecret=" + secret
        content=requests.get(url).content
        #return content
        gettoken = json.loads(content)
        token = gettoken['access_token']
        dt = datetime.now()
        d2 = str(dt.year) + '/' + str(dt.month) + '/' + str(dt.day) + ' ' + str(dt.hour) + ':' + str(dt.minute) + ':' + str(dt.second)
        sql = "update robot_wx_accesstoken set str = '" + token + "', updatatime = '" + d2 + "' where tokenname = '" + tokenname + "' "
        curser.execute(sql)
        db.commit()
        return token

def addviewlog(request):
    db=pypyodbc.win_connect_mdb(DBFILE)
    curser = db.cursor()
    scode = request.COOKIES["user_scode"]
    uid = ''
    curser.execute("select * from robot_member_scode where scode = '"+scode+"' order by id desc")
    result = curser.fetchall()
    for row in result:
        uid = str(row[1])
    ip = ''
    useragent = ''
    data_get = ' '
    viewurl = ''
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    useragent = request.META.get('HTTP_USER_AGENT')
    viewurl = request.get_full_path()
    db=pypyodbc.win_connect_mdb(LOGDBFILE)
    curser = db.cursor()
    sql = "insert into robot_log_admin_view (uid, uip, useragent, viewurl, data_get) values (?, ?, ?, ?, ?)"
    curser.execute(sql, (uid, ip, useragent, viewurl, data_get))
    db.commit()
    return True

def addajaxlog(request):
    db=pypyodbc.win_connect_mdb(DBFILE)
    curser = db.cursor()
    scode = request.COOKIES["user_scode"]
    uid = ''
    curser.execute("select * from robot_member_scode where scode = '"+scode+"' order by id desc")
    result = curser.fetchall()
    for row in result:
        uid = str(row[1])
    ip = ''
    useragent = ''
    data_get = ' '
    data_post = ''
    viewurl = ''
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    useragent = request.META.get('HTTP_USER_AGENT')
    viewurl = request.get_full_path()
    db=pypyodbc.win_connect_mdb(LOGDBFILE)
    curser = db.cursor()
    sql = "insert into robot_log_admin_ajax (uid, uip, useragent, act, data_get, data_post) values (?, ?, ?, ?, ?, ?)"
    curser.execute(sql, (uid, ip, useragent, viewurl, data_get, data_post))
    db.commit()
    return True

def getuid(request):
    scode = request.COOKIES["user_scode"]
    uid = '0'
    db=pypyodbc.win_connect_mdb(DBFILE)
    curser = db.cursor()
    curser.execute("select * from robot_member_scode where scode = '"+scode+"' order by id desc")
    result = curser.fetchall()
    for row in result:
        uid = str(row[1])
    return uid

def get_site_config(setname):
    setvalue = ''
    db=pypyodbc.win_connect_mdb(DBFILE)
    curser = db.cursor()
    curser.execute("select setvalue from robot_public_settings where setname = '"+setname+"' order by id desc")
    result = curser.fetchall()
    for row in result:
        setvalue = str(row[0])
    return setvalue
