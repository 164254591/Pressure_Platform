from django.db import models


# Create your models here.
class DB_Projects(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True, default='new project')
    # scripts = models.CharField(max_length=500, null=True, blank=True, default='[]')
    plan = models.CharField(max_length=500, null=True, blank=True, default='[]')

    def __str__(self):
        return self.name


class DB_tasks(models.Model):
    stime = models.CharField(max_length=30, null=True, blank=True, default='')
    des = models.CharField(max_length=30, null=True, blank=True, default='')
    project_id = models.IntegerField(default=0)
    status = models.CharField(max_length=10, null=True, blank=True, default='队列中')  # 队列中，压测中，已结束
    mq_id = models.IntegerField(default=0)
    stop = models.BooleanField(default=False)  # 终止状态

    def __str__(self):
        return self.des


class DB_django_task_mq(models.Model):
    topic = models.CharField(max_length=100, null=True, blank=True, default="")
    message = models.TextField(default="{}")
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.topic
