# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

"""
[Chrome DevTools Protocol][官方]: https://chromedevtools.github.io/devtools-protocol/

检测chrome 服务是否打开: http://localhost:9222/json

运行: 
    有页面chrome
    1. $ cd /Applications/Google Chrome.app/Contents/MacOS
    2. $ ./Google\ Chrome --remote-debugging-port=9222
    
    headless chrome
    1. $ ./chromedriver --headless --disable-gpu --remote-debugging-port=9222
    
    docker
    1. $ docker run -it --rm --name fate0-chrome --cap-add=SYS_ADMIN -p 9222:9222 fate0/headless-chrome
"""

import pychrome
from pychrome.tab import Tab as PyChromeTab
from pychrome.exceptions import CallMethodException as PyChromeCallMethodException
from threading import Lock as ThreadingLock
from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.async_always import *

class ChromeEventHandler(object):
    pdf_lock = ThreadingLock()

    def __init__(self, browser, tab):
        self.browser = browser
        self.tab = tab
        self.start_frame = None
        self.ip_pool_type = tri_ip_pool

    def frame_started_loading(self, frameId):
        if not self.start_frame:
            self.start_frame = frameId
        else:
            pass

    def frame_stopped_loading(self, frameId):
        if self.start_frame == frameId:
            self.tab.Page.stopLoading()
            result = self.tab.Runtime.evaluate(expression="document.documentElement.outerHTML")
            pprint(result)
            self.html_content = result.get('result', {}).get('value', "")
            print(self.html_content)
            self.tab.stop()
        else:
            pass

    def request_will_be_sent(self, **kwargs):
        """
        request register callback
        :param kwargs:
        :return:
        """
        # pprint(kwargs)
        _request = kwargs.get('request', {})
        request_id = kwargs.get('requestId', '')
        request_url = _request.get('url', '')
        has_post_data = _request.get('hasPostData', False)
        request_headers = _request.get('headers', {})
        post_data = _request.get('postData', None)

        # 处理待post data的请求[无法正常post的请求]
        # if has_post_data:
        #     if 'crawlerInfo' in post_data:
        #         print('发现目标接口...')
        #         pprint(kwargs)
        #         pprint(request_headers)
        #         print(post_data)
        #         body = Requests.get_url_body(
        #             method='post',
        #             url=request_url,
        #             headers=request_headers,
        #             params=None,
        #             data=post_data,
        #             ip_pool_type=self.ip_pool_type,)
        #         print(body)

        print("[{:8s}] loading: {}".format(
            'request',
            request_url))

        return

    def request_intercepted(self, **kwargs):
        """
        请求修改
        :param kwargs:
        :return:
        """
        # pprint(kwargs)
        self.tab.Network.continueInterceptedRequest(
            **kwargs)

        return

    def response_received(self,
                          img_pass=True,
                          font_pass=True,
                          js_pass=True,
                          stylesheet_pass=True,
                          **kwargs):
        """
        应答回调
        :param kwargs:
        :return:
        """
        # pprint(kwargs)
        loader_id = kwargs.get('loaderId', '')
        request_id = kwargs.get('requestId', '')
        response_type = kwargs.get('type', '')
        response = kwargs.get('response', {})
        response_status = response.get('status', '')
        response_headers_text = response.get('headersText')
        request_url = response.get('url', '')
        print('[received] request_url: {}'.format(request_url))
        # pprint(response)
        # print("[received] response status: {}".format(response_status))
        # print('[received] response headers_text: {}'.format(response_headers_text))

        # 跳过不处理的文件类型
        if (img_pass and response_type == 'Image')\
                or (font_pass and response_type == 'Font')\
                or (js_pass and response_type == 'Script' and re.compile('\.js').findall(request_url) != [])\
                or (stylesheet_pass and response_type == 'Stylesheet'):

            return

        print("[received] response type: {}, python_type: {}".format(
            response_type,
            type(response_type)))

        # 处理response data
        try:
            # dict类型
            res = self.tab.Network.getResponseBody(requestId=request_id)
            # pprint(res)
            # base64_encoded bool类型
            base64_encoded, body = res['base64Encoded'], res['body']
            if base64_encoded:
                body = b64decode_plus(data=body.encode())
            else:
                pass
            print(body)

        except PyChromeCallMethodException as e:
            print(e)

        except Exception as e:
            print(e)

        return

    def get_all_cookies(self):
        """
        获取cookies
        :param tab:
        :return:
        """
        cookies_list = self.tab.Network.getAllCookies()

        return cookies_list

    def get_current_page_cookies(self):
        """
        获取当前页面的cookies
        :param tab:
        :return:
        """
        cookies_list = self.tab.Network.getCookies()

        return cookies_list

    def browser_screenshot(self):
        """
        屏幕截图
        :param tab:
        :return:
        """
        screen_base64 = self.tab.call_method("Page.captureScreenshot")
        image_data = screen_base64.get('data', '')
        # print(image_data)
        with open("test.png", 'wb') as f:
            f.write(image_data.decode('base64'))

        return

    def loading_finished(self, **kwargs):
        """
        http 加载结束回调
        :param kwargs:
        :return:
        """
        print("[loading finished]")

