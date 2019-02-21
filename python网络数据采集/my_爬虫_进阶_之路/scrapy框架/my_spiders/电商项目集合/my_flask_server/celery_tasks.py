# coding:utf-8

'''
@author = super_fazai
@File    : celery_tasks.py
@connect : superonesfazai@gmail.com
'''

from gc import collect
from celery.utils.log import get_task_logger
from asyncio import wait_for, Future
from functools import partial
from threading import (
    Thread,
    current_thread,)
from asyncio import (
    new_event_loop,
    get_event_loop,
    set_event_loop,)
from multiplex_code import (
    _get_al_one_type_company_id_list,
    _get_114_one_type_company_id_list,)
from company_spider import CompanySpider
from fzutils.internet_utils import get_random_pc_ua
from fzutils.celery_utils import *
from fzutils.spider.fz_requests import Requests

"""
redis:
# 指定被修改后的redis.conf来启动
$ redis-server /usr/local/etc/redis.conf

分布式任务启动: 
1. celery -A celery_tasks worker -l info -P eventlet -c 300
(多开效果更快)
2. celery multi start w0 w1 w2 w3 w4 w5 w6 w7 w8 w9 w10 w11 w12 w13 w14 w15 w16 w17 w18 w19 w20 -A celery_tasks -P eventlet -c 300 -f /Users/afa/myFiles/my_spider_logs/tmp/celery_tasks.log 

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
        timeout=timeout)
    collect()

    return res

@app.task(name=tasks_name + '._get_114_one_type_company_id_list_task', bind=True)
def _get_114_one_type_company_id_list_task(self, ip_pool_type, num_retries, parser_obj, cate_num, page_num):
    res = _get_114_one_type_company_id_list(
        ip_pool_type=ip_pool_type,
        num_retries=num_retries,
        cate_num=cate_num,
        page_num=page_num,
        parser_obj=parser_obj,
        logger=lg,)
    collect()

    return res

class TaskObj(Thread):
    '''
    重写爬虫线程
    '''
    def __init__(self, func, args=(), default_res=None):
        super(TaskObj, self).__init__()
        self.func = func
        self.args = args
        # Thread默认结果
        self.default_res = default_res
        self.res = default_res

    def run(self):
        self.res = self.func(*self.args)

    def _get_result(self):
        try:
            Thread.join(self)  # 等待线程执行完毕
            return self.res
        except Exception:
            lg.error('线程遇到错误:', exc_info=True)
            return self.default_res

@app.task(name=tasks_name + '._parse_one_company_info_task', bind=True)
def _parse_one_company_info_task(self, short_name, company_url='', province_name='', city_name='', company_id='', type_code=''):
    def oo():
        try:
            company_spider = CompanySpider()
            # 设置当前事件循环为新的事件循环, 避免报错
            set_event_loop(new_event_loop())
            loop = new_event_loop()
            res = loop.run_until_complete(company_spider._parse_one_company_info(
                short_name=short_name,
                company_url=company_url,
                province_name=province_name,
                city_name=city_name,
                company_id=company_id,
                type_code=type_code,))
        except Exception:
            lg.error('遇到错误:', exc_info=True)
            res = {}

        try:
            loop.close()
        except:
            pass
        try:
            del company_spider
        except:
            pass
        collect()

        return res

    # TODO celery与asyncio的结合使用将在celery5.0(官方未开发)以后实现, 现在celery4.2.1会出现异常!
    thread1 = TaskObj(oo, args=(), default_res={})
    thread1.start()
    lg.info('thread {} is running...'.format(current_thread().name))

    return thread1._get_result()

def _get_pc_headers() -> dict:
    return {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': get_random_pc_ua(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

@app.task(name=tasks_name + '._get_114_company_page_html_task', bind=True)
def _get_114_company_page_html_task(self, company_id, ip_pool_type, num_retries) -> tuple:
    '''
    获取114单个页面的page_html
    :param self:
    :param company_id:
    :return: (company_id, body)
    '''
    headers = _get_pc_headers()
    headers.update({
        'Proxy-Connection': 'keep-alive',
        # 'Referer': 'http://www.114pifa.com/c-3181.html',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    })
    url = 'http://www.114pifa.com/ca/{}'.format(company_id)
    body = Requests.get_url_body(
        url=url,
        headers=headers,
        ip_pool_type=ip_pool_type,
        encoding='gbk',
        num_retries=num_retries,)
    if body == '':
        lg.error('company body为空值! shop_url: {}'.format(url))

    lg.info('[{}] 114 company_id: {}'.format('+' if body != '' else '-', company_id))

    return company_id, body