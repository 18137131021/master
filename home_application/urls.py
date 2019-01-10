# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'home'),
    (r'^dev-guide/$', 'dev_guide'),
    (r'^contactus/$', 'contactus'),
    (r'^demo_one/$', 'demo_one'),
    (r'^run_inspect/$', 'run_inspect'),
    (r'^search_pc/(\d+)$', 'search_pc'),
    (r'^all_work/', 'all_work'),
    (r'^search_pc_log/(\d+)$', 'search_pc_log'),
    (r'^del_script_job/$', 'del_script_job'),
    (r'^all_script_data/$', 'show_all_script'),
    (r'^add_script/$', 'add_script'),
    (r'^del_script/(\d+)$', 'del_script'),
    (r'^open_job/(\d+)$', 'open_job'),
    (r'^close_job/(\d+)$', 'close_job'),
    (r'^search_all_job/$', 'search_all_job'),
    (r'^api/test/$', 'test'),
)
