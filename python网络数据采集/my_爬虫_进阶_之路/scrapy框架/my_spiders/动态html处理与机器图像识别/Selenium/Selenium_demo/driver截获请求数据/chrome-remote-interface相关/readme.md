# chrome-remote-interface
Chrome调试协议界面，通过使用简单的JavaScript API提供命令和通知的简单抽象，有助于检测Chrome（或任何其他合适的实现）。

[github](https://github.com/cyrus-and/chrome-remote-interface)

## 安装
```shell
$ npm install chrome-remote-interface
```

## 使用
Chrome本身或其他实现的实例需要在已知端口上运行才能使用此模块（默认为 localhost:9222）。

### 桌面版
```shell
$ google-chrome --remote-debugging-port=9222
```

### headless
```shell
$ google-chrome --headless --remote-debugging-port=9222
```

## 捆绑的客户端
此模块附带一个捆绑的客户端应用程序，可用于交互式控制远程实例。

### 目标管理
eg:
```shell
$ chrome-remote-interface new 'http://example.com'
{
    "description": "",
    "devtoolsFrontendUrl": "/devtools/inspector.html?ws=localhost:9222/devtools/page/b049bb56-de7d-424c-a331-6ae44cf7ae01",
    "id": "b049bb56-de7d-424c-a331-6ae44cf7ae01",
    "thumbnailUrl": "/thumb/b049bb56-de7d-424c-a331-6ae44cf7ae01",
    "title": "",
    "type": "page",
    "url": "http://example.com/",
    "webSocketDebuggerUrl": "ws://localhost:9222/devtools/page/b049bb56-de7d-424c-a331-6ae44cf7ae01"
}
$ chrome-remote-interface close 'b049bb56-de7d-424c-a331-6ae44cf7ae01'
```

### 检查
使用inspect子命令可以以REPL方式执行[命令执行](https://github.com/cyrus-and/chrome-remote-interface#clientdomainmethodparams-callback) 和[事件绑定](https://github.com/cyrus-and/chrome-remote-interface#clientdomaineventcallback)。但是与常规API不同，事件永远不会返回承诺，如果省略回调，则提供允许切换处理程序的默认实现。

请记住REPL接口提供完成。

eg:
```shell
$ chrome-remote-interface inspect
>>> Runtime.evaluate({expression: 'window.location.toString()'})
...
{ result: { type: 'string', value: 'about:blank' } }
>>> Page.enable()
...
{}
>>> Page.loadEventFired() // registered
{ 'Page.loadEventFired': true }
>>> Page.loadEventFired() // unregistered
{ 'Page.loadEventFired': false }
>>> Page.loadEventFired() // registered
{ 'Page.loadEventFired': true }
>>> Page.navigate({url: 'https://github.com'})
...
{ frameId: '15174.1' }
{ 'Page.loadEventFired': { timestamp: 46427.780513 } }
>>> Runtime.evaluate({expression: 'window.location.toString()'})
...
{ result: { type: 'string', value: 'https://github.com/' } }
```

## 嵌入式文档
在REPL和常规API中，协议的每个对象都 使用描述符中的元信息进行修饰。此外， category还添加了字段，用于确定成员是a command，a event还是a type。

```shell
>>> Page.navigate
{ [Function]
  category: 'command',
  parameters: { url: { type: 'string', description: 'URL to navigate the page to.' } },
  returns:
   [ { name: 'frameId',
       '$ref': 'FrameId',
       hidden: true,
       description: 'Frame id that will be navigated.' } ],
  description: 'Navigates current page to the given URL.',
  handlers: [ 'browser', 'renderer' ] }
```

```shell
>>> Network.requestWillBeSent
{ [Function]
  category: 'event',
  description: 'Fired when page is about to send HTTP request.',
  parameters:
   { requestId: { '$ref': 'RequestId', description: 'Request identifier.' },
     frameId:
      { '$ref': 'Page.FrameId',
        description: 'Frame identifier.',
        hidden: true },
     loaderId: { '$ref': 'LoaderId', description: 'Loader identifier.' },
     documentURL:
      { type: 'string',
        description: 'URL of the document this request is loaded for.' },
     request: { '$ref': 'Request', description: 'Request data.' },
     timestamp: { '$ref': 'Timestamp', description: 'Timestamp.' },
     wallTime:
      { '$ref': 'Timestamp',
        hidden: true,
        description: 'UTC Timestamp.' },
     initiator: { '$ref': 'Initiator', description: 'Request initiator.' },
     redirectResponse:
      { optional: true,
        '$ref': 'Response',
        description: 'Redirect response data.' },
     type:
      { '$ref': 'Page.ResourceType',
        optional: true,
        hidden: true,
        description: 'Type of this resource.' } } }
```

```shell
>>> Network.Request
{ category: 'type',
  id: 'Request',
  type: 'object',
  description: 'HTTP request data.',
  properties:
   { url: { type: 'string', description: 'Request URL.' },
     method: { type: 'string', description: 'HTTP request method.' },
     headers: { '$ref': 'Headers', description: 'HTTP request headers.' },
     postData:
      { type: 'string',
        optional: true,
        description: 'HTTP POST request data.' },
     mixedContentType:
      { optional: true,
        type: 'string',
        enum: [Object],
        description: 'The mixed content status of the request, as defined in http://www.w3.org/TR/mixed-content/' },
     initialPriority:
      { '$ref': 'ResourcePriority',
        description: 'Priority of the resource request at the time request is sent.' } } }
```

## Chrome调试协议版本
默认情况下chrome-remote-interface 要求远程实例提供自己的协议。

这种行为可以通过设置来改变local选项true 时[连接](https://github.com/cyrus-and/chrome-remote-interface#cdpoptions-callback)，在这种情况下，[本地版本](https://github.com/cyrus-and/chrome-remote-interface/blob/master/lib/protocol.json)使用的协议的描述符的。此文件会不时使用scripts/update-protocol.sh并手动更新并推送到此存储库。

为了进一步覆盖上述行为，基本上有两种选择：

- 在通过自定义协议的描述符[的连接](https://github.com/cyrus-and/chrome-remote-interface#cdpoptions-callback) （protocol可选）;
- 使用[命令](https://github.com/cyrus-and/chrome-remote-interface#clientsendmethod-params-callback) 和[事件](https://github.com/cyrus-and/chrome-remote-interface#event-domainmethod)接口的原始版本来使用未出现在协议描述符的本地版本中的前沿功能;