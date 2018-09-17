# coding:utf-8

'''
@author = super_fazai
@File    : z8_text_captcha.py
@connect : superonesfazai@gmail.com
'''


import re
from os.path import exists
from os import mkdir
from PIL import Image
from pytesseract import image_to_string
from fzutils.internet_utils import get_random_pc_ua
from fzutils.common_utils import (
    json_2_dict,
    save_base64_img_2_local,)
from fzutils.spider.fz_requests import Requests

def get_one_captcha_from_z8() -> str:
    '''
    获取折800验证码
    :return:
    '''
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'diablo.alibaba.com',
        'Proxy-Connection': 'keep-alive',
        'User-Agent': get_random_pc_ua(),
    }

    query_string = {
        'sessionid': '01-m_ZiEy0_67YhTwhCfGlCh2gNq93HaGS_yk3hfYmY9iIVT6la1TM1rtkaLSZe5mwV2Wi9kDZBAK50WYxZOwAY5KYPpBGAyJKsEnvG1VEUXb5hpFCQEDaCU2YrqTfjlRPsin7-1iLEyzNzKzaPUVJKA',
        'identity': 'WKBT',
        'style': 'default_science',
        'callback': 'jsonp_08668900079497168',
    }
    url = 'http://diablo.alibaba.com/captcha/image/get.jsonp'
    body = Requests.get_url_body(url=url, use_proxy=False, headers=headers, params=query_string)
    base64_img_str = ''
    try:
        body = re.compile('jsonp_08668900079497168\((.*)\);').findall(body)[0]
        img_data = json_2_dict(body)
        base64_img_str = img_data.get('result', {}).get('data', [])[0]
    except Exception as e:
        print('遇到错误: ', e)

    return base64_img_str

def convert_Image(img, standard=127.5):
    '''
    【灰度转换】
    '''
    image = img.convert('L')

    # 【二值化】根据阈值 standard , 将所有像素都置为 0(黑色) 或 255(白色), 便于接下来的分割
    pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            if pixels[x, y] > standard:
                pixels[x, y] = 255
            else:
                pixels[x, y] = 0

    return image

save_path = '/Users/afa/Desktop/z8_images/'
if exists(save_path):
    pass
else:
    mkdir(save_path)

# 保存captcha
eng_tessdata_path = '/Users/afa/myFiles/tools/tessdata/eng.traineddata'
for index, i in enumerate(range(100)):
    base64_img_str = get_one_captcha_from_z8()
    if base64_img_str != '':
        img_file_name = '{}.jpg'.format(index)
        img_path = save_path + img_file_name
        res = save_base64_img_2_local(save_path=img_path, base64_img_str=base64_img_str)
        if res != '':
            print('[+] {} saved!'.format(img_file_name))

        img = Image.open(img_path)
        # img.show()
        convert_Image(img=img)
        # 先下载语言包, 再放到 /usr/local/Cellar/tesseract/3.05.01/share/tessdata
        # 可以通过tesseract --list-langs查看本地语言包
        print(image_to_string(img, lang='eng'))
