# coding:utf-8

'''
@author = super_fazai
@File    : urls.py
@Time    : 2017/10/6 10:50
@connect : superonesfazai@gmail.com
'''

from django.conf.urls import url
from . import views
urlpatterns = [
    # 配置首页
    url(r'^$', views.index),
    # 配置详细页url
    url(r'^(\d+)$', views.detail),
]