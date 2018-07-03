# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@Time    : 2018/7/3 17:36
@connect : superonesfazai@gmail.com
'''

"""
open-code: https://github.com/lincolnloop/python-qrcode
"""

# 常规用法
import qrcode

img = qrcode.make('https://www.baidu.com')
img.save('out.png')

# 高级用法
# import qrcode
#
# qr = qrcode.QRCode(
#     version=1,
#     error_correction=qrcode.constants.ERROR_CORRECT_L,
#     box_size=10,
#     border=4,
# )
# qr.add_data('https://www.baidu.com')
# qr.make(fit=True)
#
# img = qr.make_image(fill_color="black", back_color="white")
# img.save('out.png')