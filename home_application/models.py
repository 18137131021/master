# -*- coding: utf-8 -*-

from django.db import models
import datetime
from django.utils import timezone


class T_C_SCRIPT(models.Model):
    name = models.CharField(verbose_name=u"脚本名称", max_length=100)
    script_content = models.TextField(verbose_name=u"脚本内容", null=True)

    class Meta:
        verbose_name = u"脚本文件"

class T_SCRIPT_DATA(models.Model):
    ip_list_all = models.CharField(verbose_name=u"执行任务ip", max_length=500, null=True)
    contents_name = models.CharField(verbose_name=u"脚本名称", max_length=500, null=True)
    select_business = models.CharField(verbose_name=u"业务id", max_length=500, null=True)
    script_type = models.IntegerField(verbose_name=u"脚本类型", null=True)
    module_name = models.CharField(verbose_name=u"模块名称", max_length=500, null=True)
    script_data = models.CharField(verbose_name=u"脚本内容", max_length=3000, null=True)
    class Meta:
        verbose_name=u"脚本执行实例脚本"
        db_table = 't_script_data'

class T_RECORDS_TASK(models.Model):
    t_script_data = models.ForeignKey(T_SCRIPT_DATA, verbose_name=u"对应脚本执行实例脚本")
    script_name = models.CharField(verbose_name=u"脚本名称", max_length=500, null=True)
    ips = models.CharField(verbose_name=u"执行任务ip", max_length=500, null=True)
    biz_name = models.CharField(verbose_name=u"业务名称", max_length=500, null=True)
    module_name = models.CharField(verbose_name=u"模块name", max_length=50, null=True)
    script_instance_id = models.CharField(verbose_name=u"脚本实例id", max_length=50, null=True)
    # 0: 待获取数据；1：获取数据中；:2：获取数据成功；3：获取数据失败
    status = models.SmallIntegerField(verbose_name=u"状态", default=0)
    is_delete = models.IntegerField(verbose_name=u"是否删除", default=0)
    handle_user = models.CharField(verbose_name=u"执行人", max_length=500)

    class Meta:
        verbose_name=u"获取脚本执行数据"
        db_table = 't_records_task'


class T_PC_LOG(models.Model):
    execution_instance = models.ForeignKey(T_RECORDS_TASK, verbose_name=u"对应实例")
    script_name = models.CharField(verbose_name=u"脚本名称", max_length=500, null=True)
    execution_ip = models.CharField(verbose_name=u"主机ip", max_length=500, null=True)
    execution_content = models.CharField(verbose_name=u"主机内容", max_length=500, null=True)
    begin_time = models.DateTimeField(verbose_name=u"录入时间", null=True)

    class Meta:
        verbose_name=u"获取脚本执行记录"
        db_table = 't_pc_log'

