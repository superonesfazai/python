# coding:utf-8

'''
@author = super_fazai
@File    : spider.py
@Time    : 2018/5/19 17:55
@connect : superonesfazai@gmail.com
'''

from celery_config import app
import re
from json import dumps
from celery import Task

@app.task
def get_page_url():
    # 获取页面URL
    url_list = []
    for i in range(1,140):
        url = "http://www.umei.cc/p/gaoqing/rihan/" + str(i) + ".htm"
        url_list.append(url)

    return url_list

@app.task
def get_url(html):
    # 获取图片集url
    url_list = set(re.compile(r'/p/gaoqing/rihan/2016.*?\.htm').findall(html))

    return url_list

@app.task
def get_img(html):
    # 从HTML匹配获取图片
    img_list = set(re.compile(r'http://i1.umei.cc.*?\.jpg').findall(html))

    return img_list

# 下面跟上部程序无关
class MyTask(Task):
    name = 'MyTask'

    def run(self):
        raise ValueError('go away')

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        info = {}
        if status == 'FAILURE':
            info['error'] = retval
        self.update_state(state=status, meta=info)

app.tasks.register(MyTask())    # 类的用法