def close_all_tabs(browser):
    """
    关闭browser所有标签页
    :param browser:
    :return:
    """
    if len(browser.list_tab()) == 0:
        return
    for tab in browser.list_tab():
        try:
            tab.stop()
        except pychrome.RuntimeException:
            pass

        browser.close_tab(tab)

    try:
        assert len(browser.list_tab()) == 0
    except AssertionError:
        print('browser 原先的tabs都已关闭!')

def get_html(browser, url):
    """
    获取网页html
    :param browser:
    :param url:
    :return:
    """
    tab = browser.new_tab()
    tab.start()
    tab.call_method('Page.navigate', url=url, _timeout=5)
    tab.wait(10)
    html = tab.Runtime.evaluate(expression="document.documentElement.outerHTML")
    tab.stop()
    browser.close_tab(tab)

    return html['result']['value']

def perform_click(browser):
    """
    模拟操作
    :param browser:
    :return:
    """
    tab = browser.new_tab()

    # def loading_finished(**kwargs):
    #     print "[loading finished]"
    #
    # # when HTTP request has finished loading
    # tab.set_listener("Network.loadingFinished", loading_finished)

    tab.start()

    # call method
    # tab.Network.enable()
    tab.Network.enable()
    tab.Page.enable()
    tab.Runtime.enable()

    def dom_content_event_fired(**kwargs):
        print("[content] dom content event fired")
        tab.DOM.enable()
        root = tab.DOM.getDocument()
        root_node_id = root.get('root', {}).get('nodeId', '')
        # 找到输入框
        input_box = tab.DOM.querySelector(nodeId=root_node_id, selector='#kw')
        # tab.DOM.setNodeValue(nodeId=input_box, value='hello')
        tab.Runtime.evaluate(expression='document.getElementById("kw").value="Chrome"', )
        # 找到搜索按钮
        search_btn = tab.DOM.querySelector(nodeId=root_node_id, selector='#su')
        remote_node = tab.DOM.resolveNode(nodeId=search_btn.get('nodeId', ''))
        # 执行点击
        tab.Runtime.callFunctionOn(functionDeclaration='(function() { this.click(); })',
                                   objectId=remote_node.get('object', {}).get('objectId', {}))
        tab.wait(3)
        # 输出结果
        html = tab.Runtime.evaluate(expression="document.documentElement.outerHTML")
        body = html.get('result', {}).get('value', '').encode('utf-8')

        screen_base64 = tab.call_method("Page.captureScreenshot")
        image_data = screen_base64.get('data', '')
        with open("test.png", 'wb') as f:
            f.write(image_data.decode('base64'))

        # tab.DOM.performSearch(query='xpath', includeUserAgentShadowDOM=True)
        # stop the tab (stop handle events and stop recv message from chrome)
        tab.stop()

        # close tab
        browser.close_tab(tab)

    tab.set_listener(
        event="Page.domContentEventFired",
        callback=dom_content_event_fired)

    # 刷新当前页面，ignoreCache 是否忽略cache，如果为 true，则强行刷新，类似于 Shift+refresh
    # tab.call_method("Page.reload", ignoreCache=False)
    tab.call_method("Page.navigate", url='https://www.baidu.com', _timeout=5)
    tab.wait(20)

    return

def main():
    browser = pychrome.Browser(url="http://127.0.0.1:9222")
    close_all_tabs(browser)
    print(browser.version())

    # create a tab
    tab: PyChromeTab = browser.new_tab()
    event_handler = ChromeEventHandler(browser, tab)
    # TODO 设置监听(只能监听事件Events, 不是methods)
    # when HTTP request has finished loading
    # tab.set_listener(
    #     event="Network.loadingFinished",
    #     callback=loading_finished)
    # tab.set_listener(
    #     event='Page.frameStartedLoading',
    #     callback=event_handler.frame_started_loading)
    # tab.set_listener(
    #     event='Page.frameStoppedLoading',
    #     callback=event_handler.frame_stopped_loading,)
    # tab.set_listener(
    #     event='Network.requestIntercepted',
    #     callback=event_handler.request_intercepted,)
    tab.set_listener(
        event="Network.requestWillBeSent",
        callback=event_handler.request_will_be_sent)
    tab.set_listener(
        event="Network.responseReceived",
        callback=event_handler.response_received)

    # start the tab
    tab.start()
    # call method
    tab.call_method(_method="Network.enable")

    # target_url = 'https://m.baidu.com'
    # 多多进宝
    # target_url = 'https://jinbao.pinduoduo.com/promotion/single-promotion'
    # 淘抢购
    # target_url = 'https://qiang.taobao.com'
    # 网易云音乐
    target_url = 'https://music.163.com/m/'

    # call method with timeout
    tab.call_method(
        _method="Page.navigate",
        url=target_url,
        _timeout=8)

    tab.wait(8)
    # 停止处理事件跟接收信息
    tab.stop()
    browser.close_tab(tab)

if __name__ == '__main__':
    main()