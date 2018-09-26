# coding:utf-8

'''
@author = super_fazai
@File    : taowaimai_spider.py
@connect : superonesfazai@gmail.com
'''

"""
淘宝外卖: 假装不知道sign如何签名[sign已被我破解:)]
    下面采用driver拦截请求的方式
"""

from gc import collect
from pprint import pprint
from scrapy.selector import Selector
from fzutils.spider.fz_driver import (
    BaseDriver,
    FIREFOX,)
from fzutils.spider.selenium_always import *

FIREFOX_DRIVER_PATH = '/Users/afa/myFiles/tools/geckodriver'

class TaoWaiMaiSpider(object):
    def __init__(self):
        self.driver = BaseDriver(
            type=FIREFOX,
            executable_path=FIREFOX_DRIVER_PATH,
            headless=False,
            load_images=True,
        ).driver
        self.search_key = '杭州'

    def _actions(self):
        '''
        行为
        :return:
        '''
        url = 'https://h5.m.taobao.com/app/waimai/index.html#/'
        self.driver.get(url)
        sleep(3)

        try:
            self.driver.find_element_by_css_selector('div.location span').click()
            sleep(2)
            self.driver.find_element_by_css_selector('div.search input').send_keys(self.search_key)
            sleep(2.5)
            # add_p_list = self.driver.find_elements_by_css_selector('.search-result div.add-list div.item-wrap p.address')
            # pprint(add_p_list)
            # add_p_list[0].send_keys(Keys.ENTER)
            # 默认点第一个
            # self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Crocker St914'])[1]/preceding::p[22]").click()
            print('请点击选择定位处...')
            sleep(10)
            # scroll_js = '''document.body.scrollTop=10000'''
            scroll_js = r'''
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
            self.driver.execute_script(script=scroll_js)
            sleep(5)
            body = self.driver.page_source

            # div.list div.list-item
            shop_list = Selector(text=body).css('div.list div.list-item ::text').extract() or []
            pprint(shop_list)

        except Exception as e:
            print(e)

        sleep(60)

    def __del__(self):
        try:
            del self.driver
        except:
            pass
        collect()

if __name__ == '__main__':
    _ = TaoWaiMaiSpider()
    _._actions()





