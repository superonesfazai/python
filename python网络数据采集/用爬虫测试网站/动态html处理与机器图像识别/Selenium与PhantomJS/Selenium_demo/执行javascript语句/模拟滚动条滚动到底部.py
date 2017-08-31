# coding = utf-8

'''
@author = super_fazai
@File    : 模拟滚动条滚动到底部.py
@Time    : 2017/8/31 12:29
@connect : superonesfazai@gmail.com
'''

from selenium import webdriver
import time

driver = webdriver.PhantomJS()
driver.get('https://movie.douban.com/typerank?type_name=剧情&type=11&interval_id=100:90&action=')

# 向下滚动10000像素
js = 'document.body.scrollTop=10000'
# js="var q=document.documentElement.scrollTop=10000"
time.sleep(3)

# 查看页面快照
driver.save_screenshot('douban.png')

# 执行js语句
driver.execute_script(js)
time.sleep(10)

# 查看页面快照
driver.save_screenshot('newdouban.png')

driver.quit()