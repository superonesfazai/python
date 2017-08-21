# coding = utf-8

'''
@author = super_fazai
@File    : urls.py
@Time    : 2017/8/21 23:11
@connect : superonesfazai@gmail.com
'''
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^articles/([0-9]{4})/$', views.year_archive),
    url(r'^articles/([0-9]{4})/([0-9]{2})/$', views.month_archive),
    url(r'^articles/([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.article_detail),
]