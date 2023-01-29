from django.db import models


# Create your models here.
class DB_Projects(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True, default='new project')
    scripts = models.CharField(max_length=500, null=True, blank=True, default='')
    plan = models.CharField(max_length=500, null=True, blank=True, default='')

    def __str__(self):
        return self.name
