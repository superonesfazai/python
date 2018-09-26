# coding:utf-8

'''
@author = super_fazai
@File    : tao_news_auxiliary_tools.py
@connect : superonesfazai@gmail.com
'''

"""
淘新闻 自动化阅读辅助
"""

import gc
from pprint import pprint
from time import sleep
from appium import webdriver

class TaoNewsOps(object):
    def __init__(self):
        # 驱动配置
        server = "http://localhost:4723/wd/hub"
        desired_caps = {
            "platformName": "Android",
            "deviceName": "fz_5_0_0",
            'appPackage': 'com.coohua.xinwenzhuan',
            'appActivity': '.controller.MainActivity',
        }
        self.driver = webdriver.Remote(
            command_executor=server,
            desired_capabilities=desired_caps)

    def _action(self):
        print('运行开始...')
        sleep(5)
        self.driver.find_element_by_id('com.coohua.xinwenzhuan:id/guide_skip').click()
        sleep(2)

        # 进入第一篇文章
        try:
            title_list = self.driver.find_elements_by_id('com.coohua.xinwenzhuan:id/tab_feed__item_img_multi_title')
            pprint(title_list)
            title_list[0].click()
            sleep(3.5)
            # print(self.driver.current_context)  # NATIVE_APP
            print(self.driver.page_source)
        except Exception as e:
            print(e)
            return

        index = 1
        while True:
            print('{} 一次行为进行中...'.format(index))
            try:
                self.driver.swipe(0, 1000, 0, 200)      # 底部往上滑动
                sleep(4)
                label = ['-', '未']
                try:
                    # TODO 点击查看全文
                    look_all_button_list = self.driver.find_elements_by_id('com.coohua.xinwenzhuan:id/tab_text')
                    pprint(look_all_button_list)
                    look_all_button_list[2].click()
                    # self.driver.find_element_by_xpath("//*[@text='查看全文 ']").click()
                    label = ['+', '']
                    sleep(2)
                except Exception as e:
                    pass
                finally:
                    print('[{}] {}发现查看全文按钮!'.format(label[0], label[1]))

                for i in range(2):
                    self.driver.swipe(0, 1000, 0, 200)
                    sleep(2)

                # body = self.driver.page_source
                # print(body)
                child_title = self.driver.find_elements_by_id('com.coohua.xinwenzhuan:id/tab_feed__item_img_multi_title')
                pprint(child_title)
                child_title[0].click()
                sleep(2)
            except Exception as e:
                print(e)
                self.driver.find_element_by_id('com.coohua.xinwenzhuan:id/xlxl_actionbar_up').click()
                sleep(3)
            finally:
                index += 1

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    _ = TaoNewsOps()
    _._action()