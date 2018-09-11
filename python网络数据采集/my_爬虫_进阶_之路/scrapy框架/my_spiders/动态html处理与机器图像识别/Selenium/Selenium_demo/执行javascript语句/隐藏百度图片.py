# coding = utf-8

'''
@author = super_fazai
@File    : 隐藏百度图片.py
@Time    : 2017/8/31 12:22
@connect : superonesfazai@gmail.com
'''

from selenium import webdriver

driver = webdriver.PhantomJS()
driver.get('http://www.baidu.com')

# 给搜索输入框标红的javascript脚本
js = "var q=document.getElementById(\"kw\");q.style.border=\"2px solid red\";"

# 调用给搜索输入框标红的js脚本
driver.execute_script(js)

# 查看页面快照
driver.save_screenshot('redbaidu.png')

# js隐藏元素, 将获取的图片呢隐藏
img = driver.find_element_by_xpath('//*[id="lg"]/img')
driver.execute_script('$(arguments[0]).fadeOut()', img)

# 向下滚动到页面底部
driver.execute_script("$('.scroll_top').click(function(){$('html,body').animate({scrollTop: '0px'}, 800);});")

# 查看页面快照
driver.save_screenshot('nullbaidu.png')

driver.quit()