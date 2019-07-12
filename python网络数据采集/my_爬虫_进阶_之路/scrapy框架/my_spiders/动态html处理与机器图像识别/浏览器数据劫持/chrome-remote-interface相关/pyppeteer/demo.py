# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

from termcolor import colored
from os import system
from websockets.exceptions import ConnectionClosed as WebsocketsConnectionClosed
from asyncio.futures import InvalidStateError

from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.fz_driver import (
    PHONE,
    PC,)
from fzutils.spider.chrome_remote_interface import ChromiumPuppeteer
from fzutils.spider.fz_requests import Requests
from fzutils.spider.pyppeteer_always import *
from fzutils.spider.async_always import *

LOAD_IMAGES = False

async def do_something(target_url: str):
    chromium_puppeteer = ChromiumPuppeteer(
        ip_pool_type=tri_ip_pool,
        headless=True,
        load_images=LOAD_IMAGES,
        user_agent_type=PHONE,)
    driver = await chromium_puppeteer.create_chromium_puppeteer_browser()
    # print('chromium version: {}'.format(await driver.version()))
    # print('初始user_agent: {}'.format(await driver.userAgent()))
    page = await driver.newPage()
    # 注意: 避免反爬检测window.navigator.webdriver为true, 认为非正常浏览器
    await page.evaluate("""
    () =>{
        Object.defineProperties(navigator, {
        webdriver:{
               get: () => false
            }
        })
    }
    """)

    # 测试发现此处修改无效!
    # await page.setUserAgent(userAgent=get_random_pc_ua())
    # await page.setUserAgent(userAgent=get_random_phone_ua())
    # print('更改后user_agent: {}'.format(await driver.userAgent()))

    # await page.setViewport({
    #     'width': 1080,
    #     'height': 960})

    # ** 截获 request 和 response, 劫持请求跟应答必须都设置!
    # ** puppeteer官网事件api: https://github.com/GoogleChrome/puppeteer/blob/master/docs/api.md
    # 搜索class: Page, 找到需求事件进行重写
    await page.setRequestInterception(True)
    page.on(event='request', f=intercept_request)
    page.on(event='response', f=intercept_response)
    # page.on(event='requestfinished', f=request_finished)

    # await page.setCookie({})

    res = False
    try:
        # await page.goto(
        #     url=target_url,
        #     options={
        #         'timeout': 1000 * 30,   # unit: ms
        #     })
        await goto_plus(
            page=page,
            url=target_url,
            options={
                'timeout': 1000 * 30,   # unit: ms
            })
        body = Requests._wash_html(await page.content())
        print('[{:8s}] {}'.format(
            colored('body', 'red'),
            body,))
        res = True if body != '' else res
        # await page.pdf({
        #     'path': 'screen.pdf',
        # })
        await page.screenshot({
            'path': 'screen.png',
        })

    except (WebsocketsConnectionClosed, InvalidStateError) as e:
        pass

    except Exception as e:
        print(e)

    try:
        del chromium_puppeteer
        del page
    except:
        pass
    try:
        await driver.close()
    except:
        pass

    # 结束删除proxy扩展
    # system('rm -rf ./extensions')

    return res

async def goto_plus(page: PyppeteerPage,
                    url: str,
                    options: dict,
                    num_retries: int=6,
                    sleep_time: (float, int)=2.):
    """
    goto_plus(增加请求成功率!)
    :param page:
    :param url:
    :param options:
    :param num_retries: 避免无限循环
    :param sleep_time: 合理的num_retries跟sleep_time能提高成功率!
    :return:
    """
    while True:
        try:
            await page.goto(
                url=url,
                options=options,)
            break
        except (PyppeteerNetworkError, PyppeteerPageError) as e:
            # 无网络 'net::ERR_INTERNET_DISCONNECTED','net::ERR_TUNNEL_CONNECTION_FAILED'
            if num_retries > 0:
                if 'net::' in str(e):
                    num_retries -= 1
                    await async_sleep(sleep_time)
                else:
                    raise e
            else:
                raise e

async def intercept_request(request: PyppeteerRequest):
    """
    截获request
    :param request:
    :return:
    """
    url = request.url
    headers = request.headers
    post_data = request.postData
    request_resource_type = request.resourceType

    print('[{:8s}] url: {}, post_data: {}'.format(
        'request',
        url,
        post_data,))

    # if request.resourceType in ['image', 'media', 'eventsource', 'websocket']:
    #     await request.abort()
    # else:
    #     await request.continue_()

    if not LOAD_IMAGES and request_resource_type in ['image', 'media']:
        await request.abort()
    else:
        # 放行请求
        await request.continue_()

async def intercept_response(response: PyppeteerResponse):
    """
    截获response
    :param response:
    :return:
    """
    response_status = response.status
    request = response.request
    request_url = request.url
    request_headers = request.headers
    request_method = request.method
    request_resource_type = request.resourceType
    post_data = request.postData

    print('[{:8s}] request_resource_type: {:10s}, request_method: {:6s}, response_status: {:5s}, request_url: {}'.format(
        'response',
        request_resource_type,
        request_method,
        str(response_status),
        request_url,))

    if request_resource_type in ['xhr', 'fetch', 'document', 'script', 'websocket']:
        try:
            body = await response.text()
            intercept_body = body[0:1500].replace('\n', '').replace('\t', '').replace('  ', '')
            print('[{:8s}] {}'.format(
                colored('@-data-@', 'green'),
                intercept_body))
        except (PyppeteerNetworkError, IndexError) as e:
            print('遇到错误:', e)

    else:
        pass

async def request_finished(request: PyppeteerRequest):
    """
    请求完成
    :param kwargs:
    :return:
    """
    pass

async def main():
    # target_url = 'https://www.github.com'
    target_url = 'https://httpbin.org/get'
    # 多多进宝
    # target_url = 'https://jinbao.pinduoduo.com/promotion/single-promotion'
    # target_url = 'https://music.163.com'
    # target_url = 'https://www.baidu.com'
    # target_url = 'https://m.yiuxiu.com'
    # target_url = 'https://www.taobao.com'
    # target_url = 'https://g.zhe800.com/xianshiqiang/index'
    # 书旗m站
    # target_url = 'http://t.shuqi.com/route.php?pagename=#!/ct/listBox/pageTitle/%E6%8E%92%E8%A1%8C/page_id/4/'
    # 斗鱼m站
    # target_url = 'https://m.douyu.com/3605965'

    concurrent_num = 50
    url_list = [target_url for num in range(concurrent_num)]

    tasks = []
    for url in url_list:
        tasks.append(loop.create_task(do_something(
            target_url=url,
        )))

    all_res = await async_wait_tasks_finished(tasks=tasks)
    # pprint(all_res)

    # 成功总数
    success_count = 0
    for item in all_res:
        if item:
            success_count += 1

    print('成功个数: {}, 成功概率: {:.3f}'.format(success_count, success_count/concurrent_num))

loop = get_event_loop()
loop.run_until_complete(main())