# coding:utf-8

'''
@author = super_fazai
@File    : main.py
@connect : superonesfazai@gmail.com
'''

from proxy_tasks import (
    _get_proxy,
    check_proxy_status,)
from time import sleep
from pprint import pprint
from logging import (
    INFO,
    ERROR,)
import re
from pickle import dumps
from random import randint
from celery.exceptions import TimeoutError

from settings import (
    MAX_PROXY_NUM,
    SPIDER_LOG_PATH,
    WAIT_TIME,
    CHECK_PROXY_TIMEOUT,
    proxy_list_key_name,
    high_proxy_list_key_name,
    MIN_SCORE,)

from fzutils.log_utils import set_logger
from fzutils.time_utils import get_shanghai_time
from fzutils.data.pickle_utils import (
    deserializate_pickle_object,
    serialize_obj_item_2_dict,)
from fzutils.safe_utils import get_uuid3
from fzutils.sql_utils import BaseRedisCli
from fzutils.data.list_utils import list_remove_repeat_dict
from fzutils.common_utils import get_random_int_number

lg = set_logger(
    log_file_name=SPIDER_LOG_PATH + str(get_shanghai_time())[0:10]+'.log',
    console_log_level=INFO,
    file_log_level=ERROR)
redis_cli = BaseRedisCli()
_key = get_uuid3(proxy_list_key_name)  # 存储proxy_list的key
_h_key = get_uuid3(high_proxy_list_key_name)

def _get_simulate_log_info(retries=10) -> str:
    '''
    print仿生log.info
    :return:
    '''
    time_str = lambda x='': str(get_shanghai_time()) + ',' + str(get_random_int_number(100, 999)) + ' [INFO  ] ➞ '
    try:
        time_str = time_str()
    except ValueError:
        if retries > 0:
            return _get_simulate_log_info(retries-1)
        else:
            return ''

    return time_str

def get_proxy_process_data():
    '''
    抓取代理并更新redis中的值
    :return:
    '''
    def _create_tasks_list(**kwargs):
        urls = kwargs.get('urls')
        page_range = kwargs.get('page_range', {})
        page_min, page_max = page_range['min'], page_range['max']
        random_parser_list_item_index = kwargs.get('random_parser_list_item_index')

        results = []
        if isinstance(urls, str):
            tmp_page_num_list = list(set([randint(page_min, page_max) for i in range(1, 20)]))
            urls = [urls.format(page_num) for page_num in tmp_page_num_list]
        elif isinstance(urls, list):
            _urls = []
            for item in urls:
                if re.compile('{}').findall(item) != []:
                    tmp_page_num_list = list(set([randint(page_min, page_max) for i in range(1, 20)]))
                    _s = [item.format(page_num) for page_num in tmp_page_num_list]
                    _urls += _s
                else:
                    _urls.append(item)
            urls = list(set(_urls))
        else:
            raise TypeError('urls类型异常!')

        for proxy_url in urls:
            # 异步, 不要在外部调用task的函数中sleep阻塞进程, 可在task内休眠
            async_obj = _get_proxy.apply_async(
                args=[random_parser_list_item_index, proxy_url,],
                expires=5*60,
                retry=False)      # 过期时间
            results.append(async_obj)

        return results

    def _get_tasks_result_list(**kwargs):
        results = kwargs.get('results', [])

        all = []
        success_num = 1
        results_len = len(results)
        while len(results) > 0:
            for r_index, r in enumerate(results):
                if r.ready():
                    try:
                        all.append(r.get(timeout=2, propagate=False))
                    except TimeoutError:
                        pass
                    success_num += 1
                    try:
                        results.pop(r_index)
                    except: pass
                else:
                    pass
                print('\r' + _get_simulate_log_info() + 'proxy_tasks._get_proxy: success_num: {}, rest_num: {}'.format(success_num, results_len-success_num), end='', flush=True)
        else:
            pass
        print('\r', end='', flush=True)

        return all

    def _handle_tasks_result_list(**kwargs):
        all = kwargs.get('all', [])
        origin_data = redis_cli.get(_key) or dumps([])  # get为None, 则返回[]
        old = deserializate_pickle_object(origin_data)

        for res_content in all:
            if res_content != []:
                old += res_content

        old = list_remove_repeat_dict(target=old, repeat_key='ip')
        old = serialize_obj_item_2_dict(old)      # 转化为dict, 避免反序列化时无法识别ProxyItem
        redis_cli.set(name=_key, value=dumps(old))

        return True

    from settings import parser_list    # 动态导入

    sleep(.8)
    random_parser_list_item_index = randint(0, len(parser_list) - 1)
    results = _create_tasks_list(
        urls=parser_list[random_parser_list_item_index].get('urls', ''),
        page_range=parser_list[random_parser_list_item_index].get('page_range', {}),
        random_parser_list_item_index=random_parser_list_item_index)
    all = _get_tasks_result_list(results=results)
    res = _handle_tasks_result_list(all=all)

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

