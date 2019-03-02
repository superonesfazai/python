# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

import atx
import uiautomator2 as u2

# 如果多个手机连接电脑，则需要填入对应的设备号
# d = atx.connect()
# print(d)
# d.screenshot('screen.png')

# adb device 查看
d = u2.connect("816QECTK24ND8")
print(d.info)
d.set_fastinput_ime(True)
d.debug =True
s = d.session("com.meizu.flyme.calculator")