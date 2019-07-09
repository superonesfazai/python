# chrome-remote-interface-python
[Chrome调试协议](https://chromedevtools.github.io/devtools-protocol/)界面，通过使用简单的Python API提供命令和通知的简单抽象，有助于检测Chrome（或任何其他合适的实现）。

## 适用
python >= 3.5

## install
```shell
$ git clone https://github.com/wasiher/chrome-remote-interface-python.git
$ python3 setup.py install
```

## simple use

加载https://github.com并打印每个响应主体长度
```python
import chrome_remote_interface
from fzutils.spider.async_always import *

def test():
    class callbacks:
        async def start(tabs):
            await tabs.add()
        async def tab_start(tabs, tab):
            await tab.Page.enable()
            await tab.Network.enable()
            await tab.Page.navigate(url='http://github.com')
        async def network__loading_finished(tabs, tab, requestId, **kwargs):
            try:
                body = tabs.helpers.old_helpers.unpack_response_body(await tab.Network.get_response_body(requestId=requestId))
                print('body length:', len(body))
            except tabs.FailResponse as e:
                print('fail:', e)
        async def page__frame_stopped_loading(tabs, tab, **kwargs):
            print('finish')
            tabs.terminate()
        async def any(tabs, tab, callback_name, parameters):
            pass
            # print('Unknown event fired', callback_name)
    
    loop = get_event_loop()
    loop.run_until_complete(chrome_remote_interface.Tabs.run('localhost', 9222, callbacks))

if __name__ == '__main__':
    test()
```

我们使用这些类型的回调：
- start(tabs) - 开始时开除。
- tab_start(tabs, tab, manual) - 在tab创建时触发。
- network__response_received(tabs, tab, **kwargs)- 回调chrome Network.responseReceived事件。
- any(tabs, tab, callback_name, parameters) - 没有发现回调时触发的后备。
- tab_close(tabs, tab) - 选项卡关闭时触发
- tab_suicide(tabs, tab) - 没有你希望关闭标签时触发（也是套接字）
- close(tabs) - 关闭所有标签时触发

我们可以使用方法添加标签tabs.add()，并用tabs[n].remove()或删除它tab.remove()。

FailReponse当出现问题时，每种方法都可以抛出异常。

您可以通过致电终止您的程序tabs.terminate()。

