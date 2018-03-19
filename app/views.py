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

import public
import data




def index(request):
    SiteDate = data.Site()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'首页',
            'ConfigFile': SiteDate.getwebconf('ConfigFile'),
            'staticurl': SiteDate.getwebconf('StaticFile'),
            'HexoDir': SiteDate.getwebconf('HexoDir'),
            'year':datetime.now().year,
        }
    )
