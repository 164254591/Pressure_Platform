# -*- coding:utf-8 -*-
from django.shortcuts import render

import json
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from MyApp.models import *


# Create your views here.
# 登录函数
def login_account(request):
    form_data = json.loads(request.body)
    # 用这个用户/密码去数据库表中查找，如果找到就返回用户名，否则返回None
    USER = auth.authenticate(username=form_data['username'], password=form_data['password'])
    # print(USER)
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
    try:
        user = User.objects.create_user(username=form_data['username'], password=form_data['password'])
        user.save()
        res = {"code": 0, 'message': '注册成功'}
        return HttpResponse(json.dumps(res), content_type='application/json')
    except:
        res = {"code": 1, 'message': '注册失败'}
        return HttpResponse(json.dumps(res), content_type='application/json')


def get_echarts_data(request):
    res = {
        'legend_data': ['项目1', '项目2', '项目3'],
        'xAxis_data': ['9-15', '9-16', '9-17', '9-18'],
        'series': [
            {'name': '项目1', 'data': [3, 9, 5, 8, 7], 'type': 'line'},
            {'name': '项目2', 'data': [6, 2, 6, 9, 5], 'type': 'line'},
        ],
    }

    return HttpResponse(json.dumps(res), content_type='application/json')


# 查询
def get_projects(request):
    projects = list(DB_Projects.objects.all().values())  # 返回一个列表内容为字典[{},{}]
    return HttpResponse(json.dumps(projects))


# 默认新增
def add_project(request):
    DB_Projects.objects.create()
    return get_projects(request)


# 删除
def delete_project(request):
    project_id = request.GET['project_id']
    DB_Projects.objects.filter(id=project_id).delete()
    return get_projects(request)
