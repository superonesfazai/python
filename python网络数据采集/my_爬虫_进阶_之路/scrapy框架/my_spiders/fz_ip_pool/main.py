# coding:utf-8

'''
@author = super_fazai
@File    : main.py
@connect : superonesfazai@gmail.com
'''

from proxy_tasks import (
    _get_proxy,
    _write_into_redis,
    check_proxy_status,)
from time import sleep, time
from pprint import pprint
from logging import (
    INFO,
    ERROR,)
from pickle import dumps
from random import randint
from celery.exceptions import TimeoutError

from settings import (
    MAX_PROXY_NUM,
    SPIDER_LOG_PATH,
    WAIT_TIME,
    CHECK_PROXY_TIMEOUT,
    parser_list,
    proxy_list_key_name,
    high_proxy_list_key_name,)

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
_key = get_uuid3(proxy_list_key_name)  # 存储proxy_list的key
_h_key = get_uuid3(high_proxy_list_key_name)

def get_proxy_process_data():
    '''
    抓取代理并更新redis中的值
    :return:
    '''
    global proxy_list
    random_parser_list_item_index = randint(0, len(parser_list)-1)
    for proxy_url in parser_list[random_parser_list_item_index].get('urls', []):
        # 异步, 不要在外部调用task的函数中sleep阻塞进程, 可在task内休眠
        res = _get_proxy.apply_async(
            args=[random_parser_list_item_index, proxy_url,],
            expires=5*60,
            retry=False)      # 过期时间
        try:
            res_content = res.get(timeout=CHECK_PROXY_TIMEOUT)
        except TimeoutError:
            continue
        if res_content != []:
            _write_into_redis.apply_async(args=(res_content,),)
        try:
            proxy_list += res    # 修改记录
        except:
            pass
        if res.status == 'SUCCESS':
            lg.info('[+] task的id: {}'.format(res.id))
        else:
            lg.info('[-] task的id: {}'.format(res.id))

    return True

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
    def create_tasks_list(origin_proxy_data):
        '''建立任务集'''
        resutls = []
        for proxy_info in origin_proxy_data:
            last_check_time = proxy_info['last_check_time']
            ip = proxy_info['ip']
            port = proxy_info['port']
            score = proxy_info['score']
            if score <= 90:  # 删除跳过
                continue

            proxy = ip + ':' + str(port)
            # lg.info('testing {}...'.format(proxy))
            async_obj = check_proxy_status.apply_async(args=[proxy, ],)
            resutls.append({
                'proxy_info': proxy_info,
                'async_obj': async_obj,
            })

        return resutls

    def get_tasks_result_list(resutls):
        '''得到结果集'''
        def write_hign_proxy_info_2_redis(one_proxy_info):
            '''redis新写入高匿名ip'''
            old_h_proxy_list = deserializate_pickle_object(redis_cli.get(name=_h_key) or dumps([]))
            old_ip_list = [i.get('ip') for i in old_h_proxy_list]
            if one_proxy_info.get('ip') not in old_ip_list:
                old_h_proxy_list.append(one_proxy_info)
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
                one_proxy_info = r.get('proxy_info')
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
                    lg.info('已检测ip: {}, 剩余个数: {}, 实际可用个数: {}'.format(success_num, results_len-success_num, available_num))
                    success_num += 1
                    try:
                        resutls.pop(r_index)
                    except: pass
                else:
                    # lg.info('{} 未完成!'.format(proxy))
                    pass
        else:
            lg.info('所有异步结果完成!!')

        return all

    def handle_tasks_result_list(all):
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
                lg.info('[-] {}:{}'.format(ip, port))
            else:
                lg.info('[+] {}:{}'.format(ip, port))
                pass

            # 更新监控时间
            proxy_info.update({
                'last_check_time': str(get_shanghai_time()),
            })
            return proxy_info

        new_proxy_data = []
        for index, item in enumerate(all):
            check_res = item.get('async_res')
            proxy_info = item.get('proxy_info')

            new_proxy_info = on_success(check_res, proxy_info)
            new_proxy_data.append(new_proxy_info)

        return new_proxy_data

    lg.info('开始检测所有proxy状态...')
    start_time = time()
    resutls = create_tasks_list(origin_proxy_data)
    end_time = time()

    lg.info('@@@ 请耐心等待所有异步结果完成...')
    all = get_tasks_result_list(resutls)
    lg.info('总共耗时: {}秒!!'.format(end_time - start_time))

    new_proxy_data = handle_tasks_result_list(all)
    redis_cli.set(name=_key, value=dumps(new_proxy_data))
    lg.info('一次检查完毕!')

    return True

def main():
    while True:
        origin_proxy_data = deserializate_pickle_object(redis_cli.get(_key) or dumps([]))
        while len(origin_proxy_data) < MAX_PROXY_NUM:
            lg.info('Ip Pools已存在proxy_num: {}'.format(len(origin_proxy_data)))
            get_proxy_process_data()
            # 重置
            origin_proxy_data = deserializate_pickle_object(redis_cli.get(_key) or dumps([]))
        else:
            lg.info('达标!休眠{}s...'.format(WAIT_TIME))
            sleep(WAIT_TIME)
            check_all_proxy(origin_proxy_data)

if __name__ == '__main__':
    main()