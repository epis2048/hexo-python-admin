# coding=utf-8

import MySQLdb


def connectdb():
    #print('连接到mysql服务器...')
    # 打开数据库连接
    # 用户名:hp, 密码:Hp12345.,用户名和密码需要改成你自己的mysql用户名和密码，并且要创建数据库TESTDB，并在TESTDB数据库中创建好表Student
    #db = MySQLdb.connect("127.0.0.1","root","root.","pyblog",3306)
    #print('连接上了!')
    return db

db = connectdb()
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s " % data