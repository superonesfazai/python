# coding:utf-8

'''
@author = super_fazai
@File    : js_utils.py
@connect : superonesfazai@gmail.com
'''

"""
js utils
"""

from execjs import compile

__all__ = [
    'get_js_parser_res',        # python调用js, 并返回结果
]

def get_js_parser_res(js_path, func_name, **args):
    '''
    python调用js, 并返回结果
    :param js_path: js文件路径
    :param func_name: 待调用的函数名
    :param args: 该函数待传递的参数
    :return: res
    '''
    with open(js_path, 'r') as f:
        js_code = f.read()

    js_parser = compile(js_code)
    res = js_parser.call(func_name, *args)

    return res