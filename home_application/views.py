# -*- coding: utf-8 -*-
from account.decorators import login_exempt
from common.mymako import render_mako_context
from unins import ESB
from common.mymako import render_json
import platform
from django.db.models import Q, QuerySet
from home_application.celery_tasks import async_run_script, get_time
from django.views.decorators.http import require_http_methods
import json
from home_application import models
import base64
import HTMLParser
import datetime, time
from django.db import transaction
import random
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.db import connection
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def home(request):
    """
    首页
    """
    result = job_data(request)
    all_pid = result.get('data')
    print all_pid
    all_script = models.T_C_SCRIPT.objects.all()
    all_script_task = models.T_RECORDS_TASK.objects.filter(is_delete=0)
    all_user = models.T_RECORDS_TASK.objects.filter(is_delete=0)
    all_data_user = []
    for user in all_user:
        all_data_user.append(user.handle_user)
    all_data_user = set(all_data_user)
    print all_data_user
    # all_user.group_by = ['handle_user']
    # all_user = QuerySet(query=all_user, model=models.T_RECORDS_TASK)
    content_data = {}
    for script in all_script:
        script_id = script.id
        content_data[script_id] = script.name
    return render_mako_context(request, '/home_application/demo_one.html', {'all_pid': all_pid,
                                                                            'content_data': content_data,
                                                                            'all_script_task': all_script_task,
                                                                            'all_user': all_data_user})

def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')


def demo_one(request):
    """
    demo页面
    """
    return render_mako_context(request, '/home_application/demo_one.html')


def job_data(request):
    """
    获取当前用户下的业务
    :param request:
    :return:
    """

    response = {}

    try:
        result = ESB.ESBApi(request).search_business()
        print result
        if result['result']:
            response['result'] = True
            response['code'] = 0
            response['message'] = 'success'
            response['data'] = {}
            if len(result['data']['info'])>0:
                for item in result['data']['info']:
                    dic = {}
                    dic[item['bk_biz_id']] = item['bk_biz_name']
                    response['data'].update(dic)
            else:
                response['result'] = True
                response['code'] = 0
                response['message'] = u'该用户下无业务'
                response['data'] = {}
        else:
            response = result

    except Exception, e:
        response['result'] = False
        response['code'] = 1
        response['message'] = u'获取业务列表失败：%s' % e
        response['data'] = {}

    return response


def search_pc(request, biz_id):
    """
    获取当前业务下IP
    :param request:
    :return:
    """
    response = {
        'result': True,
        'message': 'success',
        'code': 0,
        'data': {}
    }
    biz_id = biz_id.split(',')[0]
    biz_id = int(biz_id)

    try:
        result = ESB.ESBApi(request).search_host(biz_id=biz_id)
        list = []
        if result['code'] == 0:
            if result['data']['count'] > 0:
                for biz_info in result['data']['info']:
                    listDic = {}
                    listDic['hostname'] = biz_info['host']['bk_host_name']
                    listDic['ip'] = biz_info['host']['bk_host_innerip']
                    listDic['os_type'] = biz_info['host']['bk_os_type']
                    listDic['os_name'] = biz_info['host']['bk_os_name']
                    bk_cloud = biz_info['host']['bk_cloud_id']
                    listDic['area'] = bk_cloud[0]['bk_inst_name']
                    listDic['area_id'] = bk_cloud[0]['bk_inst_id']
                    list.append(listDic)

                response['data']['list'] = list
                response['data']['count'] = len(list)
            else:
                response = {
                    'result': True,
                    'message': u'该业务下无IP',
                    'code': 0,
                    'data': {}
                }
        else:
            response = result

    except Exception, e:
        response = {
            'result': False,
            'message': '%s' % e,
            'code': 1,
            'data': {}
        }

    return render_json(response)


def run_inspect(request):
    '''
    执行脚本接口
    :param request:
    :return:
    '''
    response = {
        'result': True,
        'code': 0,
        'message': '',
        'data': {}
    }

    # 创建一条记录
    try:
        # 前端获取参数

        ips = request.GET.getlist('jiaoben_role')
        print ips
        select_script = request.GET.get('select_script')
        select_business = request.GET.get('select_business')
        select_data = select_business.split(',')
        select_business = select_data[0]
        biz_name = select_data[1]
        ip_list_all = ','.join(ips)
        script_contents = models.T_C_SCRIPT.objects.get(id=select_script)
        script_data = base64.b64encode(script_contents.script_content.encode('utf-8'))
        contents_name = script_contents.name
        ip_list = ip_list_all
        module_name = script_contents.name
        script_type = 3
        handle_user = request.user.username
        # t_script_data = models.T_SCRIPT_DATA.objects.create(
        #     ip_list_all=ip_list,
        #     contents_name=contents_name,
        #     select_business=select_business,
        #     script_type=script_type,
        #     module_name=module_name,
        #     script_data=script_data
        # )
        # async_run_script(handle_user, t_script_data, contents_name, select_business, ip_list, script_type=script_type, module_name=module_name, script_content=script_data)

    except Exception, e:
        response = {
            'result': False,
            'code': 1,
            'message': u'执行脚本失败：%s' % e,
            'data': {},
        }
    return redirect(reverse(home))


