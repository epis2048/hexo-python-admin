# -*- encoding=utf-8 -*-
from django import template 
import pypyodbc

DBFILE = 'Driver={Microsoft Access Driver (*.mdb,*.accdb)};DBQ=G:\\website\\2nkrobot\\databases\\robot.mdb'
register = template.Library()

@register.filter(name='getuserbyid')
def getuserbyid(adminid):
    #str2 = DBFILE
    db=pypyodbc.win_connect_mdb(DBFILE)
    curser = db.cursor()
    retname = ''
    #struid = str(uid)
    curser.execute("select realname, nickname, usershow from robot_member where id = "+str(adminid)+" order by id desc")
    result = curser.fetchall()
    for row in result:
        realname = row[0]
        nickname = row[1]
        usershow = row[2]
    if usershow == 1:
        retname = realname
    elif usershow == 2:
        retname = nickname
    elif usershow == 3:
        retname = nickname + '(' + realname + ')'
    elif usershow == 4:
        retname = realname + '(' + nickname + ')'
    else:
        retname = realname
    return retname

@register.filter(name='getproitembyid')
def getproitembyid(itemid):
    #str2 = DBFILE
    db=pypyodbc.win_connect_mdb(DBFILE)
    curser = db.cursor()
    itemname = ''
    #struid = str(uid)
    curser.execute("select itemname from robot_project_item where id = "+str(itemid)+" order by id desc")
    result = curser.fetchall()
    for row in result:
        itemname = row[0]
    return itemname

@register.filter(name='getproitemlinkbyid')
def getproitemlinkbyid(itemid):
    #str2 = DBFILE
    db=pypyodbc.win_connect_mdb(DBFILE)
    curser = db.cursor()
    itemlink = ''
    #struid = str(uid)
    curser.execute("select itemlink from robot_project_item where id = "+str(itemid)+" order by id desc")
    result = curser.fetchall()
    for row in result:
        itemlink = row[0]
    return itemlink

@register.filter(name='getboardtype')
def getboardtype(types):
    if types == 'TEXT':
        return '文本'
    elif types == 'LINK':
        return '链接'
    else:
        return ''

@register.filter(name='scodesmall')
def scodesmall(scode):
    return scode[0:64] + "..."

@register.filter(name='geteleitemgroupbyid')
def geteleitemgroupbyid(itemid):
    #str2 = DBFILE
    db=pypyodbc.win_connect_mdb(DBFILE)
    curser = db.cursor()
    groupname = ''
    #struid = str(uid)
    curser.execute("select groupname from robot_element_item_group where id = "+str(itemid)+" order by id desc")
    result = curser.fetchall()
    for row in result:
        groupname = row[0]
    return groupname


@register.filter(name='makestr')
def makestr(str1):
    return str(str1)
