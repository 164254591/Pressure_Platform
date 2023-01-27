# -*- coding:utf-8 -*-
from django.shortcuts import render

import json
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User


# Create your views here.
# 登录函数
def login_account(request):
    form_data = json.loads(request.body)
    # 用这个用户/密码去数据库表中查找，如果找到就返回用户名，否则返回None
    USER = auth.authenticate(username=form_data['username'], password=form_data['password'])
    print(USER)
    if USER:
        auth.login(request, USER)
        request.session['username'] = form_data['username']
        res = {"code": 0, 'message': '登录成功'}
        return HttpResponse(json.dumps(res), content_type='application/json')
    else:
        res = {"code": 1, 'message': '登录失败'}
        return HttpResponse(json.dumps(res), content_type='application/json')


# 注册函数
def register_account(request):
    form_data = json.loads(request.body)
