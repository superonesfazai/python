# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2017/10/11 14:24
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')
from gc import collect

from settings import FIREFOX_DRIVER_PATH, CHROME_DRIVER_PATH
from PIL import Image
from fzutils.spider.selenium_always import *
from fzutils.common_utils import json_2_dict
from fzutils.ocr_utils import yundama_ocr_captcha
from fzutils.internet_utils import get_random_phone_ua

def ocr_mt_captcha():
    with open('/Users/afa/myFiles/pwd/yundama_pwd.json', 'r') as f:
        yundama_info = json_2_dict(f.read())

    username = yundama_info['username']
    pwd = yundama_info['pwd']
    app_key = yundama_info['app_key']
    res = yundama_ocr_captcha(
        username=username,
        pwd=pwd,
        app_key=app_key,
        code_type=1004, # 4位字符数字
        img_path='./mt_captcha.png')

    print('识别结果:{}'.format(res))

    return res

def _get_mt_captcha_img(driver):
    '''
    截取验证码
    :param driver:
    :return:
    '''
    driver.save_screenshot('tmp_mt.png')
    captcha_css_selector = driver.find_element_by_css_selector('#yodaImgCode')
    location = captcha_css_selector.location
    size = captcha_css_selector.size
    print('location: {}, size: {}'.format(location, size))

    # 裁剪出验证码
    img1 = Image.open('tmp_mt.png')
    left = location['x']
    upper = location['y']
    right = left + size['width']
    lower = upper + size['height']

    box = (left, upper, right, lower)
    print('box:{}'.format(box))

    img2 = img1.crop(box)
    img2.save('mt_captcha.png')

    return

# 打码接入
print('--->>> 动态打码中...')
print('初始化chrome...')
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--user-agent={0}'.format(get_random_phone_ua()))

driver = webdriver.Chrome(
    executable_path=CHROME_DRIVER_PATH,
    options=chrome_options
)
print('初始化完毕!')
try:
    driver.get('https://meishi.meituan.com/i/poi/{}'.format('168877106'))
    html = driver.page_source
    # print(html)
    if '验证中心' in html:
        # geckodriver 21.0 等待时间超过 5 秒，会提示 ConnectionResetError
        sleep(1)
        _get_mt_captcha_img(driver=driver)

        res = ocr_mt_captcha()
        while True:
            if '看不清' in res:
                print('看不清, 重新点击验证码...')
                driver.find_element_by_id('yodaNextImgCode').send_keys(Keys.ENTER)
                sleep(1)
                _get_mt_captcha_img(driver=driver)
            else:
                break

        print('输入中...')
        driver.find_element_by_css_selector('input#yodaImgCodeInput').send_keys(res)

        sleep(2)
        # TODO 报错cannot read globalerror
        driver.find_element_by_id('yodaImgCodeSure').send_keys(Keys.ENTER)
    else:
        pass
except Exception as e:
    print(e)

sleep(2* 60)
try:
    driver.quit()
except:
    pass
collect()