def check_all_proxy(origin_proxy_data, redis_key_name, delete_score):
    '''
    检查所有已抓取代理状态
    :param origin_proxy_data:
    :param redis_key_name: redis待处理的key
    :param delete_score: 最低删除分数
    :return:
    '''
    def _create_tasks_list(origin_proxy_data):
        '''建立任务集'''
        nonlocal delete_score
        resutls = []
        for proxy_info in origin_proxy_data:
            last_check_time = proxy_info['last_check_time']
            ip = proxy_info['ip']
            port = proxy_info['port']
            score = proxy_info['score']
            if score <= delete_score:  # 删除跳过
                continue

            proxy = ip + ':' + str(port)
            # lg.info('testing {}...'.format(proxy))
            async_obj = check_proxy_status.apply_async(args=[proxy,],)
            resutls.append({
                'proxy_info': proxy_info,
                'async_obj': async_obj,
            })

        return resutls

    def _get_tasks_result_list(resutls):
        '''得到结果集'''
        def write_hign_proxy_info_2_redis(one_proxy_info):
            '''redis新写入高匿名ip'''
            old_h_proxy_list = deserializate_pickle_object(redis_cli.get(name=_h_key) or dumps([]))
            old_ip_list = [i.get('ip') for i in old_h_proxy_list]
            if one_proxy_info.get('ip') not in old_ip_list:
                old_score = one_proxy_info.get('score')
                one_proxy_info.update({     # 加分
                    'score': old_score + 5,
                })
                old_h_proxy_list.append(one_proxy_info)
                old_h_proxy_list = serialize_obj_item_2_dict(old_h_proxy_list)    # 防止反序列化时, 提示无法识别ProxyItem
                redis_cli.set(name=_h_key, value=dumps(old_h_proxy_list))
            else:
                pass
            return None

        all = []
        success_num = 1
        available_num = 0
        results_len = len(resutls)
        while len(resutls) > 0:
            for r_index, r in enumerate(resutls):
                proxy = r.get('proxy_info', {}).get('ip') + ':' + str(r.get('proxy_info', {}).get('port'))
                task_id = r.get('async_obj').id
                status = r.get('async_obj').status
                one_proxy_info = r.get('proxy_info', {})
                # lg.info('task_id: {}, status: {}'.format(task_id, status))
                if r.get('async_obj').ready():
                    async_res = False
                    try:
                        async_res = r.get('async_obj').get(timeout=2, propagate=False)  # 抛出异常，但程序不会停止, r.get('async_obj').traceback 追踪完整异常
                    except TimeoutError:
                        pass
                    if async_res:
                        available_num += 1
                        # 高匿ip写入redis
                        write_hign_proxy_info_2_redis(one_proxy_info)

                    all.append({
                        'async_res': async_res,
                        'proxy_info': one_proxy_info,
                    })
                    # 动态输出, '\r'回到当前开头
                    print('\r' + _get_simulate_log_info() + '已检测ip: {}, 剩余: {}, 实际可用高匿个数: {}'.format(success_num, results_len-success_num, available_num), end='', flush=True)
                    success_num += 1
                    try:
                        resutls.pop(r_index)
                    except: pass
                else:
                    # lg.info('{} 未完成!'.format(proxy))
                    pass
        else:
            print()
            # lg.info('所有异步结果完成!!')

        print('\r', end='', flush=True)

        return all

    def _handle_tasks_result_list(all):
        '''处理结果集'''
        def on_success(res, proxy_info):
            '''回调函数'''
            score = proxy_info.get('score')
            ip = proxy_info.get('ip')
            port = proxy_info.get('port')
            if not res:
                proxy_info.update({
                    'score': score - 2,
                })
                # lg.info('[-] {}:{}'.format(ip, port))
            else:
                # lg.info('[+] {}:{}'.format(ip, port))
                pass

            # 更新监控时间
            proxy_info.update({
                'last_check_time': str(get_shanghai_time()),
            })
            return proxy_info

        new_proxy_data = []
        for index, item in enumerate(all):
            new_proxy_info = on_success(
                res=item.get('async_res'),
                proxy_info=item.get('proxy_info'))
            new_proxy_data.append(new_proxy_info)

        return new_proxy_data

    global time_str

    resutls = _create_tasks_list(origin_proxy_data)
    sleep(.8)
    all = _get_tasks_result_list(resutls)

    # 处理储存最新数据
    new_proxy_data = list_remove_repeat_dict(
        target=_handle_tasks_result_list(all),
        repeat_key='ip',)
    new_proxy_data = serialize_obj_item_2_dict(new_proxy_data)
    redis_cli.set(name=redis_key_name, value=dumps(new_proxy_data))
    # lg.info('一次检查完毕!')

    return True

def main():
    global time_str

    while True:
        origin_proxy_data = list_remove_repeat_dict(
            target=deserializate_pickle_object(redis_cli.get(_key) or dumps([])),
            repeat_key='ip')
        # print()
        while len(origin_proxy_data) < MAX_PROXY_NUM:
            print('\r' + _get_simulate_log_info() + 'Ip Pools --->>> 已存在proxy_num(匿名度未知): {}'.format(len(origin_proxy_data)), end='', flush=True)
            get_proxy_process_data()
            # 重置
            origin_proxy_data = list_remove_repeat_dict(
                target=deserializate_pickle_object(redis_cli.get(_key) or dumps([])),
                repeat_key='ip')
        else:
            print()
            lg.info('达标!休眠{}s...'.format(WAIT_TIME))
            sleep(WAIT_TIME)
            lg.info('Async Checking all_proxy(匿名度未知)...')
            origin_proxy_data = list_remove_repeat_dict(target=origin_proxy_data, repeat_key='ip')
            check_all_proxy(origin_proxy_data, redis_key_name=_key, delete_score=90)

            '''删除失效的, 时刻保持最新高匿可用proxy'''
            high_origin_proxy_list = list_remove_repeat_dict(
                target=deserializate_pickle_object(redis_cli.get(_h_key) or dumps([])),
                repeat_key='ip')
            lg.info('Async Checking hign_proxy(高匿名)状态...')
            check_all_proxy(high_origin_proxy_list, redis_key_name=_h_key, delete_score=MIN_SCORE)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        lg.info('KeyboardInterrupt 退出 !!!')