# coding:utf-8

'''
@author = super_fazai
@File    : 测试跨域下载img.py
@connect : superonesfazai@gmail.com
'''

import requests
from fzutils.internet_utils import get_random_pc_ua

def request_download(image_url: str):
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': get_random_pc_ua(),
        # 必须
        'referer': image_url,
    }
    response = requests.get(
        url=image_url,
        headers=headers,)
    with open('./img2.png', 'wb') as f:
        f.write(response.content)

# image_url = 'https://pic.7y7.com/Uploads/Picture/2019-07-05/5d1eba0f819f1_450_0.jpg'
# wx(无效)
# image_url = 'https://mmbiz.qpic.cn/mmbiz_png/xwUfWjagCo99OzsMicyTaWiblEKeZTfzR01JcPJicPibaga2D9f8QibDKmUKMlabYpJDnvzB6cjGELkmbGVS3ZebD6Q/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1'
# image_url = 'https://mmbiz.qpic.cn/mmbiz_gif/I3humE75E1Ochl6EPcYmmgTohcycM3ZD5Y2WozPVeoyzrRpySvk8VjDtHxVkpR4eZuCyTAtEp8JppZ7UzUf2FA/640?wx_fmt=gif'
# 百度m站
# image_url = 'https://f10.baidu.com/it/u=1334121822,1648644466&fm=173&app=49&f=JPEG?w=640&h=691&s=1C22D5175F9377FDDC34C5DB030080B1&access=215967316'
# 搜狗
image_url = 'http://img04.sogoucdn.com/app/a/200883/71e0655d9a96ce58ceb21dbb5120e4fe'
request_download(image_url=image_url)