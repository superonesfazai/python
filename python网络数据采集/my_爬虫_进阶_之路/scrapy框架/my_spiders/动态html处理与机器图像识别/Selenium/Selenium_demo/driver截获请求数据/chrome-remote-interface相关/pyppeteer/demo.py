# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

from pyppeteer.launcher import launch
from fzutils.spider.async_always import *

# chrome path
PYPPETEER_CHROMIUM_DRIVER_PATH = ''

async def main():
    browser = await launch({
        'headless': False,
        'executablePath': PYPPETEER_CHROMIUM_DRIVER_PATH,
        'autoClose': True,
    })
    page = await browser.newPage()
    target_url = 'https://www.github.com'
    await page.goto(url=target_url)
    await page.screenshot({
        'path': 'example.png'
    })
    await browser.close()

loop = get_event_loop()
loop.run_until_complete(main())