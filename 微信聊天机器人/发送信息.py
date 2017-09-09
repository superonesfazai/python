# coding = utf-8

'''
@author = super_fazai
@File    : 发送信息.py
@Time    : 2017/9/9 12:39
@connect : superonesfazai@gmail.com
'''

"""
发送信息(文字, 图片, 文件, 音频, 视频等)
"""

import itchat
import datetime

itchat.auto_login(hotReload=True)

tmp_user_name = itchat.search_friends()['UserName']
# 文字
msg = '别来无恙啊!\n发送时间:\n{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
reply = itchat.send(msg, toUserName=tmp_user_name)
print(reply['BaseResponse']['ErrMsg'])      # 打印请求结果, 如果成功, 打印请求成功

# 图片
img_path = './QR.jpg'
reply = itchat.send_image(img_path, tmp_user_name)
print(reply['BaseResponse']['ErrMsg'])

# 文件
file_path = './你好/tmp.py'
reply = itchat.send_file(file_path, tmp_user_name)
print(reply['BaseResponse']['ErrMsg'])

# 音频(语音可以先转换成mp3)
# reply = itchat.send_file(xx, tmp_user_name)   # 等同于发送文件

# 视频    也等同于发送文件

# 发送信息去群组: group[0]['UserName']
tmp_group_user_name = itchat.search_chatrooms(name='阿发自嗨群')[0]['UserName']
msg = '别来无恙啊!\n发送时间:\n{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
reply = itchat.send(msg, tmp_group_user_name)
print(reply['BaseResponse']['ErrMsg'])

itchat.run()