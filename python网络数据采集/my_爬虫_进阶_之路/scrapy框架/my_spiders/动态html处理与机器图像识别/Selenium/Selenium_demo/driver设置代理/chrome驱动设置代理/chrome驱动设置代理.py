# coding:utf-8

'''
@author = super_fazai
@File    : chrome驱动设置代理.py
@connect : superonesfazai@gmail.com
'''

"""
测试通过, 注意使用代理偶尔获取不到淘宝html
"""

from selenium import webdriver
from fzutils.ip_pools import MyIpPools

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=http://183.136.218.253:80')
chrome_options.add_argument('--headless')     # 注意: 设置headless无法访问网页
chrome_options.add_argument('--disable-gpu')

# 设置无图模式
prefs = {
    'profile.managed_default_content_settings.images': 2
}
chrome_options.add_experimental_option("prefs", prefs)

'''无法打开https解决方案'''
# 配置忽略ssl错误
capabilities = webdriver.DesiredCapabilities.CHROME.copy()
capabilities['acceptSslCerts'] = True
capabilities['acceptInsecureCerts'] = True

# 方法1: 设置代理
ip_object = MyIpPools()
proxy_ip = ip_object._get_random_proxy_ip().replace('http://', '') if isinstance(ip_object._get_random_proxy_ip(), str) else ''
if proxy_ip != '':
    chrome_options.add_argument('--proxy-server={0}'.format(proxy_ip))

# 方法2:
# ip_object = MyIpPools()
# proxy_ip = ip_object._get_random_proxy_ip().replace('http://', '') if isinstance(ip_object._get_random_proxy_ip(), str) else ''
# # Change the proxy properties of that copy.
# capabilities['proxy'] = {
#     "httpProxy": proxy_ip,
#     "ftpProxy": proxy_ip,
#     "sslProxy": proxy_ip,
#     "noProxy": None,
#     "proxyType": "MANUAL",
#     "class": "org.openqa.selenium.Proxy",
#     "autodetect": False,
# }

CHROME_DRIVER_PATH = '/Users/afa/myFiles/tools/chromedriver'

driver = webdriver.Chrome(
    executable_path=CHROME_DRIVER_PATH,
    chrome_options=chrome_options,
    desired_capabilities=capabilities
)
print('chrome驱动已启动...')
# driver.get('http://httpbin.org/ip')
driver.get('https://www.taobao.com')
# driver.get('https://www.baidu.com')
print(driver.page_source)

driver.quit()
