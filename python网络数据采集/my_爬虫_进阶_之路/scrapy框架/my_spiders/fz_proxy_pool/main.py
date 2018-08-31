# coding:utf-8

'''
@author = super_fazai
@File    : main.py
@connect : superonesfazai@gmail.com
'''

from proxy_tasks import (
    _get_kuaidaili_proxy,
    _write_into_redis,
    check_proxy_status,)
from time import sleep
from pprint import pprint
from logging import (
    INFO,
    ERROR,)
from pickle import dumps

from settings import (
    MAX_PROXY_NUM,
    SPIDER_LOG_PATH,
    WAIT_TIME,)

from fzutils.log_utils import set_logger
from fzutils.time_utils import get_shanghai_time
from fzutils.data.pickle_utils import deserializate_pickle_object
from fzutils.safe_utils import get_uuid3
from fzutils.sql_utils import BaseRedisCli

lg = set_logger(
    log_file_name=SPIDER_LOG_PATH + str(get_shanghai_time())[0:10]+'.log',
    console_log_level=INFO,
    file_log_level=ERROR)
redis_cli = BaseRedisCli()
proxy_list = []     # 存储采集的proxy结果
_key = get_uuid3('proxy_tasks')  # 存储proxy_list的key

def get_kuaidaili_proxy_process_data():
    '''
    抓取代理并更新redis中的值
    :return:
    '''
    global proxy_list
    res = _get_kuaidaili_proxy.apply_async(expires=5*60, retry=False)      # 过期时间
    res_content = res.get(timeout=2)
    sleep(2)
    if res_content != []:
        _write_into_redis.apply_async(args=(res_content,),)
    try:
        proxy_list += res    # 修改记录
    except:
        pass

    return res

def read_celery_tasks_result_info(celery_id_list:list) -> list:
    '''
    读取celery tasks的结果
    :param celery_id_list:
    :return:
    '''
    res = []
    for item in celery_id_list:
        # 读取
        _k = 'celery-task-meta-' + str(item.id)
        result = deserializate_pickle_object(redis_cli.get(_k))
        if result.get('status', '') == 'SUCCESS':
            res.append(result.get('result', []))
        else:
            lg.info('获取key值为{}失败!'.format(_k))

    return res

def check_all_proxy(origin_proxy_data):
    '''
    检查所有已抓取代理状态
    :param origin_proxy_data:
    :return:
    '''
    lg.info('开始检测所有proxy状态...')
    for index, proxy_info in enumerate(origin_proxy_data):
        last_check_time = proxy_info['last_check_time']
        ip = proxy_info['ip']
        port = proxy_info['port']
        score = proxy_info['score']

        try:
            res = check_proxy_status.delay(ip+str(port),).get(timeout=5)
        except Exception:
            lg.error('遇到错误:', exc_info=True)
            res = False

        if score <= 88:         # 删除
            origin_proxy_data.pop(index)
            continue

        if not res:
            proxy_info.update({
                'score': score - 2,
            })
            lg.info('[-] {}:{}'.format(ip, port))
        else:
            lg.info('[+] {}:{}'.format(ip, port))
            pass

        # 更新监控时间
        now_time = str(get_shanghai_time())
        proxy_info.update({
            'last_check_time': now_time,
        })

    redis_cli.set(name=_key, value=dumps(origin_proxy_data))
    lg.info('检查完毕!')

    return True

def main():
    celery_id_list = []
    while True:
        origin_proxy_data = deserializate_pickle_object(redis_cli.get(_key) or dumps([]))
        while len(origin_proxy_data) < MAX_PROXY_NUM:
            lg.info('Pools已存在proxy_num: {}'.format(len(origin_proxy_data)))
            one_page_res = get_kuaidaili_proxy_process_data()
            if one_page_res.status == 'SUCCESS':
                lg.info('[+] task的id: {}'.format(one_page_res.id))
            else:
                lg.info('[-] task的id: {}'.format(one_page_res.id))
            celery_id_list.append(str(one_page_res.id))
            # 重置
            origin_proxy_data = deserializate_pickle_object(redis_cli.get(_key) or dumps([]))
        else:
            lg.info('达标!休眠{}s...'.format(WAIT_TIME))
            sleep(WAIT_TIME)
            check_all_proxy(origin_proxy_data)

if __name__ == '__main__':
    main()