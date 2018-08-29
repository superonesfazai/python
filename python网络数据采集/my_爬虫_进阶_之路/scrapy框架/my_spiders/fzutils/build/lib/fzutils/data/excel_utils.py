# coding:utf-8

'''
@author = super_fazai
@File    : excel_utils.py
@Time    : 2016/7/24 11:28
@connect : superonesfazai@gmail.com
'''

from pprint import pprint
from pyexcel import iget_records
from os.path import exists

__all__ = [
    'read_info_from_excel_file',                                # 本地从excel中读取文件并以list格式返回
]

def read_info_from_excel_file(excel_file_path):
    '''
    本地从excel中读取文件并以list格式返回
    :param excel_file_path:
    :return: a list eg: [{'关键词': '连衣裙', '一级类目': '女装/女士精品', '二级类目': '连衣裙', '三级类目': ''}, ...]
    '''
    result = []
    if not exists(excel_file_path):
        raise FileExistsError('在该excel的路径未找到待处理文件, 请检查!')

    else:
        data = iget_records(file_name=excel_file_path)  # row a OrderedDict object
        for index, row in enumerate(data):
            row = dict(row)     # eg: {'关键词': '连衣裙', '一级类目': '女装/女士精品', '二级类目': '连衣裙', '三级类目': ''}
            # print(row)

            result.append(row)

    return result


