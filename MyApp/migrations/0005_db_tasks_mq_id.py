# Generated by Django 3.2.13 on 2023-03-05 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0004_db_django_task_mq'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_tasks',
            name='mq_id',
            field=models.IntegerField(default=0),
        ),
    ]