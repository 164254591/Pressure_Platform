# -*- coding:utf-8 -*-
import re
import subprocess
import threading
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
    script_model = request.POST.get('script_model')
    myFile = request.FILES.get('script_file')
    file_name = str(myFile)
    fp = open('scripts/' + script_model + '/' + file_name, 'wb+')
    for i in myFile.chunks():
        fp.write(i)
    fp.close()
    return HttpResponse('')


# 获取脚本列表
def get_script_list(request):
    script_list = []
    for d in ['other', 'python', 'go']:
        script_list += [d + '/' + i for i in os.listdir(os.path.join('scripts', d))]

    # script_list = os.listdir('scripts')
    # print(script_list)
    return HttpResponse(json.dumps(script_list))


def get_tasks(request):
    tasks = list(DB_tasks.objects.all().values())[::-1]
    return HttpResponse(json.dumps(tasks))


def add_tasks(request):
    des = request.GET['des']
    project_id = request.GET['project_id']
    new = DB_tasks.objects.create(des=des, project_id=int(project_id), stime=str(time.strftime('%Y-%m-%d %H:%M:%S')))
    mq_id = mq_producer(DB_django_task_mq, topic='yace', message={'task_id': new.id})
    new.mq_id = mq_id
    new.save()
    return get_tasks(request)


def play(mq):
    def doit(filepath):
        subprocess.call('python ' + filepath + ' mq_id=' + str(mq.id), shell=True)

    def one_round(filepath, num):
        ts = []
        for n in range(int(num)):
            t = threading.Thread(target=doit, args=(filepath,))
            t.setDaemon(True)
            ts.append(t)
        for t in ts:
            t.start()
        for t in ts:
            t.join()
        print('----------结束了一轮次的压测计划--------------')

    message = json.loads(mq.message)
    task_id = message['task_id']
    task = DB_tasks.objects.filter(id=int(task_id))
    task.update(status='压测中')
    # --------------
    # 根据任务关联的项目id，去数据库找出这项目的所有内容
    project = DB_Projects.objects.filter(id=int(task[0].project_id))[0]
    scripts = eval(project.scripts)
    print(scripts)
    for step in project.plan.split(','):
        script = scripts[int(step.split('-')[0])]  # 脚本序号
        filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts', script)
        print(filepath)

        trs = []
        if '+' in step:  # 【无限增压】
            round = 100  # 安全值
        elif '_' in step:  # 瞬时增压
            round = int(step.split('-')[2]) * int(step.count('_') + 1)
        else:
            round = int(step.split('-')[2])  # 轮次
        for r in range(round):
            if '/' in step:  # 【阶梯压测】
                mid = step.split('-')[1]
                num = int(mid.split('/')[0]) + (int(mid.split('/')[1]) - int(mid.split('/')[0])) / (round - 1) * r
            elif '+' in step:
                mid = step.split('-')[1]
                num = int(mid.split('+')[0]) + int(mid.split('+')[1]) * r
            elif '_' in step:  # 瞬时增压
                mid = step.split('-')[1]
                mid = mid.split('_')
                num = int(mid[int(r / int(step.split('-')[2]))])
                print(num)
            else:
                num = int(step.split('-')[1])  # 并发数
            tr = threading.Thread(target=one_round, args=(filepath, num))
            tr.setDaemon(True)
            trs.append(tr)
        # tr是轮
        for tr in trs:
            # 路障
            now_task = DB_tasks.objects.filter(id=task_id)[0]
            if now_task.stop == True:
                break
            tr.start()
            time.sleep(5)
        for tr in trs:
            tr.join()
        print('-------------结束了一阶段的压测计划---------------')

    # ---------------
    task.update(status='已结束')


# 终止压测任务
def stop_task(request):
    def s_mac():
        ts = subprocess.check_output('ps -ef |grep mq_id=%s |grep -v "grep"' % str(mq_id), shell=True)
        for t in str(ts).split('mq_id=' + str(mq_id)):
            s = re.findall(r'\b(\d+?)\b', t)[:3]
            if s:
                pid = max([int(i) for i in s])
                subprocess.call('kill -9 ' + str(pid))

    def s_win():
        ts = subprocess.check_output('wmic process where caption="python.exe" get processid,commandline', shell=True)
        for t in str(ts).split(r'\n'):
            if 'mq_id=' + str(mq_id) in t:
                pid = re.findall(r'\b(\d+?)\b', t)[-1]
                subprocess.call('taskkill /T /F /PID %s' % pid, shell=True)

    task_id = request.GET['id']
    task = DB_tasks.objects.filter(id=int(task_id))[0]
    mq_id = task.mq_id
    if task.status == '队列中':
        DB_django_task_mq.objects.filter(id=int(mq_id)).delete()
        task.status = '队列中结束'
        task.save()
    if task.status == '压测中':
        task.stop = True
        task.save()

        for j in range(1000):
            # while True:
            now_task = DB_tasks.objects.filter(id=task_id)[0]
            if now_task.status == '压测中':
                try:
                    s_mac()
                    s_win()
                except:
                    break
                finally:
                    now_task.status = '异常数据结束'
                    now_task.save()
            else:
                break
    else:
        HttpResponse(json.dumps({"code": 300, "data": [], 'Message': '任务已结束'}), content_type='application/json')
    return HttpResponse(json.dumps({"code": 200, "data": [], 'Message': '终止成功'}), content_type='application/json')
