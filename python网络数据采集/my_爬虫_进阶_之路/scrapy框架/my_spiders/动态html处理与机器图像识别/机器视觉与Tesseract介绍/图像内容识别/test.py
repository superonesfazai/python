# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@connect : superonesfazai@gmail.com
'''

from fzutils.ocr_utils import baidu_orc_image_main_body

img_url = 'https://ss1.baidu.com/6ONXsjip0QIZ8tyhnq/it/u=1490702443,555061554&fm=58'
res = baidu_orc_image_main_body(img_url)
# res = baidu_orc_image_main_body(local_img_path='./images/captcha.jpg')
print(res)
