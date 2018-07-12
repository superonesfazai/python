# coding:utf-8

'''
@author = super_fazai
@File    : 申通快递首页查询_滑动验证码破解.py
@Time    : 2017/7/10 11:17
@connect : superonesfazai@gmail.com
'''

from selenium import webdriver
from scrapy.selector import Selector
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from time import sleep
from my_ip_pools import MyIpPools
import random
from PIL import Image
from io import BytesIO
import gc
import uuid
# import StringIO
from io import StringIO

def _init_chrome(is_headless=True, is_pic=True, is_proxy=True):
    '''
    如果使用chrome请设置page_timeout=30
    :return:
    '''
    from selenium.webdriver.support import ui
    from selenium import webdriver

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

class Slide(object):
    """滑动验证码破解"""
    def __init__(self):
        self.driver = _init_chrome(is_headless=False, is_pic=False, is_proxy=False)
        self.wait = WebDriverWait(self.driver, 10)

    def crop(self, left, top, right, bottom, pic_name):
        """截屏并裁剪"""
        ss = Image.open(BytesIO(self.driver.get_screenshot_as_png()))
        cp = ss.crop((left, top, right, bottom))  # 注意这里顺序
        cp.save(pic_name)

        return cp

    def calc_move(self, pic1, pic2):
        """根据阈值计算移动距离"""
        pix1 = pic1.load()
        pix2 = pic2.load()
        threshold = 200
        move = 0
        # 因为滑块都从左向右滑动，而碎片本身宽度为60所以从60开始遍历
        for i in range(60, pic1.size[0]):
            flag = False
            for j in range(pic1.size[1]):
                r = abs(pix1[i, j][0] - pix2[i, j][0])
                g = abs(pix1[i, j][1] - pix2[i, j][1])
                b = abs(pix1[i, j][2] - pix2[i, j][2])
                # if r > threshold and g > threshold and b > threshold:
                # 方法1：分别判断rgb大于阈值
                # flag = True
                # break
                if r + g + b > threshold:
                    # 方法2：判断rgb总和跟阈值比较，效果比1好 为什么呢？？
                    flag = True
                    break
            if flag:
                move = i
                break

        return move

    def path1(self, distance):
        """绘制移动路径方法1，构造一个等比数列"""
        q = 0.4  # 测试后发现0.4效果最佳
        n = 10  # 最多移动几次
        a1 = ((1 - q) * distance) / (1 - q**n)
        result = []
        for o in range(1, n + 1):
            an = a1 * q**(o - 1)
            if an < 0.1:  # 小于移动阈值的就不要了
                break
            t = random.uniform(0, 0.5)  # 测试后0.5秒的间隔成功率最高
            result.append([an, 0, t])
        return result

    def path2(self, distance):
        """绘制移动路径方法2,模拟物理加速、减速运动，效果比1好"""
        result = []
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0
        while current < (distance - 10):
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
            move = v0 * t + 0.5 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            result.append([round(move), 0, random.uniform(0, 0.5)])

        return result


    def run(self):
        url = 'http://www.sto.cn/Home/Index'

        self.driver.get(url)
        css_seletor = 'li.order-search'
        self.driver.find_element_by_css_selector('li.order-search textarea').send_keys('3367154640058')
        self.driver.find_element_by_css_selector('li.order-search div.btn_order_search input').click()
        sleep(5)
        # div.layui-layer-content
        # driver.save_screenshot('申通.jpg')

        body = self.driver.page_source
        # print(body)
        bg_pic = Selector(text=body).css('img.yidun_bg-img::attr("src")').extract_first()
        slide_pic = Selector(text=body).css('img.yidun_jigsaw::attr("src")').extract_first()
        print('滑块bg:', bg_pic, ' 补足部分:', slide_pic)

        '''滑动验证码破解'''
        # 等待验证码弹出
        # bg_pic = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "yidun_bg-img")))
        bg_pic = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "layui-layer-page")))

        # html中坐标原点是左上角，右为x轴正方向，下为y轴正方向
        # 输出的x为正就是此元素距离屏幕左侧距离
        # 输出的y为正就是此元素距离屏幕上侧距离
        # 所以我们需要截图的四个距离如下：
        top, bottom, left, right = (
            bg_pic.location['y'],
            bg_pic.location['y'] + bg_pic.size['height'],
            bg_pic.location['x'],
            bg_pic.location['x'] + bg_pic.size['width'])
        print('top: {0}, bottom: {1}, left: {2}, right: {3}'.format(top, bottom, left, right))
        sleep(1)
        cp1 = self.crop(left, top, right, bottom, '1.png')

        # 获取滑块按钮并点击一下
        slide = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "yidun_slider")))
        slide.click()
        sleep(3)  # 等3秒报错信息消失 TODO 这里应该可以改进
        cp2 = self.crop(left, top, right, bottom, '2.png')
        move = self.calc_move(cp1, cp2)

        result = self.path1(move)
        # result = self.path2(move)

        # 拖动滑块
        ActionChains(self.driver).click_and_hold(slide).perform()
        for x in result:
            ActionChains(self.driver).move_by_offset(xoffset=x[0], yoffset=x[1]).perform()
            # ActionChains(driver).move_to_element_with_offset(to_element=slide,xoffset=x[0],yoffset=x[1]).perform()
            sleep(x[-1])  # 如果使用方法1则需要sleep
        sleep(0.5)
        ActionChains(self.driver).release(slide).perform()  # 释放按钮

        sleep(0.8)
        # element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "gt_info_text")))
        # ans = element.text
        # if u"通过" in ans:
        #     # 这里也需要等一下才能获取到具体的链接
        #     element = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "search_list_item")))
        #     for o in self.driver.find_elements_by_xpath(u"//a[@target='_blank']"):
        #         print(o.get_attribute("href"))
        #     self.driver.quit()
        # else:
        #     print("识别失败")
        #     self.driver.quit()

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass
        gc.collect()

