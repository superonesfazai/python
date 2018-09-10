# coding:utf-8

'''
@author = super_fazai
@File    : zhihu_pc_login.py
@connect : superonesfazai@gmail.com
'''

from scrapy.selector import Selector
from time import sleep
from random import choice
from selenium.webdriver import (
    Firefox,
    FirefoxProfile,)
from gc import collect
from pprint import pprint
from base64 import b64decode

from fzutils.spider.fz_phantomjs import (
    CHROME,
    BaseDriver,)
from fzutils.common_utils import json_2_dict
from fzutils.common_utils import save_base64_img_2_local
from fzutils.ocr_utils import baidu_ocr_captcha
from fzutils.internet_utils import get_random_phone_ua

# chrome驱动
CHROME_DRIVER_PATH = '/Users/afa/myFiles/tools/chromedriver'
# phantomjs驱动
PHANTOMJS_DRIVER_PATH = '/Users/afa/myFiles/tools/phantomjs-2.1.1-macosx/bin/phantomjs'
# firefox驱动
FIREFOX_DRIVER_PATH = '/Users/afa/myFiles/tools/geckodriver'

zhihu_pwd_file_path = '/Users/afa/myFiles/pwd/zhihu_pwd.json'

class ZhiHuLogin(object):
    def __init__(self):
        # self.driver = BaseDriver(
        #     type=CHROME,
        #     executable_path=CHROME_DRIVER_PATH,
        #     chrome_visualizate=True,
        #     chrome_use_proxy=False,
        # ).driver
        firefox_profile = FirefoxProfile()
        firefox_profile.set_preference("general.useragent.override", get_random_phone_ua())
        self.driver = Firefox(executable_path=FIREFOX_DRIVER_PATH, firefox_profile=firefox_profile)
        self.pwd_info_list = self._get_pwd_info()
        one = choice(self.pwd_info_list)
        self.username = one['username']
        self.pwd = one['pwd']

    def _get_pwd_info(self) -> list:
        with open(zhihu_pwd_file_path, 'r') as f:
            pwd_info = json_2_dict(f.read())

            return pwd_info

    def action(self):
        '''
        :return:
        '''
        driver = self.driver
        driver.get("https://www.zhihu.com/signup")
        sleep(3)
        self.driver.find_element_by_css_selector('div.Login-signinButtons button.Button').click()
        sleep(1)
        # self.driver.save_screenshot('./images/tmp.png')
        sleep(2)
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys(self.username)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys(self.pwd)
        sleep(1)
        driver.find_element_by_css_selector('button.Login-submitButton').click()
        sleep(1)
        body = driver.page_source
        # print(body)

        img_captcha = Selector(text=body).css('img.Captcha-chineseImg ::attr("src")').extract_first()
        print(img_captcha)
        save_res = save_base64_img_2_local(save_path='./images/captcha.jpg', base64_img_str=img_captcha)
        if img_captcha != '':
            if save_res:    # 倒立字的情况
                print('倒立字的情况')
                pass
            else:           # 验证码的情况, 先不处理
                print('验证码的情况')
                with open('./images/captcha.jpg', 'wb') as f:
                    base64_img_str = b64decode(img_captcha)
                    f.write(base64_img_str)
                return False
        else:
            print('img_captcha为空值!')

        # TODO 出现: Missing argument grant_type
        sleep(10)
        # sleep(8)
        # driver.find_element_by_css_selector('button.SignFlow-submitButton').click()


    def __del__(self):
        try:
            del self.driver
        except:
            pass
        collect()

def orc():
    '''识别验证码'''
    baidu_orc_info_path = '/Users/afa/baidu_orc.json'
    with open(baidu_orc_info_path, 'r') as f:
        baidu_orc_info = json_2_dict(f.read())

    img_path = './images/captcha.jpg'
    app_id = str(baidu_orc_info['app_id'])
    api_key = baidu_orc_info['api_key']
    secret_key = baidu_orc_info['secret_key']

    orc_res = baidu_ocr_captcha(
        app_id=app_id,
        api_key=api_key,
        secret_key=secret_key,
        img_path=img_path,
        orc_type=1)
    pprint(orc_res)

    return orc_res

# e.currentTarget.disabled
# r.handleClick
# v3/oauth/sign_in

if __name__ == "__main__":
    _ = ZhiHuLogin()
    _.action()
    sleep(2*60)
    # res = orc()
    pass
