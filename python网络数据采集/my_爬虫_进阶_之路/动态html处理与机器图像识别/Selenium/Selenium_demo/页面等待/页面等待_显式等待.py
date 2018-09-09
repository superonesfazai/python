# coding = utf-8

'''
@author = super_fazai
@File    : 页面等待_显式等待.py
@Time    : 2017/8/31 11:30
@connect : superonesfazai@gmail.com
'''

"""
显式等待指定某个条件，然后设置最长等待时间。
如果在这个时间还没有找到元素，那么便会抛出异常了。
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
# webDriverWait库, 负责循环等待
from selenium.webdriver.support.ui import WebDriverWait
# expected_conditions类, 负责条件触发
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get('http://www.xxxxx.com/loading')
try:
    # 页面一直循环, 直到id='myDynamicElement'出现
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'myDynamicElement')) # 注意此处是一个元组
    )
finally:
    driver.quit()

'''
如果不写参数，程序默认会 0.5s 调用一次来查看元素是否已经生成，如果本来元素就是存在的，那么会立即返回。

下面是一些内置的等待条件，你可以直接调用这些条件，而不用自己写某些等待条件了:
    title_is
    title_contains
    presence_of_element_located
    visibility_of_element_located
    visibility_of
    presence_of_all_elements_located
    text_to_be_present_in_element
    text_to_be_present_in_element_value
    frame_to_be_available_and_switch_to_it
    invisibility_of_element_located
    element_to_be_clickable – it is Displayed and Enabled.
    staleness_of
    element_to_be_selected
    element_located_to_be_selected
    element_selection_state_to_be
    element_located_selection_state_to_be
    alert_is_present
'''