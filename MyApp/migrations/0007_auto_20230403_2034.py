# Generated by Django 3.2.13 on 2023-04-03 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0006_db_tasks_stop'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='db_projects',
            name='scripts',
        ),
        migrations.AlterField(
            model_name='db_projects',
            name='plan',
            field=models.CharField(blank=True, default='[]', max_length=500, null=True),
        ),
    ]
