# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@Time    : 2017/7/10 11:52
@connect : superonesfazai@gmail.com
'''

"""
国企改版不用滑动验证码了
"""

import time
import random
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

CHROME_DRIVER_PATH = '/Users/afa/myFiles/tools/chromedriver'

class Slide(object):
    """滑动验证码破解"""

    def __init__(self, target):
        self.target = target  # 要搜索的公司名称
        self.driver = webdriver.Chrome(CHROME_DRIVER_PATH)
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
        self.driver.get("http://www.gsxt.gov.cn/index")
        sleep(5)
        input_box = self.driver.find_element_by_id('keyword')
        input_box.send_keys(self.target)
        search_btn = self.driver.find_element_by_id('btn_query')
        time.sleep(3)  # 注意这里等一下再点，否则会出现卡死现象
        search_btn.click()
        # 等待验证码弹出
        bg_pic = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                                                                 "gt_cut_fullbg")))
        # html中坐标原点是左上角，右为x轴正方向，下为y轴正方向
        # 输出的x为正就是此元素距离屏幕左侧距离
        # 输出的y为正就是此元素距离屏幕上侧距离
        # 所以我们需要截图的四个距离如下：
        top, bottom, left, right = (
            bg_pic.location['y'], bg_pic.location['y'] + bg_pic.size['height'],
            bg_pic.location['x'], bg_pic.location['x'] + bg_pic.size['width'])
        time.sleep(1)
        cp1 = self.crop(left, top, right, bottom, '1.png')

        # 获取滑块按钮并点击一下
        slide = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                                                                "gt_slider_knob")))
        slide.click()
        time.sleep(3)  # 等3秒报错信息消失 TODO 这里应该可以改进
        cp2 = self.crop(left, top, right, bottom, '2.png')
        move = self.calc_move(cp1, cp2)

        result = self.path1(move)
        # result = self.path2(move)

        # 拖动滑块
        ActionChains(self.driver).click_and_hold(slide).perform()
        for x in result:
            ActionChains(self.driver).move_by_offset(xoffset=x[0],yoffset=x[1]).perform()
            # ActionChains(driver).move_to_element_with_offset(to_element=slide,xoffset=x[0],yoffset=x[1]).perform()
            time.sleep(x[-1]) # 如果使用方法1则需要sleep
        time.sleep(0.5)
        ActionChains(self.driver).release(slide).perform() # 释放按钮

        time.sleep(0.8)
        element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "gt_info_text")))
        ans = element.text
        if u"通过" in ans:
            # 这里也需要等一下才能获取到具体的链接
            element = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "search_list_item")))
            for o in self.driver.find_elements_by_xpath(u"//a[@target='_blank']"):
                print(o.get_attribute("href"))
            self.driver.quit()
        else:
            print("识别失败")
            self.driver.quit()

    def __del__(self):
        try:
            self.driver.quit()
        except: pass


if __name__ == '__main__':
    s = Slide('中国平安')
    s.run()
    del s
