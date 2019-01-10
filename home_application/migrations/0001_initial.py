# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='T_C_SCRIPT',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u811a\u672c\u540d\u79f0')),
                ('script_content', models.TextField(null=True, verbose_name='\u811a\u672c\u5185\u5bb9')),
            ],
            options={
                'verbose_name': '\u811a\u672c\u6587\u4ef6',
            },
        ),
        migrations.CreateModel(
            name='T_PC_LOG',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('script_name', models.CharField(max_length=500, null=True, verbose_name='\u811a\u672c\u540d\u79f0')),
                ('execution_ip', models.CharField(max_length=500, null=True, verbose_name='\u4e3b\u673aip')),
                ('execution_content', models.CharField(max_length=500, null=True, verbose_name='\u4e3b\u673a\u5185\u5bb9')),
                ('begin_time', models.DateTimeField(null=True, verbose_name='\u5f55\u5165\u65f6\u95f4')),
            ],
            options={
                'db_table': 't_pc_log',
                'verbose_name': '\u83b7\u53d6\u811a\u672c\u6267\u884c\u8bb0\u5f55',
            },
        ),
        migrations.CreateModel(
            name='T_RECORDS_TASK',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('script_name', models.CharField(max_length=500, null=True, verbose_name='\u811a\u672c\u540d\u79f0')),
                ('ips', models.CharField(max_length=500, null=True, verbose_name='\u6267\u884c\u4efb\u52a1ip')),
                ('biz_name', models.CharField(max_length=500, null=True, verbose_name='\u4e1a\u52a1\u540d\u79f0')),
                ('module_name', models.CharField(max_length=50, null=True, verbose_name='\u6a21\u5757name')),
                ('script_instance_id', models.CharField(max_length=50, null=True, verbose_name='\u811a\u672c\u5b9e\u4f8bid')),
                ('status', models.SmallIntegerField(default=0, verbose_name='\u72b6\u6001')),
                ('is_delete', models.IntegerField(default=0, verbose_name='\u662f\u5426\u5220\u9664')),
                ('handle_user', models.CharField(max_length=500, verbose_name='\u6267\u884c\u4eba')),
            ],
            options={
                'db_table': 't_records_task',
                'verbose_name': '\u83b7\u53d6\u811a\u672c\u6267\u884c\u6570\u636e',
            },
        ),
        migrations.CreateModel(
            name='T_SCRIPT_DATA',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip_list_all', models.CharField(max_length=500, null=True, verbose_name='\u6267\u884c\u4efb\u52a1ip')),
                ('contents_name', models.CharField(max_length=500, null=True, verbose_name='\u811a\u672c\u540d\u79f0')),
                ('select_business', models.CharField(max_length=500, null=True, verbose_name='\u4e1a\u52a1id')),
                ('script_type', models.IntegerField(null=True, verbose_name='\u811a\u672c\u7c7b\u578b')),
                ('module_name', models.CharField(max_length=500, null=True, verbose_name='\u6a21\u5757\u540d\u79f0')),
                ('script_data', models.CharField(max_length=3000, null=True, verbose_name='\u811a\u672c\u5185\u5bb9')),
            ],
            options={
                'db_table': 't_script_data',
                'verbose_name': '\u811a\u672c\u6267\u884c\u5b9e\u4f8b\u811a\u672c',
            },
        ),
        migrations.AddField(
            model_name='t_records_task',
            name='t_script_data',
            field=models.ForeignKey(verbose_name='\u5bf9\u5e94\u811a\u672c\u6267\u884c\u5b9e\u4f8b\u811a\u672c', to='home_application.T_SCRIPT_DATA'),
        ),
        migrations.AddField(
            model_name='t_pc_log',
            name='execution_instance',
            field=models.ForeignKey(verbose_name='\u5bf9\u5e94\u5b9e\u4f8b', to='home_application.T_RECORDS_TASK'),
        ),
    ]
