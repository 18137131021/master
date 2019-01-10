# -*- coding: utf-8 -*-
from common.mymako import render_mako_context, render_json

from home_application.unins.ESB import ESBComponentApi, ESBApi
import time
from django.db import transaction
from home_application import models
import json
import datetime


def job_exec(handle_user, t_script_data, contents_name, biz_id, records, script_content=None, script_params=None,script_type=None,module_name=None):
    response = {
    }
    ip_list = []
    ip_clouds = records.split(',')
    for ip_cloud_string in ip_clouds:
        ip_cloud = ip_cloud_string.split('|')
        dict = {'ip': ip_cloud[0], 'bk_cloud_id': ip_cloud[1]}
        ip_list.append(dict)
    try:
        job_exec_result = ESBComponentApi().fast_execute_script(biz_id, script_content=script_content,
                                                                ip_list=ip_list,script_param=script_params,script_type=script_type)
        print job_exec_result
        if job_exec_result['result']:
            job_instance_id = job_exec_result['data']['job_instance_id']
            job_instance_name = job_exec_result['data']['job_instance_name']
            response['result'] = True
            response['code'] = 0
            response['message'] = ''
            response['data'] = {}
            response['data']['job_instance_id'] = job_instance_id
            response['data']['job_instance_name'] = job_instance_name
            job_data = models.T_RECORDS_TASK.objects.create(
                handle_user=handle_user,
                t_script_data=t_script_data,
                ips=records,
                script_name=contents_name,
                biz_name=biz_id,
                script_instance_id=job_exec_result['data']['job_instance_id'],
                status=1,
                module_name=module_name,
            )
            while True:
                print
                job_data_result = ESBComponentApi().get_job_instance_log(biz_id, job_instance_id)
                if job_data_result['data'][0]['status'] == 3 or job_data_result['data'][0]['status'] == 4:
                    result = job_data_result['data'][0]['step_results']
                    for is_data in result:
                        ip = is_data['ip_logs'][0]['ip']
                        if is_data['ip_logs'][0]['log_content'] != u'':
                            job_content_log = is_data['ip_logs'][0]['log_content']
                            models.T_PC_LOG.objects.create(
                                execution_instance=job_data,
                                execution_ip=ip,
                                execution_content=job_content_log,
                                begin_time=datetime.datetime.now(),
                                script_name=job_data.script_name
                            )
                    job_data.script_instance_id = job_instance_id
                    job_data.save()
                    break

        else:
            response['result'] = False
            response['code'] = 1
            response['message'] = job_exec_result['message']
            response['data'] = {}
    except Exception as e:
        response['result'] = False
        response['code'] = 1
        response['message'] = e
        response['data'] = {}
    return response


def time_script():
    script_job = models.T_RECORDS_TASK.objects.filter(status=0, is_delete=0)
    if script_job.count() != 0:
        for job_data in script_job:
            script_data = job_data.t_script_data
            ip_list = []
            ip_clouds = script_data.ip_list_all.split(',')
            for ip_cloud_string in ip_clouds:
                ip_cloud = ip_cloud_string.split('|')
                dict_data = {'ip': ip_cloud[0], 'bk_cloud_id': ip_cloud[1]}
                ip_list.append(dict_data)
            script_params = None
            script_type = None
            job_exec_result = ESBComponentApi().fast_execute_script(script_data.select_business, script_content=script_data.script_data,
                                                                    ip_list=ip_list, script_param=script_params,
                                                                    script_type=script_type)
            if job_exec_result['result']:
                biz_id = job_data.biz_name
                job_instance_id = job_exec_result['data']['job_instance_id']
                while True:
                    job_data_result = ESBComponentApi().get_job_instance_log(biz_id, job_instance_id)
                    if job_data_result['data'][0]['status'] == 3 or job_data_result['data'][0]['status'] == 4:
                        result = job_data_result['data'][0]['step_results']
                        for is_data in result:
                            ip = is_data['ip_logs'][0]['ip']
                            if is_data['ip_logs'][0]['log_content'] != u'':
                                job_content_log = is_data['ip_logs'][0]['log_content']
                                models.T_PC_LOG.objects.create(
                                    execution_instance=job_data,
                                    execution_ip=ip,
                                    execution_content=job_content_log,
                                    begin_time=datetime.datetime.now(),
                                    script_name=job_data.script_name
                                )
                        job_data.script_instance_id = job_instance_id
                        job_data.save()
                        break


a = {"host_name":"rbtnode1",
     "ip":"ens192 192.168.51.51/24, virbr0 192.168.122.1/24",
     "sys_type":"CentOS Linux release 7.3.1611 (Core) ",
     "lang":"zh_CN.UTF-8",
     "mac":"ens192:00:50:56:9b:c5:44, virbr0:52:54:00:d4:50:d0, virbr0-nic:52:54:00:d4:50:d0"}


b = "Number found where operator expected at /tmp/bkjob/stepInstanceId_26901.pl line 12, near \"&amp;#39\"\n\t(Missing operator before 39?)\nOperator or semicolon missing before &amp;quot at /tmp/bkjob/stepInstanceId_26901.pl line 13.\nAmbiguous use of &amp; resolved as operator &amp; at /tmp/bkjob/stepInstanceId_26901.pl line 13.\nNumber found where operator expected at /tmp/bkjob/stepInstanceId_26901.pl line 22, near \"&amp;#39\"\n\t(Missing operator before 39?)\nScalar found where operator expected at /tmp/bkjob/stepInstanceId_26901.pl line 25, near \"$mac_add$arr_mac\"\n\t(Missing operator before $arr_mac?)\nScalar found where operator expected at /tmp/bkjob/stepInstanceId_26901.pl line 25, near \"]$arr_mac\"\n\t(Missing operator before $arr_mac?)\nBackslash found where operator expected at /tmp/bkjob/stepInstanceId_26901.pl line 29, near \"host_name\"\nBackslash found where operator expected at /tmp/bkjob/stepInstanceId_26901.pl line 29, near \"$Hostname\"\n\t(Missing operator before \\?)\nsyntax error at /tmp/bkjob/stepInstanceId_26901.pl line 12, near \"&amp;#39\"\nsyntax error at /tmp/bkjob/stepInstanceId_26901.pl line 22, near \"&amp;#39\"\nsyntax error at /tmp/bkjob/stepInstanceId_26901.pl line 23, near \"for\"\nsyntax error at /tmp/bkjob/stepInstanceId_26901.pl line 23, near \"0;\"\nsyntax error at /tmp/bkjob/stepInstanceId_26901.pl line 23, near \"&amp;lt\"\nsyntax error at /tmp/bkjob/stepInstanceId_26901.pl line 24, near \"2) \n\t\"\nsyntax error at /tmp/bkjob/stepInstanceId_26901.pl line 25, near \"$mac_add$arr_mac\"\nsyntax error at /tmp/bkjob/stepInstanceId_26901.pl line 26, near \"}\"\nsyntax error at /tmp/bkjob/stepInstanceId_26901.pl line 29, near \"host_name\"\nsyntax error at /tmp/bkjob/stepInstanceId_26901.pl line 29, near \"$Hostname\"\n/tmp/bkjob/stepInstanceId_26901.pl has too many errors.\n"