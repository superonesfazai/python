# coding = utf-8

'''
@author = super_fazai
@File    : admin.py
@Time    : 2017/8/21 23:07
@connect : superonesfazai@gmail.com
'''

from django.contrib import admin

from . import models

admin.site.register(models.Article)

'''
这里的理念 is that your site is edited by a staff, or a client, 
or maybe just you – and you don’t want to have to deal with creating backend interfaces just to manage content.
'''