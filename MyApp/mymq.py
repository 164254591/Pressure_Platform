import os, sys, django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%s.settings' % 'Pressure_Platform')  # 引号中请输入您的setting父级目录名
django.setup()  # 启动django服务
from MyApp.models import DB_django_task_mq
from django_task_mq import mq_consumer
from MyApp.views import play

mq_consumer(DB_django_task_mq, play, topic='yace')
