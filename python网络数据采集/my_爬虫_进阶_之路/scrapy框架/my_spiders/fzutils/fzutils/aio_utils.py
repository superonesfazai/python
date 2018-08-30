# coding:utf-8

"""
aio 异步utils
"""

from asyncio import get_event_loop

from .spider.fz_aiohttp import AioHttp

__all__ = [
    'Asyncer',
    'get_async_execute_result',     # 获取异步执行结果
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