# 管理脚本


# 查看所有执行的脚本主机
def all_work(request):
    all_work_data = models.T_RECORDS_TASK.objects.filter(is_delete=0)
    content_data = {}
    for work in all_work_data:
        work_id = work.id
        content_data[work_id] = work.script_name + work.ips
    return render_mako_context(request, '/home_application/script_work_log.html', {'all_work': content_data})


# 查看日志
def search_pc_log(request, log_pc):
    log_pc = int(log_pc)
    t_task = models.T_RECORDS_TASK.objects.get(id=log_pc)
    cursor = connection.cursor()
    cursor.execute("SELECT execution_ip,execution_content FROM t_pc_log a WHERE execution_instance_id = %s AND 10>=(SELECT COUNT(*) FROM t_pc_log b WHERE a.execution_ip=b.execution_ip AND a.execution_content<=b.execution_content) ORDER BY a.execution_ip,a.execution_content" % t_task.id)
    pc_data = cursor.fetchall()
    all_data = {'time_list': []}
    for t_log in pc_data:
        all_data[t_log[0]] = {'cpu': [], 'memory': [], 'disk': []}
    for name_log in all_data:
        a = 1
        for content_logs in pc_data:
            if name_log == content_logs[0]:
                if len(content_logs[1].split('|')) > 1:
                    all_data[name_log]['cpu'].append(float(content_logs[1].split('|')[1][:-1]))
                    all_data[name_log]['memory'].append(float(content_logs[1].split('|')[2][:-1]))
                    all_data[name_log]['disk'].append(float(content_logs[1].split('|')[3][:-2]))
                    if a == 1:
                        all_data['time_list'].append(content_logs[1].split('|')[0][11:-3])
                else:
                    all_data[name_log]['cpu'].append(0)
                    all_data[name_log]['memory'].append(0)
                    all_data[name_log]['disk'].append(0)
        a += 1
    return render_json(all_data)


# 删除执行的脚本
def del_script_job(request):
    job_id = request.GET.get('select_business')
    job_data = models.T_RECORDS_TASK.objects.get(id=job_id)
    job_data.is_delete = 1
    job_data.save()
    return redirect(reverse(all_work))


# 脚本列表
def show_all_script(request):
    all_script_data = models.T_C_SCRIPT.objects.all()
    return render_mako_context(request, '/home_application/script_supervise.html', {'all_script_data': all_script_data})


# 新增脚本
def add_script(request):
    script_name = request.GET.get('script_name')
    script_content = request.GET.get('script_content')
    models.T_C_SCRIPT.objects.create(
        name=script_name,
        script_content=script_content
    )
    return redirect(reverse(show_all_script))


# 删除脚本
def del_script(request, s_id):
    script_data = models.T_C_SCRIPT.objects.get(id=s_id)
    script_data.delete()
    return redirect(reverse(show_all_script))


# 开启脚本周期任务
def open_job(request, o_id):
    job_data = models.T_RECORDS_TASK.objects.get(id=o_id)
    job_data.status = 0
    job_data.save()
    return redirect(reverse(home))


# 关闭周期任务
def close_job(request, o_id):
    job_data = models.T_RECORDS_TASK.objects.get(id=o_id)
    job_data.status = 1
    job_data.save()
    return redirect(reverse(home))


@login_exempt
def test(request):

    return render_json({
        "result":True,
        "message":'hello',
        "data":'world'
    })


def search_all_job(request):
    biz_id = request.GET.get('biz_id', '')
    user_name = request.GET.get('user_name', '')
    q = Q(is_delete__contains=0)
    if user_name:
        q.add(Q(handle_user=user_name), q.AND)
    if biz_id:
        q.add(Q(biz_name=biz_id), q.AND)
    # if biz_id and user_name is not None:
    #     search_data = models.T_RECORDS_TASK.objects.filter(script_name=biz_id,handle_user=user_name)
    # elif biz_id is None:
    #     search_data = models.T_RECORDS_TASK.objects.filter(handle_user=user_name)
    # elif user_name is None:
    #     search_data = models.T_RECORDS_TASK.objects.filter(script_name=biz_id)
    # else:
    #     search_data = ''
    search_data = models.T_RECORDS_TASK.objects.filter(q)
    list = []
    for one_data in search_data:
        listDic = {}
        listDic['id'] = one_data.id
        listDic['ips'] = one_data.ips
        listDic['script_name'] = one_data.script_name
        listDic['biz_id'] = one_data.biz_name
        if one_data.status == 1:
            listDic['status1'] = u'关闭'
            listDic['status2'] = u'开启'
            listDic['open_url'] = '/open_job/' + str(one_data.id)
        else:
            listDic['status1'] = u'开启'
            listDic['status2'] = u'关闭'
            listDic['url'] = '/close_job/' + str(one_data.id)
        listDic['url_name'] = '/show_job_log/' + str(one_data.id)
        list.append(listDic)
    data = {
        'massage': True,
        'data': list
    }
    print data
    return render_json(data)


