# coding:utf-8

'''
@author = super_fazai
@File    : fz_baidu_orc.py
@connect : superonesfazai@gmail.com
'''

from fzutils.common_utils import json_2_dict
from aip import AipOcr

def baidu_orc_captcha(app_id, api_key, secret_key, img_path, orc_type=3):
    '''
    百度orc识别captcha
    :param app_id:
    :param api_key:
    :param secret_key:
    :param img_path:
    :param orc_type: 1: basic_general 2: general 3: web_image
    :return:
    '''
    def basic_general():
        '''通用文字识别接口'''
        res = api_orc.basicGeneral(image=get_img_content(img_path), options=basic_general_options)

        return res

    def general():
        '''通用文字识别(含位置信息版)'''
        # 可以接受任意图片，并识别出图片中的文字以及全部文字串，以及字符在图片中的位置信息。
        general_options = basic_general_options
        general_options.update({
            'vertexes_location': 'true',  # 是否返回结果中表示文字的位置
        })
        res = api_orc.general(image=get_img_content(img_path), options=general_options)

        return res

    def web_image():
        '''网络图片文字识别接口'''
        # 用于识别一些网络上背景复杂，特殊字体的文字。(经测试, 这种识别率较高)
        general_options = basic_general_options
        general_options.update({
            'vertexes_location': 'true',  # 是否返回结果中表示文字的位置
        })
        res = api_orc.webImage(image=get_img_content(img_path), options=general_options)

        return res

    def get_img_content(img_path):
        '''读取img内容'''
        with open(img_path, 'rb') as f:
            return f.read()

    api_orc = AipOcr(app_id, api_key, secret_key)

    # 定义参数变量
    basic_general_options = {
        'detect_direction': 'true',         # 是否检测图像朝向, 默认不检测'false'
        'detect_language': 'true',          # 是否检测语言, 默认不检测'false'
        'language_type': 'CHN_ENG',         # 识别语言类型， 默认为CHN_ENG。 选值包括：-CHN_ENG： 中英文混合；-ENG： 英文；-POR：葡萄牙语；-FRE：法语；-GER：德语；-ITA：意大利语；-SPA：西班牙语；-RUS：俄语；-JAP：日语
        'classify_dimension': 'lottery',    # 分类维度, 当前仅支持lottery， 设置detect_direction有助于提升精度
    }
    if orc_type == 1:
        return basic_general()
    elif orc_type == 2:
        return general()
    elif orc_type == 3:
        return web_image()
    else:
        raise ValueError('orc_type赋值异常!')

baidu_orc_info_path = '/Users/afa/baidu_orc.json'

with open(baidu_orc_info_path, 'r') as f:
    baidu_orc_info = json_2_dict(f.read())

img_path = './images/captcha2.jpg'
# img_path = './images/pin.png'

app_id = str(baidu_orc_info['app_id'])
api_key = baidu_orc_info['api_key']
secret_key = baidu_orc_info['secret_key']

print(baidu_orc_captcha(
    app_id=app_id,
    api_key=api_key,
    secret_key=secret_key,
    img_path=img_path,
    orc_type=1))

