# coding:utf-8

'''
@author = super_fazai
@File    : demo_2.py
@Time    : 2017/7/10 15:15
@connect : superonesfazai@gmail.com
'''

import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import gc

EMAIL = 'cqc@cuiqingcai.com'
PASSWORD = ''
BORDER = 6
INIT_LEFT = 60

def _init_chrome(is_headless=True, is_pic=True, is_proxy=True):
    '''
    如果使用chrome请设置page_timeout=30
    :return:
    '''
    from selenium.webdriver.support import ui

    CHROME_DRIVER_PATH = '/Users/afa/myFiles/tools/chromedriver'
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

class CrackGeetest():
    def __init__(self):
        self.url = 'https://account.geetest.com/login'
        self.browser = _init_chrome(is_headless=False, is_pic=False, is_proxy=False)
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.password = PASSWORD

    def __del__(self):
        self.browser.close()

    def get_geetest_button(self):
        """
        获取初始验证按钮
        :return:
        """
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
        return button

    def get_position(self):
        """
        获取验证码位置
        :return: 验证码位置元组
        """
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return (top, bottom, left, right)

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider

    def get_geetest_image(self, name='captcha.png'):
        """
        获取验证码图片
        :return: 图片对象
        """
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def open(self):
        """
        打开网页输入用户名密码
        :return: None
        """
        self.browser.get(self.url)
        email = self.wait.until(EC.presence_of_element_located((By.ID, 'email')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'password')))
        email.send_keys(self.email)
        password.send_keys(self.password)

    def get_gap(self, image1, image2):
        """
        获取缺口偏移量
        :param image1: 不带缺口图片
        :param image2: 带缺口图片
        :return:
        """
        left = 60
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left

        return left

    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                        pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -3
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def move_to_gap(self, slider, track):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        """
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()

    def login(self):
        """
        登录
        :return: None
        """
        submit = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'login-btn')))
        submit.click()
        time.sleep(10)
        print('登录成功')

    def crack(self):
        # 输入用户名密码
        self.open()
        # 点击验证按钮
        button = self.get_geetest_button()
        button.click()
        # 获取验证码图片
        image1 = self.get_geetest_image('captcha1.png')
        # 点按呼出缺口
        slider = self.get_slider()
        slider.click()
        # 获取带缺口的验证码图片
        image2 = self.get_geetest_image('captcha2.png')
        # 获取缺口位置
        gap = self.get_gap(image1, image2)
        print('缺口位置', gap)
        # 减去缺口位移
        gap -= BORDER
        # 获取移动轨迹
        track = self.get_track(gap)
        print('滑动轨迹', track)
        # 拖动滑块
        self.move_to_gap(slider, track)

        try:
            success = self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_success_radar_tip_content'), '验证成功'))
            print(success)
        except TimeoutException as e:
            print(e)
            # self.crack()
            return None

        # 失败后重试
        if not success:
            self.crack()
        else:
            self.login()

    def __del__(self):
        try:
            self.browser.quit()
        except: pass
        gc.collect()

if __name__ == '__main__':
    crack = CrackGeetest()
    crack.crack()
