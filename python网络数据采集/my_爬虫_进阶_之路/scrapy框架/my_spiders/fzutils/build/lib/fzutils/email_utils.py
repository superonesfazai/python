# coding:utf-8

import smtplib
from gc import collect
from email.mime.text import MIMEText

__all__ = [
    'FZEmail',              # 邮件对象
]

class FZEmail(object):
    """
    邮件obj
        目前支持: qq邮箱 [qq邮箱设置开启smtp, 并获得授权码]
        用法: eg:
            _ = FZEmail(user='2939161681@qq.com', passwd='smtp授权码or密码')
            _.send_email(to=['superonesfazai@gmail.com',])
    """
    def __init__(self, user, passwd, host='smtp.qq.com', port=465):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd    # 邮箱密码 or 邮箱smtp授权码
        self._init_connect()

    def _init_connect(self):
        '''
        初始化连接
        :return:
        '''
        self.server = smtplib.SMTP_SSL(self.host, self.port)     # 创建一个smtp主机
        self.server.login(user=self.user, password=self.passwd)

    def send_email(self, to, subject='邮件主题', text='邮件正文'):
        '''
        发送email
        :param to: a list eg: ["superonesfazai@gmail.com", ...]
        :param subject:
        :param text:
        :return:
        '''
        if not isinstance(to, list):
            raise ValueError('to类型为list, 格式eg: ["superonesfazai@gmail.com", ...]')

        msg = MIMEText(text)  # 还可以是html eg: msg = MIMEText(r'''<html></html>''', 'html', 'utf-8')
        msg["Subject"] = subject
        msg["From"] = self.user
        msg["To"] = to

        try:
            self.server.sendmail(self.user, to, msg.as_string())
            print('邮件发送成功!')

        except Exception as e:
            print(e)
            print('邮件发送失败!')

    def __del__(self):
        try:
            self.server.quit()  # 断开smtp连接
        except:
            pass
        collect()