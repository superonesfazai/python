# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

import chrome_remote_interface
from chrome_remote_interface import (
    FailResponse,
)
from fzutils.spider.async_always import *

"""
截获chrome流量
[Chrome Debugging Protocol][官方]: https://chromedevtools.github.io/devtools-protocol/

运行: 
    1. $ google-chrome --headless --remote-debugging-port=9222
    2. $ python3 demo.py
"""

class callbacks:
    target_url = 'https://github.com'
    result = []

    async def start(tabs):
        await tabs.add()

    async def tab_start(tabs, tab):
        await tab.Page.enable()
        await tab.Network.enable()
        await tab.Page.navigate(url=callbacks.target_url)

    async def network__loading_finished(tabs,
                                        tab,
                                        requestId,
                                        loaderId,
                                        timestamp,
                                        type,
                                        response,
                                        **kwargs):
        """
        封装了Chrome Debugging Protocol接口Network.ResponseReceived函数，而此函数接受的参数，以及一些属性方法等都可以在该文档中查询。
        more response attribute: https://chromedevtools.github.io/devtools-protocol/tot/Network#type-Response
        :param tab:
        :param requestId:
        :param loaderId:
        :param timestamp:
        :param type:
        :param response:
        :param kwargs:
        :return:
        """
        # print(response.requestHeaders)
        # print(dir(response))
        try:
            packed = await tab.Network.get_response_body(requestId=requestId)
            body = tabs.helpers.old_helpers.unpack_response_body(packed=packed)

        except FailResponse as e:
            print('[Error] ', e)

        else:
            print(response.url, response.status, len(body))
            callbacks.result.append((response.url, response.status, len(body)))

    async def page__frame_stopped_loading(tabs, tab, **kwargs):
        print('[Info] finish')
        tabs.terminate()

    async def any(tabs, tab, callback_name, parameters):
        pass
        # print('Unknown event fired', callback_name)

if __name__ == '__main__':
    loop = get_event_loop()
    loop.run_until_complete(chrome_remote_interface.Tabs.run('localhost', 9222, callbacks))