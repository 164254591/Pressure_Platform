# -*- coding:utf-8 -*-
from django.shortcuts import render

import json
from django.http import HttpResponse


# Create your views here.

def login_account(request):
    form_data = json.loads(request.body)
    username = form_data['username']
    password = form_data['password']
    print(username, password)
    res = {"code": 0, 'message': '登录成功'}
    return HttpResponse(json.dumps(res), content_type='application/json')