class BaseGeetestCrack(object):
    """验证码破解基础类"""
    def __init__(self, driver):
        self.driver = driver
        self.driver.maximize_window()

    def input_by_id(self, text='', element_id='',
                    by_css=False, by_xpath=False, by_id=False):
        """输入查询关键词
        :text: Unicode, 要输入的文本
        :element_id: 输入框网页元素id
        """
        if by_id:
            input_el = self.driver.find_element_by_id(element_id)
        elif by_css:
            input_el = self.driver.find_element_by_css_selector(element_id)
        elif by_xpath:
            input_el = self.driver.find_element_by_xpath(element_id)
        else:
            input_el = None
            print('请选择按什么进行筛选元素!')

        input_el.clear()
        input_el.send_keys(text)
        sleep(1)

    def click_by_id(self, element_id='',
                    by_css=False, by_id=False, by_xpath=False, by_tag_name=False):
        """点击查询按钮
        :element_id: 查询按钮网页元素id
        """
        if by_id:
            search_el = self.driver.find_element_by_id(element_id)
        elif by_css:
            search_el = self.driver.find_element_by_css_selector(element_id)
        elif by_xpath:
            search_el = self.driver.find_element_by_xpath(element_id)
        elif by_tag_name:
            search_el = self.driver.find_elements_by_tag_name(element_id)
        else:
            search_el = None
            print('请选择按什么进行筛选元素!')

        # search_el.click()
        search_el.send_keys(Keys.ENTER)

        sleep(3)

    def calculate_slider_offset(self):
        """计算滑块偏移位置，必须在点击查询按钮之后调用
        :returns: Number
        """
        img1 = self.crop_captcha_image()
        self.drag_and_drop(x_offset=5)
        img2 = self.crop_captcha_image()
        w1, h1 = img1.size
        w2, h2 = img2.size
        if w1 != w2 or h1 != h2:
            return False
        left = 0
        flag = False
        for i in range(45, w1):
            for j in range(h1):
                if not self.is_pixel_equal(img1, img2, i, j):
                    left = i
                    flag = True
                    break
            if flag:
                break
        if left == 45:
            left -= 2
        return left

    def is_pixel_equal(self, img1, img2, x, y):
        pix1 = img1.load()[x, y]
        pix2 = img2.load()[x, y]
        if (abs(pix1[0] - pix2[0] < 60) and abs(pix1[1] - pix2[1] < 60) and abs(pix1[2] - pix2[2] < 60)):
            return True
        else:
            return False

    def crop_captcha_image(self, element_id="yidun_bg-img"):
        """截取验证码图片
        :element_id: 验证码图片网页元素id
        :returns: StringIO, 图片内容
        """
        captcha_el = self.driver.find_element_by_class_name(element_id)
        location = captcha_el.location
        size = captcha_el.size
        left = int(location['x'])
        top = int(location['y'])
        left = 1010
        top = 535
        # right = left + int(size['width'])
        # bottom = top + int(size['height'])
        right = left + 523
        bottom = top + 235
        print(left, top, right, bottom)

        screenshot = self.driver.get_screenshot_as_png()

        screenshot = Image.open(StringIO.StringIO(screenshot))
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save("%s.png" % uuid.uuid4().get_hex())

        return captcha

    def get_browser_name(self):
        """获取当前使用浏览器名称
        :returns: TODO
        """
        return str(self.driver).split('.')[2]

    def drag_and_drop(self, x_offset=0, y_offset=0, element_class="gt_slider_knob"):
        """拖拽滑块
        :x_offset: 相对滑块x坐标偏移
        :y_offset: 相对滑块y坐标偏移
        :element_class: 滑块网页元素CSS类名
        """
        dragger = self.driver.find_element_by_class_name(element_class)
        action = ActionChains(self.driver)
        action.drag_and_drop_by_offset(dragger, x_offset, y_offset).perform()
        # 这个延时必须有，在滑动后等待回复原状
        sleep(8)

    def move_to_element(self, element_class="gt_slider_knob"):
        """鼠标移动到网页元素上
        :element: 目标网页元素
        """
        sleep(3)
        element = self.driver.find_element_by_class_name(element_class)
        action = ActionChains(self.driver)
        action.move_to_element(element).perform()
        sleep(4.5)

    def crack(self):
        """执行破解程序
        """
        raise NotImplementedError


