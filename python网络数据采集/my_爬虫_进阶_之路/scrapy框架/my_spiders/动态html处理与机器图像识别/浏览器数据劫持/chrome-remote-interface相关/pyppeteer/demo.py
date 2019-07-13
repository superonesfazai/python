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
from fzutils.spider.pyppeteer_always import *
from fzutils.spider.chrome_remote_interface import *
from fzutils.spider.async_always import *

HEADLESS = True
LOAD_IMAGES = False
USER_AGENT_TYPE = PHONE

async def do_something(target_url: str):
    chromium_puppeteer = ChromiumPuppeteer(
        ip_pool_type=tri_ip_pool,
        headless=HEADLESS,
        load_images=LOAD_IMAGES,
        user_agent_type=USER_AGENT_TYPE,)
    driver = await chromium_puppeteer.create_chromium_puppeteer_browser()
    # print('chromium version: {}'.format(await driver.version()))
    # print('初始user_agent: {}'.format(await driver.userAgent()))
    page = await driver.newPage()
    await bypass_chrome_spiders_detection(page=page)

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
    network_interceptor = NetworkInterceptorTest()
    page.on(event='request', f=network_interceptor.intercept_request)
    page.on(event='response', f=network_interceptor.intercept_response)
    page.on(event='requestfailed', f=network_interceptor.request_failed)
    # page.on(event='requestfinished', f=network_interceptor.request_finished)

    # await page.setCookie({})

    res = False
    try:
        # await page.goto(
        #     url=target_url,
        #     options={
        #         'timeout': 1000 * 30,   # unit: ms
        #     })
        # await page.waitForSelector(
        #     selector='css_xxxx',
        #     timeout=1000 * 30,)
        await goto_plus(
            page=page,
            url=target_url,
            options={
                'timeout': 1000 * 35,           # unit: ms
                'waitUntil': [                  # 页面加载完成 or 不再有网络连接
                    'domcontentloaded',
                    'networkidle0',
                ]
            })

        # 生成pdf
        # await page.pdf({
        #     'path': 'screen.pdf',
        # })

        # 全屏截图
        await page.screenshot({
            'path': 'screen.png',
            'type': 'png',
            'fullPage': True,
        })

        # 下滑至底部
        # await auto_scroll_to_bottom(page=page)

        # 目标元素定位截图
        # target_ele = await page.querySelector(selector='div.board')
        # await target_ele.screenshot({
        #     'path': 'target_ele.png',
        #     'type': 'png',
        # })

        # 如果网页内有用iframe等标签，这时page对象是无法读取<iframe>里面的内容的，需要用到下面
        # frames_list = page.frames
        # pprint(frames_list)

        body = Requests._wash_html(await page.content())
        print('[{:8s}] {}'.format(
            colored('body', 'red'),
            body,))
        res = True if body != '' else res

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

class NetworkInterceptorTest(NetworkInterceptor):
    def __init__(self):
        NetworkInterceptor.__init__(
            self,
            load_images=LOAD_IMAGES,)

async def auto_scroll_to_bottom(page: PyppeteerPage):
    """
    自动下滑至底部
    :param page:
    :return:
    """
    print('### auto_scroll start')
    await page.evaluate('''
    async () => {
        await new Promise((resolve, reject) => {
            // 页面的当前高度
            let totalHeight = 0;
            // 每次向下滚动的距离
            let distance = 100;
            // 通过setInterval循环执行
            let timer = setInterval(() => {
                let scrollHeight = document.body.scrollHeight;
                // 执行滚动操作
                window.scrollBy(0, distance);
        
                // 如果滚动的距离大于当前元素高度则停止执行
                totalHeight += distance;
                if (totalHeight >= scrollHeight) {
                    clearInterval(timer);
                    resolve();
                }
            }, 100);
        });
    }
    ''')
    print('### auto_scroll over')

    # 完成懒加载后可以完整截图或者爬取数据...
    # do what you like ...

async def main():
    global USER_AGENT_TYPE

    USER_AGENT_TYPE = PHONE
    # target_url = 'https://www.github.com'
    # target_url = 'https://httpbin.org/get'
    # 多多进宝
    # target_url = 'https://jinbao.pinduoduo.com/promotion/single-promotion'
    # target_url = 'https://music.163.com'
    # target_url = 'https://www.baidu.com'
    # target_url = 'https://m.yiuxiu.com'
    # target_url = 'https://www.taobao.com'
    # target_url = 'https://g.zhe800.com/xianshiqiang/index'
    # 书旗m站
    # target_url = 'http://t.shuqi.com'
    # 斗鱼m站
    # target_url = 'https://m.douyu.com/3605965'
    # 简书
    # target_url = 'https://www.jianshu.com/u/40909ea33e50'
    # target_url = 'https://www.jianshu.com'
    # 唯品会
    # m
    # target_url = 'https://m.vip.com/product-1710617992-6918185219909833864.html'
    # pc
    # target_url = 'https://detail.vip.com/detail-100170974-806750333981150.html?f=ad'
    # 马蜂窝
    target_url = 'https://m.mafengwo.cn/mtraffic/flightinter/list.html?departCity=%E5%8C%97%E4%BA%AC&departCode=BJS&destCity=%E6%9B%BC%E8%B0%B7&destCode=BKK&departDate=2019-07-21&destDate=&status=0&adult_nums=1&child_nums=0&baby_nums=0&followId=d17df66e43ce9f6bec3b4648f61f3394'

    concurrent_num = 3
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