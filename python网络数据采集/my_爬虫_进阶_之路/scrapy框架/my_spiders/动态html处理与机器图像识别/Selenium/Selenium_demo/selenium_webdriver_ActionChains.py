# coding = utf-8

'''
@author = super_fazai
@File    : selenium_webdriver_ActionChains.py
@connect : superonesfazai@gmail.com
'''

from selenium.webdriver import ActionChains     # 导入ActionChains类
from selenium import webdriver

# 调用环境变量指定的PhantomJS浏览器创建浏览对象
driver = webdriver.PhantomJS()

# 鼠标移到ac位置
ac = driver.find_element_by_xpath('element')
ActionChains(driver).move_to_element(ac).perform()

# 在ac位置单击
ac = driver.find_element_by_xpath('elementA')
ActionChains(driver).move_to_element(ac).click(ac).perform()

# 在ac位置双击
ac = driver.find_element_by_xpath('elementB')
ActionChains(driver).move_to_element(ac).double_click(ac).perform()

# 在ac位置右击
ac =  driver.find_element_by_xpath('elementC')
ActionChains(driver).move_to_element(ac).context_click(ac).perform()

# 在ac位置左键单击hold住
ac = driver.find_element_by_xpath('elementF')
ActionChains(driver).move_to_element(ac).click_and_hold(ac).perform()

# 将ac1拖拽到ac2位置
ac1 = driver.find_element_by_xpath('elementD')
ac2 = driver.find_element_by_xpath('elementE')
ActionChains(driver).drag_and_drop(ac1, ac2).perform()

