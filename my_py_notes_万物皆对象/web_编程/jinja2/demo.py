# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@Time    : 2016/8/9 18:58
@connect : superonesfazai@gmail.com
'''

from jinja2 import Template

template = Template('Hello {{ name }}!')
template.render(name='super_fazai')