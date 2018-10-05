# coding:utf-8

"""
aio 异步utils
"""

from asyncio import get_event_loop, wait

from .spider.fz_aiohttp import AioHttp

__all__ = [
    'Asyncer',
    'get_async_execute_result',     # 获取异步执行结果
    'async_wait_tasks_finished',    # 异步等待目标tasks完成
]

class Asyncer(object):
    '''异步类'''
    async def get_async_requests_body(**kwargs):
        return await AioHttp.aio_get_url_body(**kwargs)

def get_async_execute_result(obj=Asyncer,
                             obj_method_name='get_async_requests_body',
                             **kwargs):
    '''
    获取异步执行结果
    :param obj: 对象的类
    :param obj_method_name: 对象的方法名
    :param kwargs: 该方法附带的参数
    :return:
    '''
    loop = get_event_loop()
    if hasattr(obj, obj_method_name):
        method_callback = getattr(obj, obj_method_name)
    else:
        raise AttributeError('{obj}类没有{obj_method_name}方法!'.format(obj=obj, obj_method_name=obj_method_name))

    result = loop.run_until_complete(
        future=method_callback(**kwargs))

    return result

async def async_wait_tasks_finished(tasks:list) -> list:
    '''
    异步等待目标tasks完成
    :param tasks: 任务集
    :return:
    '''
    try:
        success_jobs, fail_jobs = await wait(tasks)
        print('请耐心等待所有任务完成...')
        print('执行完毕! success_task_num: {}, fail_task_num: {}'.format(len(success_jobs), len(fail_jobs)))
        all_res = [r.result() for r in success_jobs]
    except Exception as e:
        print(e)
        return []

    return all_res