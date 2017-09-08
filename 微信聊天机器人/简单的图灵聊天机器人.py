# coding = utf-8

'''
@author = super_fazai
@File    : 简单的图灵聊天机器人.py
@Time    : 2017/9/8 20:59
@connect : superonesfazai@gmail.com
'''

import requests
import itchat

KEY = '8edce3ce905a4c1dbb965e6b35c3834d'

def get_response(msg):
    '''
    构造要发送给服务器的数据
    :param msg:
    :return:
    '''
    api_url = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': KEY,
        'info': msg,
        'user_id': 'wechat-robot',
    }
    try:
        r = requests.post(api_url, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')
    # 为了防止服务器没有正常响应导致程序异常退出，这里捕获异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 返回一个None
        return

@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    defaultReply = 'I received: ' + msg['Text']
    # 如果图灵Key出现问题，那么reply将会是None
    reply = get_response(msg['Text'])
    # a or b的意思是，如果a有内容，那么返回a，否则返回b
    # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
    return reply or defaultReply

# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
itchat.auto_login(hotReload=True)
itchat.run()