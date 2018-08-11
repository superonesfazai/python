# coding:utf-8

'''
@author = super_fazai
@File    : reuse.py
@Time    : 2017/8/11 11:24
@connect : superonesfazai@gmail.com
'''

# high reuse(高复用code)

def add_base_info_2_processed_data(**kwargs):
    '''
    给采集后的data增加基础信息
    :param kwargs:
    :return:
    '''
    data = kwargs.get('data')
    spider_url = kwargs.get('spider_url')
    username = kwargs.get('username')
    goods_id = str(kwargs.get('goods_id'))

    wait_to_save_data = data
    wait_to_save_data['spider_url'] = spider_url
    wait_to_save_data['username'] = username
    wait_to_save_data['goods_id'] = goods_id

    return wait_to_save_data

def is_login(**kwargs):
    '''
    判断是否合法登录
    :param kwargs:
    :return: bool
    '''
    request = kwargs.get('request')

    if request.cookies.get('username') is not None \
            and request.cookies.get('passwd') is not None:   # request.cookies -> return a dict
        return True
    else:
        return False
