# coding:utf-8

'''
@author = super_fazai
@File    : 每日幸运大转盘.py
@connect : superonesfazai@gmail.com
'''

from selenium import webdriver

# phantomjs驱动地址
PHANTOMJS_DRIVER_PATH = '/Users/afa/myFiles/tools/phantomjs-2.1.1-macosx/bin/phantomjs'

"""
初始化带cookie的驱动，之所以用phantomjs是因为其加载速度很快(快过chrome驱动太多)
"""

print('--->>>初始化phantomjs驱动中<<<---')
cap = webdriver.DesiredCapabilities.PHANTOMJS
cap['phantomjs.page.settings.resourceTimeout'] = 1000  # 1秒
cap['phantomjs.page.settings.loadImages'] = False
cap['phantomjs.page.settings.disk-cache'] = True
# cap['phantomjs.page.settings.userAgent'] = HEADERS[randint(0, 34)]  # 随机一个请求头
# cap['phantomjs.page.customHeaders.Cookie'] = cookies

driver = webdriver.PhantomJS(executable_path=PHANTOMJS_DRIVER_PATH, desired_capabilities=cap)

# wait = ui.WebDriverWait(self.driver, 12)  # 显示等待n秒, 每过0.5检查一次页面是否加载完毕
print('------->>>初始化完毕<<<-------')

driver.command_executor._commands['executePhantomScript'] = ('POST', '/session/$sessionId/phantom/execute')
driver.execute('executePhantomScript', {'script': 'phantom.setProxy("118.178.124.33", 3128);', 'args' : [] })

url = 'https://h5.m.taobao.com/app/detail/desc.html?_isH5Des=true#!id=546818961702&type=1&f=TB1_pjTQVXXXXX9apXX8qtpFXlX&sellerType=C'
driver.set_page_load_timeout(5)
try:
    driver.get(url)
except Exception:
    driver.save_screenshot('tmp.jpg')
    print(driver.page_source)
    driver.quit()


