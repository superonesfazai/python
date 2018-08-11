# coding:utf-8

'''
@author = super_fazai
@File    : auto_wechat_robot.py
@Time    : 2018/7/5 16:06
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

import itchat
from pprint import pprint
from queue import Queue
import re
from taobao_weitao_share_parse import TaoBaoWeiTaoShareParse
import asyncio
import gc
import uuid

from fzutils.linux_utils import restart_program

my_queue = Queue(100)
old_message_url_uuid_list = []

@itchat.msg_register(itchat.content.TEXT, isFriendChat=True)
def text_reply(msg):
    '''
    回复他人发送给自己的信息
    :param msg:
    :return:
    '''
    global my_queue

    from_user_name = msg.get('FromUserName')
    tmp_sender = itchat.search_friends(userName=from_user_name)['NickName']
    # pprint(tmp_sender)

    msg_content = str(msg.get('Text')) if msg.get('Text') is not None else ''
    print('收到来自 ' + tmp_sender + ' 的微信: ' + msg_content)
    url = get_weitao_short_url(msg_content)

    if url != '':
        old_append_url_uuid(url)

        # 回复发送诶自己的信息
        reply = '谢谢亲[嘴唇]\n我收到您的信息如下:\n' \
                + '-'*30 + '\n' \
                + ' ' + msg_content

        my_queue.put(url)   # 问题解决了……自己在手机里发的消息也会进入控制台
        weitao_spider()

    else:
        reply = ''

    return reply

def get_weitao_short_url(msg_content):
    '''
    获取short_url
    :param msg_content:
    :return:
    '''
    if re.compile(r'淘♂寳♀').findall(msg_content) != []:
        try:
            url = re.compile(r'http:.*? ').findall(msg_content)[0].replace(' ', '')
            print('收到微淘url:', url)
        except IndexError:
            print('IndexError异常!')
            return None
    else:
        url = ''

    return url

def old_append_url_uuid(url):
    global old_message_url_uuid_list

    if old_message_url_uuid_list == []:
        return None

    # 在itchat.msg_register中无法修改全局变量的值，于是单独放此处修改
    url_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, url))
    old_message_url_uuid_list.append(url_uuid)
    old_message_url_uuid_list = list(set(old_message_url_uuid_list))

    return None

def weitao_spider():
    global loop

    if not my_queue.empty():
        taobao_short_url = my_queue.get()
        taobao_short_url_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, taobao_short_url))
        print(taobao_short_url_uuid)
        print(old_message_url_uuid_list)
        if taobao_short_url_uuid in old_message_url_uuid_list:
            return False

        print('拿到待处理url:', taobao_short_url)

        weitao = TaoBaoWeiTaoShareParse()
        try:
            loop.run_until_complete(weitao._deal_with_api_info(taobao_short_url))
        except RuntimeError:
            pass

        try:
            del weitao
            # loop.close()  # 重用loop
        except:
            pass
        gc.collect()
        restart_program()  # 通过这个重启环境, 避免log重复打印

        return True
    else:
        print('空queue!')

        return False

itchat.auto_login(hotReload=True)
loop = asyncio.get_event_loop()

itchat.run()
itchat.logout()

