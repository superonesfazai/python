# coding:utf-8

'''
@author = super_fazai
@File    : list_utils.py
@Time    : 2018/8/4 11:46
@connect : superonesfazai@gmail.com
'''

__all__ = [
    'unique_list_and_keep_original_order',              # 从列表中删除重复的元素, 同时保留其原始顺序
]

def unique_list_and_keep_original_order(target_list, key=None):
    '''
    从列表中删除重复的元素, 同时保留其原始顺序
    :param target_list: 待处理的list
    :param key: 是一个函数，它接受一个参数并返回一个 key 来测试唯一性
    :return:
    '''
    key = key or (lambda x: x)
    seen = set()
    unique_list = []
    for value in target_list:
        unique_value = key(value)
        if unique_value in seen:
            continue

        seen.add(unique_value)
        unique_list.append(value)

    return unique_list
