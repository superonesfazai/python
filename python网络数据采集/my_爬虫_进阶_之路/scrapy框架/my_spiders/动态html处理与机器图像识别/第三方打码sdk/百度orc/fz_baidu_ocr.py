# coding:utf-8

'''
@author = super_fazai
@File    : fz_baidu_ocr.py
@connect : superonesfazai@gmail.com
'''

from pprint import pprint
from fzutils.common_utils import json_2_dict
from fzutils.ocr_utils import baidu_ocr_captcha

baidu_orc_info_path = '/Users/afa/baidu_orc.json'

with open(baidu_orc_info_path, 'r') as f:
    baidu_orc_info = json_2_dict(f.read())

img_path = './images/captcha2.jpg'
# img_path = './images/pin.png'
# img_path = './images/ali_captcha.jpg'

app_id = str(baidu_orc_info['app_id'])
api_key = baidu_orc_info['api_key']
secret_key = baidu_orc_info['secret_key']

pprint(baidu_ocr_captcha(
    app_id=app_id,
    api_key=api_key,
    secret_key=secret_key,
    img_path=img_path,
    orc_type=1))