class IndustryAndCommerceGeetestCrack(BaseGeetestCrack):
    """滑动验证码破解类"""
    def __init__(self, driver):
        super(IndustryAndCommerceGeetestCrack, self).__init__(driver)

    def crack(self):
        """执行破解程序
        """
        # self.driver.find_element_by_css_selector('li.order-search div.btn_order_search input.btn_order_search').click()
        self.input_by_id(element_id='li.order-search textarea', by_css=True, text='3367154640058')
        self.click_by_id(element_id='input.btn_order_search', by_css=True)

        body = self.driver.page_source
        # print(body)
        bg_pic = Selector(text=body).css('img.yidun_bg-img::attr("src")').extract_first()
        slide_pic = Selector(text=body).css('img.yidun_jigsaw::attr("src")').extract_first()
        print('滑块bg:', bg_pic, ' 补足部分:', slide_pic)

        sleep(2)
        x_offset = self.calculate_slider_offset()
        self.drag_and_drop(x_offset=x_offset)

def main():
    driver = _init_chrome(is_headless=False, is_pic=True, is_proxy=False)
    url = 'http://www.sto.cn/Home/Index'
    driver.get(url)
    cracker = IndustryAndCommerceGeetestCrack(driver)
    cracker.crack()
    print(driver.get_window_size())
    sleep(3)
    driver.save_screenshot("screen.png")
    driver.close()

if __name__ == '__main__':
    # _ = Slide()
    # _.run()
    # sleep(2*60)
    main()

    
    
