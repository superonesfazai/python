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
    COOKIES = 'SINAGLOBAL=1920862274319.4636.1502628639473; httpsupgrade_ab=SSL; _s_tentry=cuiqingcai.com; Apache=7249798919057.913.1506162529527; ULV=1506162530082:6:3:3:7249798919057.913.1506162529527:1505873317470; login_sid_t=2a41e3628a877dcd52fb5a9091b93e77; TC-Ugrow-G0=e66b2e50a7e7f417f6cc12eec600f517; TC-V5-G0=f88ad6a0154aa03e3d2a393c93b76575; YF-V5-G0=02157a7d11e4c84ad719358d1520e5d4; YF-Ugrow-G0=57484c7c1ded49566c905773d5d00f82; YF-Page-G0=f27a36a453e657c2f4af998bd4de9419; cross_origin_proto=SSL; WBStorage=9fa115468b6c43a6|undefined; UOR=developer.51cto.com,widget.weibo.com,login.sina.com.cn; SSOLoginState=1506412304; SCF=AluwsnVuuVb8f4iOGi5k7zRy-IBKAxmfDFs-_RbHERcHHeIBBuFjx2PMZUS-wHdbD5YPOfD8LUX8NcsbcXPp3rM.; SUB=_2A250zndBDeRhGeNM41sX8ybLzjmIHXVXuu-JrDV8PUNbmtBeLWXnkW8U8mBbCeUC6dQVP77W1IQLHBNsbg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFLov-n86vP3ShBTANACnLe5JpX5K2hUgL.Fo-E1h.ce0nNSK-2dJLoI7_0UPWLMLvJqPDyIBtt; SUHB=08J7I6GiMwQzNU; ALF=1537948304; un=15661611306; wvr=6'

    def __init__(self):
        """
        初始化带cookie的驱动
        """
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap['phantomjs.page.settings.resourceTimeout'] = 5000   # 5秒
        cap['phantomjs.page.settings.loadImages'] = True
        cap['phantomjs.page.settings.disk-cache'] = True
        cap['phantomjs.page.customHeaders.Cookie'] = self.COOKIES
        print('============| phantomjs即将执行 |')
        self.driver = webdriver.PhantomJS(executable_path='/Users/afa/myFiles/tools/phantomjs-2.1.1-macosx/bin/phantomjs', desired_capabilities=cap)
        print('============| phantomjs执行成功 |')
        wait = ui.WebDriverWait(self.driver, 10)   # 显示等待n秒, 每过0.5检查一次页面是否加载完毕

    def visit_page(self, url):
        """
        动态js模拟网页下拉
        :param url:
        :return:
        """
        print('============| 正在加载网站...... |')
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        # 滚动, 加载
        # js = "var q=document.documentElement.scrollTop=30000"     # 适用于ie, 火狐
        # js = 'window.scrollTo(0, document.body.scrollHeight)'
        # js = 'document.getElementsByClassName("obj_name")[0].scrollTop=10000'
        # js = 'document.body.scrollTop=10000'  # 适用于chrome
        """
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
        self.driver.execute_script(js)
        self.driver.implicitly_wait(30)
        try:
            element = ui.WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.LINK_TEXT, '点击重新载入'))
            )
            self.driver.find_element_by_link_text('点击重新载入').click()
            print('============| 找到指定元素, 已点击 |')
        except Exception as e:
            print('============| 没有找到点击指定元素 |')
            print('============| 错误如下 |', e)
        # self.driver.find_element_by_link_text('点击重新载入').click()
        time.sleep(10)
        # self.driver.implicitly_wait(30)
        """
        # source: 351354573
        # status_type: 0
        # callback: STK_150647103925612

        '''
        # ajwvr: 6
        # domain: 102803
        # _ctg1_6288_ - _ctg1_6288
        # from:faxian_hot
        # mod: fenlei
        pagebar: 0
        # tab: home
        current_page: 1
        # pre_page: 1
        # page: 1
        # pl_name: Pl_Core_NewMixFeed__3
        # id: 102803
        # _ctg1_6288_ - _ctg1_6288
        # script_uri: / 102803
        # _ctg1_6288_ - _ctg1_6288
        # feed_type: 1
        # domain_op: 102803
        # _ctg1_6288_ - _ctg1_6288
        __rnd: 1506471272094

        ajwvr: 6
        domain: 102803
        _ctg1_6288_ - _ctg1_6288
        from:faxian_hot
        mod: fenlei
        pagebar: 1
        tab: home
        current_page: 2
        pre_page: 1
        page: 1
        pl_name: Pl_Core_NewMixFeed__3
        id: 102803
        _ctg1_6288_ - _ctg1_6288
        script_uri: / 102803
        _ctg1_6288_ - _ctg1_6288
        feed_type: 1
        domain_op: 102803
        _ctg1_6288_ - _ctg1_6288
        __rnd: 1506471442609

        ajwvr: 6
        domain: 102803
        _ctg1_6288_ - _ctg1_6288
        from:faxian_hot
        mod: fenlei
        pagebar: 2
        tab: home
        current_page: 3
        pre_page: 1
        page: 1
        pl_name: Pl_Core_NewMixFeed__3
        id: 102803
        _ctg1_6288_ - _ctg1_6288
        script_uri: / 102803
        _ctg1_6288_ - _ctg1_6288
        feed_type: 1
        domain_op: 102803
        _ctg1_6288_ - _ctg1_6288
        __rnd: 1506471503611

        ajwvr: 6
        domain: 102803
        _ctg1_6288_ - _ctg1_6288
        from:faxian_hot
        mod: fenlei
        pagebar: 3
        tab: home
        current_page: 4
        pre_page: 1
        page: 1
        pl_name: Pl_Core_NewMixFeed__3
        id: 102803
        _ctg1_6288_ - _ctg1_6288
        script_uri: / 102803
        _ctg1_6288_ - _ctg1_6288
        feed_type: 1
        domain_op: 102803
        _ctg1_6288_ - _ctg1_6288
        __rnd: 1506471533330

        ajwvr: 6
        domain: 102803
        _ctg1_6288_ - _ctg1_6288
        from:faxian_hot
        mod: fenlei
        pagebar: 3
        tab: home
        current_page: 4
        pre_page: 1
        page: 1
        pl_name: Pl_Core_NewMixFeed__3
        id: 102803
        _ctg1_6288_ - _ctg1_6288
        script_uri: / 102803
        _ctg1_6288_ - _ctg1_6288
        feed_type: 1
        domain_op: 102803
        _ctg1_6288_ - _ctg1_6288
        __rnd: 1506470595511

        ajwvr: 6
        domain: 102803
        _ctg1_6288_ - _ctg1_6288
        from:faxian_hot
        mod: fenlei
        pagebar: 4
        tab: home
        current_page: 5
        pre_page: 1
        page: 1
        pl_name: Pl_Core_NewMixFeed__3
        id: 102803
        _ctg1_6288_ - _ctg1_6288
        script_uri: / 102803
        _ctg1_6288_ - _ctg1_6288
        feed_type: 1
        domain_op: 102803
        _ctg1_6288_ - _ctg1_6288
        __rnd: 1506470640973

        ajwvr: 6
        domain: 102803
        _ctg1_6288_ - _ctg1_6288
        from:faxian_hot
        mod: fenlei
        pre_page: 1
        page: 2
        pids: Pl_Core_NewMixFeed__3
        current_page: 6
        since_id:
        pl_name: Pl_Core_NewMixFeed__3
        id: 102803
        _ctg1_6288_ - _ctg1_6288
        script_uri: / 102803
        _ctg1_6288_ - _ctg1_6288
        feed_type: 1
        domain_op: 102803
        _ctg1_6288_ - _ctg1_6288
        __rnd: 1506470811418

        ajwvr: 6
        domain: 102803
        _ctg1_6288_ - _ctg1_6288
        from:faxian_hot
        mod: fenlei
        pagebar: 0
        tab: home
        current_page: 7
        pre_page: 2
        page: 2
        pl_name: Pl_Core_NewMixFeed__3
        id: 102803
        _ctg1_6288_ - _ctg1_6288
        script_uri: / 102803
        _ctg1_6288_ - _ctg1_6288
        feed_type: 1
        domain_op: 102803
        _ctg1_6288_ - _ctg1_6288
        __rnd: 1506470845858
        '''

        # ajwvr: 6
        # domain: 102803
        # _ctg1_6288_ - _ctg1_6288
        # from:faxian_hot
        # mod: fenlei
        pagebar: 0
        # tab: home
        current_page: 1
        # pre_page: 1
        # page: 1
        # pl_name: Pl_Core_NewMixFeed__3
        # id: 102803
        # _ctg1_6288_ - _ctg1_6288
        # script_uri: / 102803
        # _ctg1_6288_ - _ctg1_6288
        # feed_type: 1
        # domain_op: 102803
        # _ctg1_6288_ - _ctg1_6288
        __rnd: 1506471272094

        domain = '102803_ctg1_{}_-_ctg1_{}'.format(str(6288), str(6288))
        id = domain
        pagebar = str(0)
        current_page = str(1)
        script_uri = r'/102803_ctg1_{}_-_ctg1_{}'.format(str(6288), str(6288))
        domain_op = domain
        __rnd = str(150647) + ''
        update_url = 'https://d.weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&from=faxian_hot&mod=fenlei&tab=home&pre_page=1&page=1&pl_name=Pl_Core_NewMixFeed__3&feed_type=1&domain={}&pagebar={}&current_page={}&id={}&script_uri={}&domain_op={}'\
            .format(domain, pagebar, current_page, id, script_uri, domain_op)
        # request = Request(method='get', )

        ## 正常刷新4次，第五次要点击 查看跟多，如此循环
        self.driver.get(update_url)
        time.sleep(10)
        self.driver.save_screenshot('./下拉截图.png')       # 下拉截图方便调试
        # time.sleep(20)
        # 等待时间不宜过短，否则页面无法加载完全，测试等待20秒时，还未加载出来
        content = self.driver.page_source.encode('utf-8')
        print('============| 网页加载完毕.......... |')
        # pprint(content.decode())
        return content

    def __del__(self):
        self.driver.quit()