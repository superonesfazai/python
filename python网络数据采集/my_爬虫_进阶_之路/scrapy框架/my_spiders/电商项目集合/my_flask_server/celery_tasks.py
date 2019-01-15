# coding:utf-8

'''
@author = super_fazai
@File    : celery_tasks.py
@connect : superonesfazai@gmail.com
'''

from gc import collect
from celery.utils.log import get_task_logger
from asyncio import (
    new_event_loop,
    get_event_loop,)
from multiplex_code import _get_al_one_type_company_id_list
from fzutils.celery_utils import *

"""
redis:
# 指定被修改后的redis.conf来启动
$ redis-server /usr/local/etc/redis.conf

分布式任务启动: 
1. celery -A celery_tasks worker -l info -P eventlet -c 300
2. celery multi start w0 w1 w2 w3 w4 w5 w6 w7 w8 -A celery_tasks -P eventlet -c 300 -f /Users/afa/myFiles/my_spider_logs/tmp/celery_tasks.log (多开效果更快)

监控:
$ celery -A celery_tasks flower --address=127.0.0.1 --port=5555
$ open http://localhost:5555
"""

tasks_name = 'celery_tasks'
app = init_celery_app(
    name=tasks_name,
)
lg = get_task_logger(tasks_name)

@app.task(name=tasks_name + '._get_al_one_type_company_id_list_task', bind=True)
def _get_al_one_type_company_id_list_task(self, ip_pool_type, keyword, page_num, timeout=15):
    # def _get_args():
    #     return [
    #         db_al_unique_id_list,
    #         ip_pool_type,
    #         lg,
    #         keyword,
    #         page_num,
    #         timeout,
    #     ]

    # loop = get_event_loop()
    # loop = new_event_loop()
    # args = _get_args()
    # try:
    #     # res = loop.run_in_executor(None, _get_al_one_type_company_id_list(
    #     #     db_al_unique_id_list=db_al_unique_id_list,
    #     #     ip_pool_type=ip_pool_type,
    #     #     logger=lg,
    #     #     keyword=keyword,
    #     #     page_num=page_num,
    #     #     timeout=timeout,
    #     # ))
    #     res = loop.run_in_executor(None, _get_al_one_type_company_id_list, *args)
    # except Exception as e:
    #     lg.error('遇到错误:', exc_info=True)
    # finally:
    #     try:
    #         del loop
    #     except:
    #         pass
    #     collect()
    #
    #     return res

    # celery不能序列化协程对象, 故无法写成协程形式, 使用常规函数式
    res = _get_al_one_type_company_id_list(
        ip_pool_type=ip_pool_type,
        logger=lg,
        keyword=keyword,
        page_num=page_num,
        timeout=timeout
    )
    collect()

    return res