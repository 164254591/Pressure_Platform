# -*- coding:utf-8 -*-
import time

from django.shortcuts import render

import json
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from MyApp.models import *
import os
from django_task_mq import mq_producer


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
    return HttpResponse(json.dumps(projects), content_type='application/json')


# 默认新增
def add_project(request):
    DB_Projects.objects.create()
    return get_projects(request)


# 删除
def delete_project(request):
    project_id = request.GET['project_id']
    DB_Projects.objects.filter(id=project_id).delete()
    return get_projects(request)


# 项目详情
def get_project_detail(request):
    project_id = request.GET['project_id']
    project_detail = list(DB_Projects.objects.filter(id=project_id).values())[0]
    project_detail['scripts'] = eval(project_detail['scripts'])
    return HttpResponse(json.dumps(project_detail))


def save_project(request):
    form = json.loads(request.body.decode('utf-8'))
    id = form['id']
    DB_Projects.objects.filter(id=id).update(**form)
    return HttpResponse('')


# 上传文件
def upload_script_file(request):
    myFile = request.FILES.get('script_file')
    file_name = str(myFile)
    fp = open('scripts/' + file_name, 'wb+')
    for i in myFile.chunks():
        fp.write(i)
    fp.close()
    return HttpResponse('')


# 获取脚本列表
def get_script_list(request):
    script_list = os.listdir('scripts')
    # print(script_list)
    return HttpResponse(json.dumps(script_list))


def get_tasks(request):
    tasks = list(DB_tasks.objects.all().values())[::-1]
    return HttpResponse(json.dumps(tasks))


def add_tasks(request):
    des = request.GET['des']
    project_id = request.GET['project_id']
    new = DB_tasks.objects.create(des=des, project_id=int(project_id), stime=str(time.strftime('%Y-%m-%d %H:%M:%S')))
    mq_producer(DB_django_task_mq, topic='yace', message={'task_id': new.id})
    return get_tasks(request)


def play(message):
    message = json.loads(message)
    task_id = message['task_id']
    DB_tasks.objects.filter(id=int(task_id)).update(status='压测中')
    # --------------
    time.sleep(10)
    # ---------------
    DB_tasks.objects.filter(id=int(task_id)).update(status='已结束')
