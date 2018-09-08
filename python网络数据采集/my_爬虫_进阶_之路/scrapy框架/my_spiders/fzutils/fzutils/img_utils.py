# coding:utf-8

'''
@author = super_fazai
@File    : img_utils.py
@connect : superonesfazai@gmail.com
'''

"""
img utils
"""

from PIL import Image
import requests
from io import BytesIO
from base64 import b64encode

from .path_utils import from_file_path_get_file_extension_name

__all__ = [
    'save_img_through_url',             # 根据img_url保存图片
    'read_img_use_base64',              # 以base64格式读取img
]

def save_img_through_url(img_url, save_path) -> bool:
    '''
    根据img_url保存图片
    :param img_url:
    :param save_path:
    :return:
    '''
    res = False
    try:
        img = Image.open(BytesIO(requests.get(url=img_url).content))
        img.save(save_path)
        res = True
    except Exception as e:
        print(e)

    return res

def read_img_use_base64(file_path) -> bytes:
    '''
    以base64格式读取img
    :param file_path:
    :return:
    '''
    file_extension_name = from_file_path_get_file_extension_name(file_path=file_path)
    with open(file_path, 'rb') as f:
        img_content = bytes('data:image/{};base64,'.format(file_extension_name), encoding='utf-8') + b64encode(f.read())

        return img_content