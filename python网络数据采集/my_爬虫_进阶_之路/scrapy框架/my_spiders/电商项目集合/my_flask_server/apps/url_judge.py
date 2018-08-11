# coding:utf-8

'''
@author = super_fazai
@File    : url_judge.py
@Time    : 2017/8/11 11:30
@connect : superonesfazai@gmail.com
'''

import re

def _is_taobao_url_plus(goods_link):
    '''
    淘宝m站
    :param goods_link:
    :return:
    '''
    if re.compile(r'https://h5.m.taobao.com/awp/core/detail.htm.*?').findall(goods_link) != [] \
            or re.compile(r'https://item.taobao.com/item.htm.*?').findall(goods_link) != []:
        return True

    return False

def _is_tmall_url(wait_to_deal_with_url):
    '''
    判断是否为tmall的url
    :param wait_to_deal_with_url:
    :return: bool
    '''
    _ = False
    if re.compile(r'https://detail.tmall.com/item.htm.*?').findall(wait_to_deal_with_url) != [] \
         or re.compile(r'https://chaoshi.detail.tmall.com/item.htm.*?').findall(wait_to_deal_with_url) != [] \
         or re.compile(r'https://detail.tmall.hk/.*?item.htm.*?').findall(wait_to_deal_with_url) != []:
        _ = True

    return _

def _is_tmall_url_plus(goods_link):
    '''
    天猫m站/pc站地址
    :param goods_link:
    :return:
    '''
    if re.compile(r'detail.tmall.').findall(goods_link) != [] \
        or re.compile(r'detail.m.tmall.com').findall(goods_link) != []:
        return True

    return False

def _is_jd_url(wait_to_deal_with_url):
    '''
    判断是否为jd的url
    :param wait_to_deal_with_url:
    :return: bool
    '''
    _ = False
    if re.compile(r'https://item.jd.com/.*?').findall(wait_to_deal_with_url) != [] \
         or re.compile(r'https://item.jd.hk/.*?').findall(wait_to_deal_with_url) != [] \
         or re.compile(r'https://item.yiyaojd.com/.*?').findall(wait_to_deal_with_url) != []:
        _ = True

    return _

def _is_jd_url_plus(goods_link):
    '''
    京东m站/pc站
    :param goods_link:
    :return:
    '''
    if re.compile('item.jd|item.yiyaojd|item.m.jd.com|mitem.jd.hk|m.yiyaojd.com').findall(goods_link) != []:
        return True

    return False
