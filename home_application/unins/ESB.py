# -*- coding: utf-8 -*-
# Author : heyang
# @Time  : 2018/11/20 10:49
# @File  : ESB.py
__pet__ = '''   
              ┏┓     ┏┓
            ┏━┛┻━━━━━┛┻━━┓
            ┃      ☃      ┃
            ┃  ┳━┛  ┗━┳  ┃
            ┃      ┻      ┃
             ┗━━┓      ┏━━┛
                ┃       ┗━━━━┓
                ┃  神兽保佑   ┣┓
                ┃　永无BUG！  ┏┛
                ┗━┓━┓┏━━┳┓┏━━┛
                  ┃┫┫   ┃┫┫
                  ┗┻┛   ┗┻┛
'''
from conf.default import APP_ID, APP_TOKEN
from blueking.component.shortcuts import get_client_by_request, get_client_by_user
from django.http.request import HttpRequest
from blueking.component.client import ComponentClient



class ESBApi(object):
    """
     需要传request参数
    """

    def __init__(self, param):
        if isinstance(param, HttpRequest):
            self.__client = get_client_by_request(param)  # 获取用户登陆态
            self.username = param.user.username
        else:
            self.__client = get_client_by_user(param)  # 获取到用户对象
            self.username = param
        self.__param = {
            "app_code": APP_ID,
            "app_secret": APP_TOKEN,
            'bk_username': self.username
        }

    def search_business(self, page=None):
        if page is None:
            page = {"start": 0, "limit": 200}
        param = self.__param
        fields = ["bk_biz_id", "bk_biz_name"]
        param['fields'] = fields
        param['page'] = page
        print param
        result = self.__client.cc.search_business(param)

    # def search_business(self, page=None):
    #     param = {}
    #     if page is None:
    #         page = {"start": 0, "limit": 200}
    #     fields = ["bk_biz_id", "bk_biz_name"]
    #     param['bk_app_code'] = APP_ID
    #     param['bk_app_secret'] = APP_TOKEN
    #     param['bk_username'] = self.username
    #     print param
    #     result = self.__client.cc.search_business(param)

        return result

    # def search_host(self, biz_id, os_type, page=None):
    #     """
    #     获取当前业务下的IP
    #     :param biz_id:
    #     :param page:
    #     :return:
    #     """
    #
    #     try:
    #         if page is None:
    #             page = {"start": 0, "limit": 200}
    #
    #         condition = [{"bk_obj_id": 'host', "condition": [{'field': 'bk_os_type', "operator": "$eq", 'value': os_type}]}]
    #         param = self.__param
    #         param['bk_biz_id'] = biz_id
    #         param['page'] = page
    #         param['condition'] = condition
    #         result = self.__client.cc.search_host(param)
    #     except Exception, e:
    #         result = {'message': e}
    #
    #     return result
    def search_host(self, biz_id, page=None):
        try:
            if page is None:
                page = {"start": 0, "limit": 20}
            param = self.__param
            param['bk_biz_id'] = biz_id
            param['page'] = page
            param['condition'] = []
            result = self.__client.cc.search_host(param)
        except Exception, e:
            result = {'message': e}

        return result

    def get_app_by_user(self):
        """
        获取当前用户下的业务列表
        :return:
        """
        try:
            param = self.__param
            self.__client.set_bk_api_ver('')
            result = self.__client.cc.get_app_by_user(param)
        except Exception, e:
            result = {'message': e}

        return result


class ESBComponentApi(object):
    '''
    不需要request参数的esb
    '''

    def __init__(self):
        self.__param = {
            "app_code": APP_ID,
            "app_secret": APP_TOKEN,
            'bk_username': "admin"
        }
        common_args = {'username': 'admin'}
        self.client = ComponentClient(
            # APP_ID 应用ID
            app_code=APP_ID,
            # APP_TOKEN 应用TOKEN
            app_secret=APP_TOKEN,
            common_args=common_args
        )

    def fast_execute_script(self, bk_biz_id=None, script_id=None, script_content=None, ip_list=None, script_param=None,
                            account=None,script_type=None):
        '''
        执行脚本
        :param bk_biz_id:
        :param script_id:
        :param script_content:
        :param ip_list:
        :param script_param:
        :param account:
        :return:
        '''
        param = self.__param
        if account is None:
            account = 'root'
        if not script_id:
            param['script_id'] = script_id

        param["bk_biz_id"] = bk_biz_id
        param["script_content"] = script_content
        param["account"] = account
        param["ip_list"] = ip_list
        param["script_type"] = script_type

        if script_param is not None:
            param['script_param'] = script_param
        result = self.client.job.fast_execute_script(param)
        # print result, '--------快速执行脚本结果'
        return result

    def get_job_instance_log(self, bk_biz_id=None, job_instance_id=None):
        param = {
            "bk_app_code": self.__param['app_code'],
            "bk_app_secret": self.__param['app_secret'],
            "bk_biz_id": bk_biz_id,
            "job_instance_id": job_instance_id
        }
        result = self.client.job.get_job_instance_log(param)
        return result