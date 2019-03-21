# coding:utf-8

'''
@author = super_fazai
@File    : 异步地向服务器取数据.py
@connect : superonesfazai@gmail.com
'''

import gevent.monkey
from gevent import (
    spawn,)
from gevent import joinall as gevent_joinall
gevent.monkey.patch_socket()

import simplejson as json
from fzutils.spider.fz_requests import Requests

def fetch(pid):
    url = 'http://json-time.appspot.com/time.json'
    body = Requests.get_url_body(
        url=url,
        use_proxy=False)
    # print(body)
    json_result = json.loads(body)
    datetime = json_result['datetime']

    print('Process %s: %s' % (pid, datetime))

    return json_result['datetime']

def synchronous():
    for i in range(1,10):
        fetch(i)

def asynchronous():
    tasks = []
    for i in range(1,10):
        tasks.append(spawn(fetch, i))

    gevent_joinall(tasks)

print('Synchronous:')
synchronous()

print('Asynchronous:')
asynchronous()