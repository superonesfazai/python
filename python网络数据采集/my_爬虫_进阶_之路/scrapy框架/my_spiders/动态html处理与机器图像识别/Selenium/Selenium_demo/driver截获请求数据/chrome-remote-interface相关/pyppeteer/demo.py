# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

from gc import collect
from pyppeteer.launcher import launch as chromium_launch
from pyppeteer.network_manager import Request as PyppeteerRequest
from pyppeteer.network_manager import Response as PyppeteerResponse
from fzutils.spider.fz_driver import (
    PC,
    PHONE,)
from fzutils.ip_pools import tri_ip_pool
from fzutils.common_utils import _print
from fzutils.spider.async_always import *

# chromium path
PYPPETEER_CHROMIUM_DRIVER_PATH = '/Users/afa/myFiles/tools/pyppeteer_driver/mac/chrome-mac/Chromium.app/Contents/MacOS/Chromium'

async def main():
    chromium_puppeteer = ChromiumPuppeteer()
    driver = await chromium_puppeteer.init_puppeteer()
    page = await driver.newPage()
    # 注意: 避免反爬检测window.navigator.webdriver为true, 认为非正常浏览器
    # await page.evaluate("""
    #     () =>{
    #         Object.defineProperties(navigator,{
    #             webdriver:{
    #             get: () => false
    #             }
    #         })
    #     }
    # """)
    await page.setUserAgent(get_random_pc_ua())
    # await page.setViewport({
    #     'width': 1080,
    #     'height': 960})
    # 截获 request 和 response
    await page.setRequestInterception(True)
    page.on(
        event='request',
        f=intercept_request)
    page.on(
        event='response',
        f=intercept_response)

    # target_url = 'https://www.github.com'
    target_url = 'https://httpbin.org/get'

    try:
        await page.goto(
            url=target_url,
            # timeout=25,
        )
        await page.screenshot({
            'path': 'screen.png'
        })
        await driver.close()
    except Exception as e:
        print(e)

PYPPETEER = 0

class ChromiumPuppeteer(object):
    """
    chromium 操作者
    """
    def __init__(self,
                 type=PYPPETEER,
                 load_images=False,
                 executable_path=PYPPETEER_CHROMIUM_DRIVER_PATH,
                 high_conceal=True,
                 logger=None,
                 headless=False,
                 driver_use_proxy=True,
                 user_agent_type=PC,
                 driver_obj=None,
                 ip_pool_type=tri_ip_pool,
                 driver_cookies=None,
                 driver_auto_close=True,
                 driver_dumpio=True,
                 driver_devtools=False,):
        super(ChromiumPuppeteer, self).__init__()
        self.type = type
        self.executable_path = executable_path
        self.high_conceal = high_conceal
        self.load_images = load_images
        self.headless = headless
        self.driver_use_proxy = driver_use_proxy
        self.lg = logger
        self.user_agent_type = user_agent_type
        self.ip_pool_type = ip_pool_type
        self._cookies = driver_cookies
        self.driver_auto_close = driver_auto_close
        # 把无头浏览器进程的 stderr 核 stdout pip 到主程序，也就是设置为 True 的话，chromium console 的输出就会在主程序中被打印出来
        self.driver_dumpio = driver_dumpio
        self.driver_devtools = driver_devtools
        self.driver = None
        # if driver_obj is None:
        #     self._set_driver()
        # else:
        #     self.driver = driver_obj

    async def init_puppeteer(self,):
        # 设置代理
        proxy_ip = ''
        if self.driver_use_proxy:
            proxy_ip = self._get_random_proxy_ip()
            assert proxy_ip != '', '给chrome设置代理失败, 异常抛出!'
            # print(proxy_ip)

        # TODO chrome设置代理进行请求成功率较低
        driver_args = [
            '--disable-extensions',
            '--hide-scrollbars',
            '--disable-bundled-ppapi-flash',
            '--mute-audio',
            '--no-sandbox',
            # 取消提示: chrome正在受自动软件控制
            '--disable-infobars',
            '--disable-setuid-sandbox',
            '--disable-gpu',
            '--proxy-server=http://{0}'.format(proxy_ip) if proxy_ip != '' else '',
        ]
        self.driver = await chromium_launch({
            'headless': self.headless,
            'devtools': self.driver_devtools,
            'executablePath': self.executable_path,
            # 可选args: https://peter.sh/experiments/chromium-command-line-switches/
            'args': driver_args,
            'autoClose': self.driver_auto_close,
            'dumpio': self.driver_dumpio,
        })

        return self.driver

    def _get_random_proxy_ip(self) -> str:
        '''
        得到一个随机代理
        :return: 格式: ip:port or ''
        '''
        ip_object = MyIpPools(type=self.ip_pool_type, high_conceal=self.high_conceal)
        _ = ip_object._get_random_proxy_ip()
        proxy_ip = re.compile(r'https://|http://').sub('', _) if isinstance(_, str) else ''

        return proxy_ip

    def _get_driver(self):
        '''
        得到driver对象
        :return:
        '''
        return self.driver

    def __del__(self):
        try:
            del self.lg
        except:
            pass
        try:
            self.driver
        except:
            pass
        collect()

async def intercept_request(request: PyppeteerRequest):
    """
    请求过滤
    :param request:
    :return:
    """
    url = request.url
    headers = request.headers
    post_data = request.postData

    print('[{:8s}] url: {}, post_data: {}'.format(
        'request',
        url,
        post_data,
    ))

    if request.resourceType in ['image', 'media', 'eventsource', 'websocket']:
        await request.abort()
    else:
        await request.continue_()

async def intercept_response(response: PyppeteerResponse):
    response_status = response.status
    response_request = response.request
    request_url = response_request.url
    request_resource_type = response_request.resourceType
    print('[{:8s}] request_resource_type: {:10s}, request_url: {}'.format(
        'response',
        request_resource_type,
        request_url,))

    if request_resource_type in ['xhr', 'fetch', 'document']:
        # 只打印xhr, fetch的内容
        body = await response.text()
        print(body)

loop = get_event_loop()
loop.run_until_complete(main())