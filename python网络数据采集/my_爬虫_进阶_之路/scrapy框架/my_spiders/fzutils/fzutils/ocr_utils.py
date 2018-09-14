# coding:utf-8

'''
@author = super_fazai
@File    : ocr_utils.py
@connect : superonesfazai@gmail.com
'''

"""
光学识别
"""

from aip import AipOcr
import requests

from .internet_utils import get_random_pc_ua
from .img_utils import read_img_use_base64
from .common_utils import json_2_dict

__all__ = [
    'baidu_ocr_captcha',            # 百度ocr识别captcha
    'baidu_orc_image_main_body',    # 百度orc图像主体位置识别

    # 轨迹生成
    'get_tracks_based_on_distance', # 根据给与的距离生成不规律的移动轨迹tracks
]

def baidu_ocr_captcha(app_id, api_key, secret_key, img_path, orc_type=3) -> dict:
    '''
    百度ocr识别captcha
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

def baidu_orc_image_main_body(img_url='', local_img_path=None) -> dict:
    '''
    百度orc图像主体位置识别
    hack 百度图像主体检测功能演示, 旨在: 常规使用不付费
    https://ai.baidu.com/tech/imagerecognition/general
    :param img_url: 跟下面参数, 二选一
    :param local_img_path: 如果没有url, 则可通过本地图片path
    :return:
        success eg:
            {
                'errno': 0,
                'msg': 'success',
                'data': {
                    'log_id': '2587356961021549289',
                    'result': {
                        'width': 103,   # 宽度103px
                        'top': 2,       # 距上2px
                        'left': 10,     # 距左10px
                        'height': 115,  # 高度115px
                    }
                }
            }
    '''
    # BAIDUID是cookies的唯一必要参数
    cookies = {
        'BAIDUID': 'D668B34BE04D9BF359FB05917F1E1340:FG=1',
    }

    headers = {
        'Origin': 'https://ai.baidu.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': get_random_pc_ua(),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        # 'Referer': 'https://ai.baidu.com/tech/imagerecognition/general',
        'Connection': 'keep-alive',
    }

    img_content = ''
    if local_img_path is not None:
        img_content = read_img_use_base64(file_path=local_img_path)
        img_url = ''
        # print(img_content)

    data = [
      ('image', img_content),
      ('image_url', img_url),
      ('type', 'object_detect'),
    ]

    response = requests.post('https://ai.baidu.com/aidemo', headers=headers, cookies=cookies, data=data)

    return json_2_dict(response.text)

def get_tracks_based_on_distance(distance: int) -> dict:
    '''
    根据给与的距离生成不规律的移动轨迹tracks
    :param distance:
    :return: {'forward_tracks': [...], 'back_tracks': [...]}
    '''
    print('移动距离为:{}'.format(distance))
    distance += 20
    v = 0
    t = 0.2
    forward_tracks = []
    current = 0
    mid = distance * 3 / 5
    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3
        s = v * t + 0.5 * a * (t ** 2)
        v = v + a * t
        current += s
        forward_tracks.append(round(s))

    back_tracks = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1]

    return {
        'forward_tracks': forward_tracks,
        'back_tracks': back_tracks,
    }