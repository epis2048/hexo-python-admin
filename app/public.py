# encoding: utf-8  

import hashlib
import yaml
import data

def sha1pass(uid, upass):
    uidmd5 = hashlib.md5(str(uid)).hexdigest()
    uidmd5 = uidmd5
    upasssha1 = hashlib.sha1(upass).hexdigest()
    step1 = hashlib.sha1(uidmd5 + upasssha1).hexdigest()
    step2 = hashlib.sha1(step1).hexdigest()
    return step2

def checklogin(request):
    username= ''
    password= ''

    try:
        username = request.COOKIES["username"]
        password = request.COOKIES["password"]
    except:
        return False
    
    SiteData = data.Site()
    path = SiteData.getwebconf('ConfigFile') + '/_config.yaml'
    config = []
    with open(path, 'r') as f:
        config = yaml.load(f)
    
    username2 = config['account']['username']
    password2 = config['account']['password']

    if username2 == username and password == password2:
        return True
    else:
        return False
