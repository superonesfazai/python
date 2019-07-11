# Pyppeteer(推荐使用)
非官方Python端口的 [puppeteer](https://github.com/GoogleChrome/puppeteer) JavaScript（无头）chrome / chromium浏览器自动化库。

[doc](https://miyakogi.github.io/pyppeteer/reference.html)

## DevTools Protocol
与无头浏览器交互的协议，可以直接使用websocket与开启的chrome进行通信。 所有的控制指令都以json通信

## 版本控制
python 3.6+（实验支持python 3.5）

## 安装
```shell
$ pip3 install pyppeteer
```

## puppeteer和pyppeteer
鉴于使用Chrome DevTools Protocol非常违反用户操作浏览器的习惯，便有了各种封装好的API。 puppeteer便是Google团队官方提供的API工具，它的特点是：像用户一样操作浏览器。 例如，我们想进行一次搜索功能，习惯是打开一个浏览器，选择一个页面，输入网址并回车，点击其中一个搜索结果，截图并保存，最后关闭浏览器。 这在puppeteer中

官方提供的puppeteer是nodejs模块，如果要在python中使用，可以使用pyppeteer。 pyppeteer是puppeteer的python移植版，其作者力求更上puppeteer的所有更新，但是自己不会增加新的特性。 要使用pyppeteer也可以直接翻阅puppeteer的api文档，几乎所有的方法和参数都完全一致。 

```python
import asyncio
from pyppeteer import launch

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('http://example.com')
    await page.click("button");
    await page.screenshot({'path': 'example.png'})
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
```

执行js脚本
```python
import asyncio
from pyppeteer import launch

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('http://example.com')
    await page.screenshot({'path': 'example.png'})

    dimensions = await page.evaluate('''() => {
        return {
            width: document.documentElement.clientWidth,
            height: document.documentElement.clientHeight,
            deviceScaleFactor: window.devicePixelRatio,
        }
    }''')

    print(dimensions)
    # >>> {'width': 800, 'height': 600, 'deviceScaleFactor': 1}
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
```

## puppeteer脚本自动生成
chrome安装扩展puppeteer recorder

[github](https://github.com/checkly/puppeteer-recorder)