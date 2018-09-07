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

__all__ = [
    'save_img_through_url',             # 根据img_url保存图片
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