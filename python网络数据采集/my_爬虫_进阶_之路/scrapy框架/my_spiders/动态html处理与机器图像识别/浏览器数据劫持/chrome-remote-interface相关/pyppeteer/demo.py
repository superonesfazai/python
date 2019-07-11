# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

from os import system
from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.fz_driver import (
    ChromiumPuppeteer,
    PHONE,
    PC,)
from fzutils.spider.pyppeteer_always import *
from fzutils.spider.async_always import *

async def main():
    chromium_puppeteer = ChromiumPuppeteer(
        ip_pool_type=tri_ip_pool,
        headless=False,
        user_agent_type=PC,
    )
    driver = await chromium_puppeteer.create_chromium_puppeteer_browser()
    print('chromium  version: {}'.format(await driver.version()))
    print('初始user_agent: {}'.format(await driver.userAgent()))
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
    # await page.evaluate("""
    # () =>{
    #     Object.defineProperties(navigator, {
    #     webdriver:{
    #            get: () => false
    #         }
    #     })
    # }
    # """)

    # 测试发现此处修改无效!
    # await page.setUserAgent(userAgent=get_random_pc_ua())
    # await page.setUserAgent(userAgent=get_random_phone_ua())
    # print('更改后user_agent: {}'.format(await driver.userAgent()))

    # await page.setViewport({
    #     'width': 1080,
    #     'height': 960})

    # ** 截获 request 和 response, 劫持请求跟应答必须都设置!
    await page.setRequestInterception(True)
    page.on(event='request', f=puppeteer_intercept_request)
    page.on(event='response', f=puppeteer_intercept_response)

    # target_url = 'https://www.github.com'
    # target_url = 'https://httpbin.org/get'
    # 多多进宝
    # target_url = 'https://jinbao.pinduoduo.com/promotion/single-promotion'
    # target_url = 'https://music.163.com'
    # target_url = 'https://www.baidu.com'
    # target_url = 'https://www.taobao.com'
    target_url = 'https://stackoverflow.com/questions/51629151/puppeteer-protocol-error-page-navigate-target-closed'

    try:
        await page.goto(
            url=target_url,
            options={
                'timeout': 1000 * 80,   # unit: ms
            })
        await page.screenshot({
            'path': 'screen.png'
        })
        await driver.close()
    except Exception as e:
        print(e)

    # 结束删除proxy扩展
    system('rm -rf ./extensions')

    return

async def puppeteer_intercept_request(request: PyppeteerRequest, **kwargs):
    """
    请求过滤
    :param request:
    :return:
    """
    # pprint(kwargs)
    url = request.url
    headers = request.headers
    post_data = request.postData

    print('[{:8s}] url: {}, post_data: {}'.format(
        'request',
        url,
        post_data,
    ))

    # if request.resourceType in ['image', 'media', 'eventsource', 'websocket']:
    #     await request.abort()
    # else:
    #     await request.continue_()

    await request.continue_()

async def puppeteer_intercept_response(response: PyppeteerResponse, **kwargs):
    # pprint(kwargs)
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
        try:
            body = await response.text()
            print(body[0:600].replace('\n', '').replace('\t', ''))
        except (PyppeteerNetworkError, IndexError) as e:
            print('遇到错误:', e)

loop = get_event_loop()
loop.run_until_complete(main())