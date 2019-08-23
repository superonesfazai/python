# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

from threading import current_thread
from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.async_always import *

@catch_exceptions(default_res='')
def test(index: int):
    current_thread_obj = current_thread()
    print('index: {}, thread_name: {}'.format(index, current_thread_obj.name))
    # sleep(5.)
    sleep(get_random_int_number(1, 5))
    print('index: {}, thread_name: {} over!'.format(index, current_thread_obj.name))

    return '{}:{}'.format(index, current_thread_obj.name)

@catch_exceptions(default_res={})
def get_url_body(index):
    url = 'https://httpbin.org/get'
    body = Requests.get_url_body(
        url=url,
        ip_pool_type=tri_ip_pool,
        proxy_type=PROXY_TYPE_HTTPS,
        timeout=15,)
    data = json_2_dict(json_str=body)
    print('[{}] index: {}'.format(
        '+' if data != {} else '-',
        index,
    ))

    return data

@func_time
def main():
    print('main_thread_name: {}'.format(current_thread().name))
    tasks = []
    for index in range(1, 50):
        print('create task[where is index: {}] ...'.format(index))
        # task = ThreadTaskObj(
        #     func_name=test,
        #     args=[
        #         index,
        #     ],
        #     default_res=None,)
        task = ThreadTaskObj(
            func_name=get_url_body,
            args=[
                index,
            ],
            default_res={},
            func_timeout=None,)
        tasks.append(task)

    one_res = start_thread_tasks_and_get_thread_tasks_res(tasks=tasks)
    # pprint(one_res)

    try:
        del tasks
    except:
        pass

if __name__ == '__main__':
    main()

