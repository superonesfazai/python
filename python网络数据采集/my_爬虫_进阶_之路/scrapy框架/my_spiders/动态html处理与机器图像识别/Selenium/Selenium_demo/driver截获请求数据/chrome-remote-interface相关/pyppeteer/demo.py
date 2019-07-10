# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

from pyppeteer.launcher import launch
from fzutils.spider.async_always import *

# chrome path
PYPPETEER_CHROMIUM_DRIVER_PATH = '/Users/afa/myFiles/tools/pyppeteer_driver/mac/chrome-mac/Chromium.app'

async def main():
    browser = await launch({
        'headless': False,
        'devtools': False,
        'executablePath': PYPPETEER_CHROMIUM_DRIVER_PATH,
        # 可选args: https://peter.sh/experiments/chromium-command-line-switches/
        'args': [
            '--disable-extensions',
            '--hide-scrollbars',
            '--disable-bundled-ppapi-flash',
            '--mute-audio',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
        ],
        'autoClose': True,
        # 'dumpio': True,
    })
    page = await browser.newPage()
    await page.setUserAgent(get_random_pc_ua())
    # await page.setViewport({
    #     'width': 1080,
    #     'height': 960})
    target_url = 'https://www.github.com'
    await page.goto(url=target_url)
    await page.screenshot({
        'path': 'test.png'
    })
    await browser.close()

loop = get_event_loop()
loop.run_until_complete(main())