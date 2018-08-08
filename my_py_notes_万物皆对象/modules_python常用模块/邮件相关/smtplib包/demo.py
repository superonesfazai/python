# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@Time    : 2018/5/18 15:11
@connect : superonesfazai@gmail.com
'''

import json

email_passwd_json_path = '/Users/afa/email_passwd.json'

def get_email_passwd():
    try:
        with open(email_passwd_json_path, 'r') as f:
            _tmp = json.loads(f.readline())
    except FileNotFoundError:
        print('严重错误, 数据库初始配置json文件未找到!请检查!')
        return ''
    except Exception as e:
        print('错误如下: ', e)
        return ''

    else:
        return _tmp['passwd']

import smtplib
import gc
from email.mime.text import MIMEText

class FZEmail(object):
    """
    邮件obj
        目前支持: qq邮箱 [qq邮箱设置开启smtp, 并获得授权码]
    """
    def __init__(self, user, passwd, host='smtp.qq.com',):
        self.host = host
        self.user = user
        self.passwd = passwd    # 邮箱密码 or 邮箱smtp授权码
        self._init_connect()

    def _init_connect(self):
        '''
        初始化连接
        :return:
        '''
        self.server = smtplib.SMTP_SSL(self.host, 465)     # 创建一个smtp主机
        self.server.login(user=self.user, password=self.passwd)

    def send_email(self, to, subject='邮件主题', text='邮件正文'):
        '''
        发送email
        :param to:
        :param subject:
        :param text:
        :return:
        '''
        msg = MIMEText(text)  # 还可以是html eg: msg = MIMEText(r'''<html></html>''', 'html', 'utf-8')
        msg["Subject"] = subject
        msg["From"] = self.user
        msg["To"] = to

        try:
            self.server.sendmail(self.user, [to], msg.as_string())
            print('邮件发送成功!')

        except Exception as e:
            print(e)
            print('邮件发送失败!')

    def __del__(self):
        try:
            self.server.quit()  # 断开smtp连接
        except:
            pass
        gc.collect()

_ = FZEmail(user='2939161681@qq.com', passwd=get_email_passwd())
# _.send_email(to='superonesfazai@gmail.com')
# _.send_email(to='553106453@qq.com', subject='李颖丹大猪头!', text='起床了, pig running....')