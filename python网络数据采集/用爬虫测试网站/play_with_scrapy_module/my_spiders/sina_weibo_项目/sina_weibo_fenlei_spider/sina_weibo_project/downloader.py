# coding:utf-8

'''
@author = super_fazai
@File    : downloader.py
@Time    : 2017/9/26 15:47
@connect : superonesfazai@gmail.com
'''

import time
from scrapy.exceptions import IgnoreRequest
from scrapy.http import HtmlResponse, Response, XmlRpcRequest, Request
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from pprint import pprint
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class CustomDownloader(object):
    COOKIES = 'SINAGLOBAL=1920862274319.4636.1502628639473; httpsupgrade_ab=SSL; login_sid_t=6c2521139641765552eaeffdc3bc61bb; _s_tentry=login.sina.com.cn; Apache=5561465425422.705.1506498709692; ULV=1506498709703:7:4:1:5561465425422.705.1506498709692:1506162530082; un=15661611306; cross_origin_proto=SSL; SCF=AluwsnVuuVb8f4iOGi5k7zRy-IBKAxmfDFs-_RbHERcHdUDJGWQpJm1Ui7yG47p9R92qkWR9fwNaJgW4Ttru2hw.; SUB=_2A250z_IADeRhGeNM41sX8ybLzjmIHXVXvWTIrDV8PUNbmtBeLXDwkW9b9vZp0F8LL4lEz4GUfwkSGT0kGA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFLov-n86vP3ShBTANACnLe5JpX5KzhUgL.Fo-E1h.ce0nNSK-2dJLoI7_0UPWLMLvJqPDyIBtt; SUHB=0S7CzD56B3SmUG; ALF=1538045387; SSOLoginState=1506509392; wvr=6; YF-Page-G0=b5853766541bcc934acef7f6116c26d1; TC-Page-G0=4c4b51307dd4a2e262171871fe64f295; UOR=developer.51cto.com,widget.weibo.com,www.google.co.jp'

    def __init__(self):
        """
        初始化带cookie的驱动
        """
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap['phantomjs.page.settings.resourceTimeout'] = 1000   # 1秒
        cap['phantomjs.page.settings.loadImages'] = False
        cap['phantomjs.page.settings.disk-cache'] = True
        cap['phantomjs.page.customHeaders.Cookie'] = self.COOKIES
        print('============| phantomjs即将执行 |')
        self.driver = webdriver.PhantomJS(executable_path='/Users/afa/myFiles/tools/phantomjs-2.1.1-macosx/bin/phantomjs', desired_capabilities=cap)
        print('============| phantomjs执行成功 |')
        self.driver.set_window_size(1200, 7000)      # 设置默认大小，避免默认大小显示
        wait = ui.WebDriverWait(self.driver, 10)   # 显示等待n秒, 每过0.5检查一次页面是否加载完毕

    def visit_page(self, url):
        """
        动态js模拟网页下拉
        :param url:
        :return:
        """
        print('============| 正在加载网站...... |')
        self.driver.get(url)
        self.driver.implicitly_wait(3)
        # 滚动, 加载
        # js = "var q=document.documentElement.scrollTop=30000"     # 适用于ie, 火狐
        # js = 'window.scrollTo(0, document.body.scrollHeight)'
        # js = 'document.getElementsByClassName("obj_name")[0].scrollTop=10000'
        # js = 'document.body.scrollTop=10000'  # 适用于chrome
        js = r'''
        function scrollToBottom() {
            var Height = document.body.clientHeight,  //文本高度
                screenHeight = window.innerHeight,  //屏幕高度
                INTERVAL = 100,  // 滚动动作之间的间隔时间
                delta = 500,  //每次滚动距离
                curScrollTop = 0;    //当前window.scrollTop 值
        
            var scroll = function () {
                curScrollTop = document.body.scrollTop;
                window.scrollTo(0,curScrollTop + delta);
            };
        
            var timer = setInterval(function () {
                var curHeight = curScrollTop + screenHeight;
                if (curHeight >= Height){   //滚动到页面底部时，结束滚动
                    clearInterval(timer);
                }
                scroll();
            }, INTERVAL)
        }
        scrollToBottom()
        '''
        # self.driver.execute_script(js)    # 执行脚本
        # self.driver.implicitly_wait(5)

        # try:
        #     element = ui.WebDriverWait(self.driver, 10).until(
        #         EC.presence_of_element_located((By.CLASS_NAME, 'ficon_arrow_right'))
        #     )
        #     self.driver.find_element_by_class_name('ficon_arrow_right').click()
        #     print('============| 找到指定元素, 已点击 |')
        # except Exception as e:
        #     print('============| 没有找到点击指定元素 |')
        #     print('============| 错误如下 |', e)
        # self.driver.find_element_by_link_text('点击重新载入').click()
        self.driver.implicitly_wait(20)

        # self.driver.save_screenshot('./截图.png')       # 下拉截图方便调试
        content = self.driver.page_source.encode('utf-8')
        print('============| 网页加载完毕.......... |')
        # pprint(content.decode())
        return content

    def __del__(self):
        self.driver.quit()