# coding:utf-8

'''
@author = super_fazai
@File    : jobs.py
@connect : superonesfazai@gmail.com
'''

from redis import Redis
from rq import Queue
from requests import get

def count_words(url):
    return len(get(url).text.split())

def get_q():
    redis_conn = Redis()
    return Queue(connection=redis_conn)