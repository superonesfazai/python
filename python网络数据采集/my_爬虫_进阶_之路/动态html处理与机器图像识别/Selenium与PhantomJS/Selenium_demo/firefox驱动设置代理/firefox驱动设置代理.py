# coding:utf-8

'''
@author = super_fazai
@File    : firefox驱动设置代理.py
@Time    : 2017/11/1 10:45
@connect : superonesfazai@gmail.com
'''

from selenium import webdriver

# ip_ip = ip.split(":")[0]
# ip_port = int(ip.split(":")[1])
# print(ip_ip)
# print(ip_port)
# random_header = random.choice(HEADERS)
# webdriver.DesiredCapabilities.FIREFOX['firefox.page.settings.userAgent'] = random_header

FIRFOX_DRIVER_PATH = '/Users/afa/myFiles/tools/geckodriver'

proxy = '183.136.218.253'
proxy_port = 80         # 注意此处得是int类型，才有效

profile = webdriver.FirefoxProfile()
profile.set_preference('network.proxy.type', 1)  # 默认值0，就是直接连接；1就是手工配置代理。
profile.set_preference('network.proxy.http', proxy)
profile.set_preference('network.proxy.http_port', proxy_port)
profile.set_preference('network.proxy.ssl', proxy)
profile.set_preference('network.proxy.ssl_port', proxy_port)
profile.update_preferences()
driver = webdriver.Firefox(executable_path=FIRFOX_DRIVER_PATH, firefox_profile=profile)

driver.get('http://httpbin.org/ip')
print(driver.page_source)

driver.get('http://www.taobao.com')

# driver.quit()
