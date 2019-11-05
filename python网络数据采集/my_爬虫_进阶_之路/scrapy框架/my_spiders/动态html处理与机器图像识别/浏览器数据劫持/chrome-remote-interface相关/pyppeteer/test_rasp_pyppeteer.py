# coding:utf-8

'''
@author = super_fazai
@File    : test_rasp_pyppeteer.py
@connect : superonesfazai@gmail.com
'''

"""
测试树莓派4b pyppeteer 环境(测试可用, 一定的失败率, 原因出自代理)
"""

from termcolor import colored
from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.fz_driver import PHONE
from fzutils.spider.chrome_remote_interface import *
from fzutils.spider.async_always import *

async def test():
    chromium_puppeteer = ChromiumPuppeteer(
        ip_pool_type=tri_ip_pool,
        headless=True,
        load_images=False,
        user_agent_type=PHONE,
        # 执行路径必须为系统安装的chromium-browser路径, 查看方式'where is chromium-browser'
        executable_path='/usr/bin/chromium-browser',
    )
    driver = await chromium_puppeteer.create_chromium_puppeteer_browser()
    page = await driver.newPage()
    await bypass_chrome_spiders_detection(page=page)

    target_url = 'https://httpbin.org/get'
    await goto_plus(
        page=page,
        url=target_url,
        options={
            'timeout': 1000 * 50,  # unit: ms
            'waitUntil': [  # 页面加载完成 or 不再有网络连接
                'domcontentloaded',
                'networkidle0',
            ]
        })
    body = Requests._wash_html(await page.content())
    print('[{:8s}] {}'.format(
        colored('body', 'red'),
        body, ))

    try:
        del chromium_puppeteer
        del page
    except:
        pass
    try:
        await driver.close()
    except:
        pass

loop = get_event_loop()
loop.run_until_complete(test())