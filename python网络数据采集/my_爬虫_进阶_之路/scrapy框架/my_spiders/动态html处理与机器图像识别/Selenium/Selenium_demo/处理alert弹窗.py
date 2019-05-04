# coding:utf-8

'''
@author = super_fazai
@File    : 处理alert弹窗.py
@connect : superonesfazai@gmail.com
'''

from time import sleep
# Alert 父子关系弹窗对象
from selenium.webdriver.common.alert import Alert
from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.fz_driver import (
    BaseDriver,
    FIREFOX,)

FIREFOX_DRIVER_PATH = '/Users/afa/myFiles/tools/geckodriver'
target_url = 'https://sso.volkswagen.de/kpmweb/b2bLogin.do'

d = BaseDriver(
    type=FIREFOX,
    load_images=True,
    ip_pool_type=tri_ip_pool,
    executable_path=FIREFOX_DRIVER_PATH,)

def action(d):
    d.get_url_body(url=target_url, timeout=30)
    # 刷新使出现弹窗
    d.refresh()
    alert = d.switch_to_alert()
    # alert 确认 or ok
    # alert.accept()
    # alert 取消
    # alert.dismiss()

    # alert的文本
    # text = alert.text

    # 发送文本，对有提交需求的prompt框
    # alert.send_keys('aaa')

    # 验证，针对需要身份验证的alert, 不成功!
    alert.authenticate(
        username='fzhook',
        password='pwd!',)

    # 下面这种方式成功!!
    # new_url = "https://{}:{}@sso.volkswagen.de/kpmweb/b2bLogin.do".format(username, pwd)
    # d.get_url_body(new_url)

    sleep(60)

action(d=d)
try:
    del d
except:
    pass

