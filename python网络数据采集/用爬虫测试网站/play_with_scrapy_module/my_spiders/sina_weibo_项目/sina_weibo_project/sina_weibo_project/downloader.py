# coding:utf-8

'''
@author = super_fazai
@File    : downloader.py
@Time    : 2017/9/26 15:47
@connect : superonesfazai@gmail.com
'''

import time
from scrapy.exceptions import IgnoreRequest
from scrapy.http import HtmlResponse, Response
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from pprint import pprint
from selenium.webdriver.common.keys import Keys

class CustomDownloader(object):
    COOKIES = 'SINAGLOBAL=1920862274319.4636.1502628639473; httpsupgrade_ab=SSL; _s_tentry=cuiqingcai.com; Apache=7249798919057.913.1506162529527; ULV=1506162530082:6:3:3:7249798919057.913.1506162529527:1505873317470; login_sid_t=2a41e3628a877dcd52fb5a9091b93e77; TC-Ugrow-G0=e66b2e50a7e7f417f6cc12eec600f517; TC-V5-G0=f88ad6a0154aa03e3d2a393c93b76575; YF-V5-G0=02157a7d11e4c84ad719358d1520e5d4; YF-Ugrow-G0=57484c7c1ded49566c905773d5d00f82; YF-Page-G0=f27a36a453e657c2f4af998bd4de9419; cross_origin_proto=SSL; WBStorage=9fa115468b6c43a6|undefined; UOR=developer.51cto.com,widget.weibo.com,login.sina.com.cn; SSOLoginState=1506412304; SCF=AluwsnVuuVb8f4iOGi5k7zRy-IBKAxmfDFs-_RbHERcHHeIBBuFjx2PMZUS-wHdbD5YPOfD8LUX8NcsbcXPp3rM.; SUB=_2A250zndBDeRhGeNM41sX8ybLzjmIHXVXuu-JrDV8PUNbmtBeLWXnkW8U8mBbCeUC6dQVP77W1IQLHBNsbg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFLov-n86vP3ShBTANACnLe5JpX5K2hUgL.Fo-E1h.ce0nNSK-2dJLoI7_0UPWLMLvJqPDyIBtt; SUHB=08J7I6GiMwQzNU; ALF=1537948304; un=15661611306; wvr=6'

    def __init__(self):
        """
        初始化带cookie的驱动
        """
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap['phantomjs.page.settings.resourceTimeout'] = 1000
        cap['phantomjs.page.settings.loadImages'] = True
        cap['phantomjs.page.settings.disk-cache'] = True
        cap['phantomjs.page.customHeaders.Cookie'] = self.COOKIES
        print('============| phantomjs即将执行 |')
        self.driver = webdriver.PhantomJS(executable_path='phantomjs', desired_capabilities=cap)
        print('============| phantomjs执行成功 |')
        wait = ui.WebDriverWait(self.driver, 15)   # 显示等待n秒, 每过0.5检查一次页面是否加载完毕

    def visit_page(self, url):
        """
        动态js模拟网页下拉
        :param url:
        :return:
        """
        print('============| 正在加载网站...... |')
        self.driver.get(url)
        time.sleep(4)
        # 滚动, 加载
        # js = "var q=document.documentElement.scrollTop=30000"     # 适用于ie, 火狐
        # js = 'window.scrollTo(0, document.body.scrollHeight)'
        # js = 'document.getElementsByClassName("obj_name")[0].scrollTop=10000'
        js = 'document.body.scrollTop=30000'  # 适用于chrome
        for i in range(3):
            self.driver.execute_script(js)
            time.sleep(2)      # 等待时间不宜过短，否则页面无法加载完全，测试等待20秒时，还未加载出来
        content = self.driver.page_source.encode('utf-8')
        print('============| 网页加载完毕.......... |')
        pprint(content.decode())
        return content

    def __del__(self):
        self.driver.quit()