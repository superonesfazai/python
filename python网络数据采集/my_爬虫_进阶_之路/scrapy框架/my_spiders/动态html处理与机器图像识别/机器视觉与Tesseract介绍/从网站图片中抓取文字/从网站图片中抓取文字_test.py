# coding = utf-8

'''
@author = super_fazai
@File    : 从网站图片中抓取文字_test.py
@connect : superonesfazai@gmail.com
'''

"""
知乎动态验证码:https://www.zhihu.com/captcha.gif
下面演示:首先导航到托尔斯泰的《战争与和平》的大字号印刷版1, 
打开阅读器,收集图片的 URL 链接,然后下载图片,识别图片,最后打印每个图片的文 字
"""

import time
from urllib.request import urlretrieve
import subprocess
from selenium import webdriver

# 创建新的Selenium driver
driver = webdriver.PhantomJS()

# 用Selenium试试Firefox浏览器:
# driver = webdriver.Firefox()

driver.get("http://www.amazon.com/War-Peace-Leo-Nikolayevich-Tolstoy/dp/1427030200")
driver.find_element_by_id("sitbLogoImg").click()    # 单击图书预览按钮
imageList = set()

time.sleep(5)   # 等待页面加载完成

# 当向右箭头可以点击时,开始翻页
while "pointer" in driver.find_element_by_id("sitbReaderRightPageTurner").get_attribute("style"):
    driver.find_element_by_id("sitbReaderRightPageTurner").click()
    time.sleep(2)

    # 获取已加载的新页面(一次可以加载多个页面,但是重复的页面不能加载到集合中)
    pages = driver.find_elements_by_xpath("//div[@class='pageImage']/div/img")
    for page in pages:
        image = page.get_attribute("src")
        imageList.add(image)
driver.quit()

# 用Tesseract处理我们收集的图片URL链接
for image in sorted(imageList):
    # 保存图片
    urlretrieve(image, "page.jpg")
    p = subprocess.Popen(["tesseract", "page.jpg", "page"], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    f = open("page.txt", "r")
    p.wait()
    print(f.read())