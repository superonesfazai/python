# coding:utf-8

'''
@author = super_fazai
@File    : tasks.py
@connect : superonesfazai@gmail.com
'''

base_url = "http://www.geetest.com/type"

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from PIL import Image
import time
import numpy as np
import gc

def get_snap(driver, names):
    driver.save_screenshot(names)
    page_snap_obj = Image.open(names)
    return page_snap_obj


def get_image(driver, names):
    img = driver.find_element_by_class_name('geetest_canvas_img')
    time.sleep(2)
    location = img.location
    size = img.size

    left = location['x']
    top = location['y']
    right = left + size['width']
    bottom = top + size['height']

    page_snap_obj = get_snap(driver, names)
    image_obj = page_snap_obj.crop((left, top, right, bottom))
    # image_obj.show()
    return image_obj

def get_distance(image1, image2):
    start = int(np.ceil(image2.size[0] / 4))
    threhold = 120

    for i in range(start, image1.size[0]):
        for j in range(image1.size[1]):
            rgb1 = image1.load()[i, j]
            rgb2 = image2.load()[i, j]
            res1 = abs(rgb1[0] - rgb2[0])
            res2 = abs(rgb1[1] - rgb2[1])
            res3 = abs(rgb1[2] - rgb2[2])
            # print(res1,res2,res3)
            if not (res1 < threhold and res2 < threhold and res3 < threhold):
                return i - 4
    return i - 4


def get_tracks(distance):
    '''
    本质来源于物理学中的加速度算距离： s = vt + 1/2 at^2
                                    v = v_0 + at

    在这里：总距离S= distance+20
            加速度：前3/5S加速度2，后半部分加速度是-3

    '''
    distance += 20  # 先滑过一点，最后再反着滑动回来
    v = 0
    t = 0.2
    forward_tracks = []

    current = 0
    mid = distance * 3 / 5
    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3

        s = v * t + 0.5 * a * (t ** 2)
        v = v + a * t
        current += s
        forward_tracks.append(round(s))

    # 反着滑动到准确位置
    back_tracks = [-3, -3, -3, -2, -2, -1, -2, -1, -1, -1]  # 总共等于-10

    return {'forward_tracks': list(forward_tracks), 'back_tracks': back_tracks}


# 判断元素是否存在
# 'geetest_success_radar_tip'
def isElementExist(driver, element):
    flag = True
    browser = driver
    try:
        browser.find_element_by_class_name(element)
        return flag

    except:
        flag = False
        return flag

CHROME_DRIVER_PATH = '/Users/afa/myFiles/tools/chromedriver'

def _init_chrome(is_headless=True, is_pic=True, is_proxy=True):
    '''
    如果使用chrome请设置page_timeout=30
    :return:
    '''
    from selenium.webdriver.support import ui

    print('--->>>初始化chrome驱动中<<<---')
    chrome_options = webdriver.ChromeOptions()
    if is_headless:
        chrome_options.add_argument('--headless')     # 注意: 设置headless无法访问网页
    # 谷歌文档提到需要加上这个属性来规避bug
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')  # required when running as root user. otherwise you would get no sandbox errors.

    # chrome_options.add_argument('window-size=1200x600')   # 设置窗口大小

    # 设置无图模式
    if is_pic:
        prefs = {
            'profile.managed_default_content_settings.images': 2,
        }
        chrome_options.add_experimental_option("prefs", prefs)

    # 设置代理
    if is_proxy:
        ip_object = MyIpPools()
        proxy_ip = ip_object._get_random_proxy_ip().replace('http://', '') if isinstance(ip_object._get_random_proxy_ip(), str) else ''
        if proxy_ip != '':
            chrome_options.add_argument('--proxy-server={0}'.format(proxy_ip))

    '''无法打开https解决方案'''
    # 配置忽略ssl错误
    capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    capabilities['acceptSslCerts'] = True
    capabilities['acceptInsecureCerts'] = True

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    # 修改user-agent
    chrome_options.add_argument('--user-agent={0}'.format(user_agent))

    # 忽视证书错误
    chrome_options.add_experimental_option('excludeSwitches', ['ignore-certificate-errors'])

    driver = webdriver.Chrome(
        executable_path=CHROME_DRIVER_PATH,
        chrome_options=chrome_options,
        desired_capabilities=capabilities
    )
    wait = ui.WebDriverWait(driver, 30)  # 显示等待n秒, 每过0.5检查一次页面是否加载完毕
    print('------->>>初始化完毕<<<-------')

    return driver

def my_scrapy():
    driver = _init_chrome(is_headless=False, is_pic=False, is_proxy=False)
    try:
        # 1、输入账号密码回车
        driver.implicitly_wait(3)
        driver.get("http://www.geetest.com/type")

        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="app"]/section/div/ul/li[2]/h2').click()
        # 1获取全相
        time.sleep(2)
        driver.find_element_by_class_name('geetest_wait').click()
        time.sleep(1)
        image1 = get_image(driver, 'before.png')

        # 2获取有缺口的图像
        driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/div[1]/div[2]/div[2]').click()
        image2 = get_image(driver, 'after.png')

        # 3对比两种图片的像素点，找出位移
        distance = get_distance(image1, image2)

        # 4模拟人的行为习惯，根据总位移得到行为轨迹
        tracks = get_tracks(distance)
        # print(tracks)

        # 5按照行动轨迹先正向滑动，后反滑动
        button = driver.find_element_by_class_name('geetest_slider_button')
        ActionChains(driver).click_and_hold(button).perform()

        # 6正常滑动
        for track in tracks['forward_tracks']:
            ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()

        # 7返回
        time.sleep(0.5)
        for back_track in tracks['back_tracks']:
            ActionChains(driver).move_by_offset(xoffset=back_track, yoffset=0).perform()

        # 8小幅晃动模拟人操作
        ActionChains(driver).move_by_offset(xoffset=-3, yoffset=0).perform()
        ActionChains(driver).move_by_offset(xoffset=3, yoffset=0).perform()

        ActionChains(driver).move_by_offset(xoffset=2, yoffset=0).perform()
        ActionChains(driver).move_by_offset(xoffset=-2, yoffset=0).perform()

        # 9松开滑块
        time.sleep(0.5)
        ActionChains(driver).release().perform()

        # 10记录本次是否验证成功
        time.sleep(3)
        if driver.find_element_by_class_name('geetest_success_radar_tip').text == '':
            success_tag = False
        else:
            success_tag = True
        return success_tag
    except Exception as e:
        print(e)

    finally:
        driver.close()
        gc.collect()

if __name__ == '__main__':

    my_success = 0
    for i in range(0, 500):
        my_test = my_scrapy()
        print('[+]第' + str(i + 1) + r'/500次模拟状态:' + str(my_test))
        if my_test:
            my_success += 1

    print(my_success)