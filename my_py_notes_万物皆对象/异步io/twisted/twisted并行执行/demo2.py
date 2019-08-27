# coding:utf-8

'''
@author = super_fazai
@File    : demo2.py
@connect : superonesfazai@gmail.com
'''

from twisted.internet import defer as twisted_defer
from twisted.internet import reactor as twisted_reactor
from twisted.internet import threads as twisted_threads
from twisted.python import threadable as twisted_threadable
from twisted.internet.interfaces import IReactorTime
from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.async_always import *

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
    def get_twisted_deferred_list_res(*args) -> list:
        """
        获取延迟列表deferred_list执行结果
        :param args: tuple
        :return:
        """
        nonlocal deferred_list_res

        # pprint(args)
        deferred_list_res = list(args)

        return deferred_list_res

    # 假如你的url写在文件中 用第一个参数传进来
    tasks = []
    for index in range(1, 50):
        print('create task[where index: {}] ...'.format(index))
        func_args = [
            index,
        ]
        tasks.append(twisted_threads.deferToThread(
            get_url_body,
            *func_args,))

    # 延迟列表
    deferred_list = twisted_defer.DeferredList(
        deferredList=tasks,
        fireOnOneCallback=False,
        fireOnOneErrback=False,
        consumeErrors=False,)
    deferred_list_res = []
    # deferred_list.addTimeout(timeout=100)
    # 增加回调函数
    callback_func_args = []
    deferred_list\
        .addCallback(
            callback=get_twisted_deferred_list_res,
            *callback_func_args,)\
        .addCallback(
            callback=lambda x: twisted_reactor.stop())

    twisted_threadable.init(with_threads=1)
    twisted_reactor.run()
    one_res = handle_deferred_list_res(
        deferred_list_res=deferred_list_res)
    pprint(one_res)

if __name__ == '__main__':
    main()