# encoding: utf-8  

import hashlib

def sha1pass(uid, upass):
    uidmd5 = hashlib.md5(str(uid)).hexdigest()
    uidmd5 = uidmd5
    upasssha1 = hashlib.sha1(upass).hexdigest()
    step1 = hashlib.sha1(uidmd5 + upasssha1).hexdigest()
    step2 = hashlib.sha1(step1).hexdigest()
    return step2

