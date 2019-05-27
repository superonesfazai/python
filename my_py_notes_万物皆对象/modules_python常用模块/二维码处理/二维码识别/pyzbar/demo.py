# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

"""
二维码识别(pip3 install pyzbar)

问题:
1. ImportError: Unable to find zbar shared library
    ubuntu: sudo apt-get install libzbar-dev
    mac: brew install zbar
"""

from requests import get
from PIL import Image
from io import BytesIO
from pyzbar.pyzbar import decode

def decode_qrcode(img_url=None, img_path=None, headers=None):
    '''
    二维码解码
    :param img_url: 二维码地址
    :param img_path:
    :return:
    '''
    assert img_url is not None or img_path is not None, 'img_url or img_path都为None, 赋值异常!'
    # decode_result的格式是[Decoded(data='****',……)]，列表里包含一个name tuple
    if img_url is not None:
        decode_result = decode(Image.open(BytesIO(get(url=img_url, headers=headers).content)))
    elif img_path is not None:
        decode_result = decode(Image.open(img_path))
    else:
        raise AssertionError
    # print(decode_result)

    return str(decode_result[0].data, encoding='utf-8')

# img_path = './images/tmp.jpg'
# print(decode_qrcode(img_path=img_path))
# img_url = 'https://i.loli.net/2018/11/15/5bed1adce184e.jpg'
# 新版二维码, 类似微信小程序的二维码(qrcode无法处理, android可复制)
# img_url = 'https://i.loli.net/2019/05/27/5cebac51260d124609.jpg'
# print(decode_qrcode(img_url=img_url))