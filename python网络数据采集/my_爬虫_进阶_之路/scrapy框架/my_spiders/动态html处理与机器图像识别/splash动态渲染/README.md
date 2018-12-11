# splash
splash是一个JavaScript渲染服务，是一个带有HTTP API的轻量级浏览器，同时它对接了Python中的Twisted和QT库。利用它，我们同样可以实现动态渲染页面的抓取。

[doc](https://splash.readthedocs.io/en/stable/)

[github](https://github.com/scrapinghub/splash)

## 功能介绍
利用splash，我们可以实现如下功能：

- 异步方式处理多个网页渲染过程；
- 获取渲染后的页面的源代码或截图；
- 通过关闭图片渲染或者使用Adblock规则来加快页面渲染速度；
- 可执行特定的JavaScript脚本；
- 可通过Lua脚本来控制页面渲染过程；
- 获取渲染的详细过程并通过HAR（HTTP Archive）格式呈现。

## 准备工作
先确保正确安装splash并可以正常进行服务

### 安装splash
[ubuntu官方安装docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/#set-up-the-repository)
```
$ sudo docker pull scrapinghub/splash:latest
```

### 运行splash
```bash
$ sudo docker run -p 8050:8050 scrapinghub/splash
$ open http://localhost:8050
```

## 使用
通过HAR的结果可以看到，Splash执行了整个网页的渲染过程，包括CSS、JavaScript的加载等过程，呈现的页面和我们在浏览器中得到的结果完全一致。

那么，这个过程由什么来控制呢？重新返回首页，可以看到实际上是有一段脚本，内容如下：
```lua
# 是用Lua语言写的脚本
function main(splash, args)
  assert(splash:go(args.url))
  assert(splash:wait(0.5))
  return {
    html = splash:html(),
    png = splash:png(),
    har = splash:har(),
  }
end
```
到这里，我们大体了解了Splash是通过Lua脚本来控制了页面的加载过程的，加载过程完全模拟浏览器，最后可返回各种格式的结果，如网页源码和截图等。

### splash lua脚本
Splash可以通过Lua脚本执行一系列渲染操作，这样我们就可以用Splash来模拟类似Chrome、PhantomJS的操作了。

首先，我们来了解一下Splash Lua脚本的入口和执行方式。
#### 入口及返回值
```lua
function main(splash, args)
  splash:go("http://www.baidu.com")
  splash:wait(0.5)
  local title = splash:evaljs("document.title")
  return {title=title}
end
```
我们将代码粘贴到刚才打开的http://localhost:8050/的代码编辑区域，然后点击Render me!按钮来测试一下。

我们看到它返回了网页的标题，这里我们通过evaljs()方法传入JavaScript脚本，而document.title的执行结果就是返回网页标题，执行完毕后将其赋值给一个title变量，随后将其返回。

注意，我们在这里定义的方法名称叫作main()。这个名称必须是固定的，Splash会默认调用这个方法。

该方法的返回值既可以是字典形式，也可以是字符串形式，最后都会转化为Splash HTTP Response，例如：
```lua
function main(splash)
    return {hello="world!"}
end
```

#### 异步处理
Splash支持异步处理，但是这里并没有显式指明回调方法，其回调的跳转是在Splash内部完成的。示例如下：
```lua
function main(splash, args)
  local example_urls = {"www.baidu.com", "www.taobao.com", "www.zhihu.com"}
  local urls = args.urls or example_urls
  local results = {}
  for index, url in ipairs(urls) do
    local ok, reason = splash:go("http://" .. url)
    if ok then
      splash:wait(2)
      results[url] = splash:png()
    end
  end
  return results
end
```
运行结果是3个站点的截图

在脚本内调用的wait()方法类似于Python中的sleep()，其参数为等待的秒数。当Splash执行到此方法时，它会转而去处理其他任务，然后在指定的时间过后再回来继续处理。

这里值得注意的是，Lua脚本中的字符串拼接和Python不同，它使用的是..操作符，而不是+。如果有必要，可以简单了解一下[Lua脚本的语法](http://www.runoob.com/lua/lua-basic-syntax.html)。

另外，这里做了加载时的异常检测。go()方法会返回加载页面的结果状态，如果页面出现4xx或5xx状态码，ok变量就为空，就不会返回加载后的图片。

#### Splash对象属性
我们注意到，前面例子中main()方法的第一个参数是splash，这个对象非常重要，它类似于Selenium中的WebDriver对象，我们可以调用它的一些属性和方法来控制加载过程。接下来，先看下它的属性。

- args

该属性可以获取加载时配置的参数，比如URL，如果为GET请求，它还可以获取GET请求参数；如果为POST请求，它可以获取表单提交的数据。Splash也支持使用第二个参数直接作为args，例如：
```
function main(splash, args)
    local url = args.url
end
```
这里第二个参数args就相当于splash.args属性，以上代码等价于：
```
function main(splash)
    local url = splash.args.url
end
```
- js_enabled

这个属性是Splash的JavaScript执行开关，可以将其配置为true或false来控制是否执行JavaScript代码，默认为true。例如，这里禁止执行JavaScript代码：
```
function main(splash, args)
  splash:go("https://www.baidu.com")
  splash.js_enabled = false
  local title = splash:evaljs("document.title")
  return {title=title}
end
```
接着我们重新调用了evaljs()方法执行JavaScript代码，此时运行结果就会抛出异常：
```
{
    "error": 400,
    "type": "ScriptError",
    "info": {
        "type": "JS_ERROR",
        "js_error_message": null,
        "source": "[string \"function main(splash, args)\r...\"]",
        "message": "[string \"function main(splash, args)\r...\"]:4: unknown JS error: None",
        "line_number": 4,
        "error": "unknown JS error: None",
        "splash_method": "evaljs"
    },
    "description": "Error happened while executing Lua script"
}
```
不过一般来说，不用设置此属性，默认开启即可。

- resource_timeout

此属性可以设置加载的超时时间，单位是秒。如果设置为0或nil（类似Python中的None），代表不检测超时。示例如下：

```
function main(splash)
    splash.resource_timeout = 0.1
    assert(splash:go('https://www.taobao.com'))
    return splash:png()
end
```
例如，这里将超时时间设置为0.1秒。如果在0.1秒之内没有得到响应，就会抛出异常，错误如下：
```
{
    "error": 400,
    "type": "ScriptError",
    "info": {
        "error": "network5",
        "type": "LUA_ERROR",
        "line_number": 3,
        "source": "[string \"function main(splash)\r...\"]",
        "message": "Lua error: [string \"function main(splash)\r...\"]:3: network5"
    },
    "description": "Error happened while executing Lua script"
}
```
此属性适合在网页加载速度较慢的情况下设置。如果超过了某个时间无响应，则直接抛出异常并忽略即可。

- images_enabled

设置图片是否加载，默认情况下是加载的。禁用该属性后，可以节省网络流量并提高网页加载速度。但是需要注意的是，禁用图片加载可能会影响JavaScript渲染。因为禁用图片之后，它的外层DOM节点的高度会受影响，进而影响DOM节点的位置。因此，如果JavaScript对图片节点有操作的话，其执行就会受到影响。

另外值得注意的是，Splash使用了缓存。如果一开始加载出来了网页图片，然后禁用了图片加载，再重新加载页面，之前加载好的图片可能还会显示出来，这时直接重启Splash即可。
```
function main(splash, args)
  splash.images_enabled = false
  assert(splash:go('https://www.jd.com'))
  return {png=splash:png()}
end
```
- plugins_enabled

控制浏览器插件（如Flash插件）是否开启。默认情况下，此属性是false，表示不开启。可以使用如下代码控制其开启和关闭：
```
splash.plugins_enabled = true/false
```
- scroll_position

控制页面上下或左右滚动
```
function main(splash, args)
  assert(splash:go('https://www.taobao.com'))
  splash.scroll_position = {y=400}
  return {png=splash:png()}
end
```
如果要让页面左右滚动，可以传入x参数，代码如下：
```
splash.scroll_position = {x=100, y=200}
```

#### Splash对象的方法
`go()`

该方法用来请求某个链接，而且它可以模拟GET和POST请求，同时支持传入请求头、表单等数据，其用法如下：
```
ok, reason = splash:go{url, baseurl=nil, headers=nil, http_method="GET", body=nil, formdata=nil}
```
其参数说明如下。
- url：请求的URL。
- baseurl：可选参数，默认为空，表示资源加载相对路径。
- headers：可选参数，默认为空，表示请求头。
- http_method：可选参数，默认为GET，同时支持POST。
- body：可选参数，默认为空，发POST请求时的表单数据，使用的Content-type为application/json。
- formdata：可选参数，默认为空，POST的时候的表单数据，使用的Content-type为application/x-www-form-urlencode

该方法的返回结果是结果ok和原因reason的组合，如果ok为空，代表网页加载出现了错误，此时reason变量中包含了错误的原因，否则证明页面加载成功。示例如下：

```
function main(splash, args)
  local ok, reason = splash:go{"http://httpbin.org/post", http_method="POST", body="name=Germey"}
  if ok then
        return splash:html()
  end
end
```
`wait()`

此方法可以控制页面的等待时间，使用方法如下：
```
ok, reason = splash:wait{time, cancel_on_redirect=false, cancel_on_error=true}
```
参数说明如下。
- time：等待的秒数。
- cancel_on_redirect：可选参数，默认为false，表示如果发生了重定向就停止等待，并返回重定向结果。
- cancel_on_error：可选参数，默认为false，表示如果发生了加载错误，就停止等待。

返回结果同样是结果ok和原因reason的组合。
```
function main(splash)
    splash:go("https://www.taobao.com")
    splash:wait(2)
    return {html=splash:html()}
end
```
`jsfunc()`

此方法可以直接调用JavaScript定义的方法，但是所调用的方法需要用双中括号包围，这相当于实现了JavaScript方法到Lua脚本的转换。示例如下：
```
function main(splash, args)
  local get_div_count = splash:jsfunc([[
  function () {
    var body = document.body;
    var divs = body.getElementsByTagName('div');
    return divs.length;
  }
  ]])
  splash:go("https://www.baidu.com")
  return ("There are %s DIVs"):format(
    get_div_count())
end
```
关于JavaScript到Lua脚本的更多转换细节, 可以参考[官方文档](https://splash.readthedocs.io/en/stable/scripting-ref.html#splash-jsfunc)

`evaljs()`

此方法可以执行JavaScript代码并返回最后一条JavaScript语句的返回结果，使用方法如下：
```
result = splash:evaljs(js)
```
`runjs()`

与evaljs()的功能类似，但是更偏向于执行某些动作或声明某些方法。例如：
```
function main(splash, args)
  splash:go("https://www.baidu.com")
  splash:runjs("foo = function() { return 'bar' }")
  local result = splash:evaljs("foo()")
  return result
end
```

`autoload()`

此方法可以设置每个页面访问时自动加载的对象
```
ok, reason = splash:autoload{source_or_url, source=nil, url=nil}
```
参数说明如下。
- source_or_url：JavaScript代码或者JavaScript库链接。
- source：JavaScript代码。
- url：JavaScript库链接

但是此方法只负责加载JavaScript代码或库，不执行任何操作。如果要执行操作，可以调用evaljs()或runjs()方法。示例如下：
```
function main(splash, args)
  splash:autoload([[
    function get_document_title(){
      return document.title;
    }
  ]])
  splash:go("https://www.baidu.com")
  return splash:evaljs("get_document_title()")
end
```
这里我们调用autoload()方法声明了一个JavaScript方法，然后通过evaljs()方法来执行此JavaScript方法。

另外，我们也可以使用autoload()方法加载某些方法库，如jQuery
```
function main(splash, args)
  assert(splash:autoload("https://code.jquery.com/jquery-2.1.3.min.js"))
  assert(splash:go("https://www.taobao.com"))
  local version = splash:evaljs("$.fn.jquery")
  return 'JQuery version: ' .. version
end
```

`call_later()`

此方法可以通过设置定时任务和延迟时间来实现任务延时执行，并且可以在执行前通过cancel()方法重新执行定时任务。
```
function main(splash, args)
  local snapshots = {}
  local timer = splash:call_later(function()
    snapshots["a"] = splash:png()
    splash:wait(1.0)
    snapshots["b"] = splash:png()
  end, 0.2)
  splash:go("https://www.taobao.com")
  splash:wait(3.0)
  return snapshots
end
```
这里我们设置了一个定时任务，0.2秒的时候获取网页截图，然后等待1秒，1.2秒时再次获取网页截图，访问的页面是淘宝，最后将截图结果返回

`http_get()`

可以模拟发送HTTP的GET请求
```
response = splash:http_get{url, headers=nil, follow_redirects=true}
```
```
function main(splash, args)
  local treat = require("treat")
  local response = splash:http_get("http://httpbin.org/get")
    return {
    html=treat.as_string(response.body),
    url=response.url,
    status=response.status
    }
end
```

`http_post()`

模拟发送POST请求, 不过多了一个参数body
```
response = splash:http_post{url, headers=nil, follow_redirects=true, body=nil}
```
参数说明:
- body: 可选参数, 即表单数据, 默认为空
```
function main(splash, args)
  local treat = require("treat")
  local json = require("json")
  local response = splash:http_post{"http://httpbin.org/post",
      body=json.encode({name="Germey"}),
      headers={["content-type"]="application/json"}
    }
    return {
    html=treat.as_string(response.body),
    url=response.url,
    status=response.status
    }
end
```

`set_content()`

用来设置页面的内容
```
function main(splash)
    assert(splash:set_content("<html><body><h1>hello</h1></body></html>"))
    return splash:png()
end
```

`html()`

此方法用来获取网页的源代码，它是非常简单又常用的方法。
```
function main(splash, args)
  splash:go("https://httpbin.org/get")
  return splash:html()
end
```

`png()`

用来获取PNG格式的网页截图
```
function main(splash, args)
  splash:go("https://www.taobao.com")
  return splash:png()
end
```

`jpeg()`

类似png()

`har()`

此方法用来获取页面加载过程描述
```
function main(splash, args)
  splash:go("https://www.baidu.com")
  return splash:har()
end
```

`url()`

获取当前正在访问的URL
```
function main(splash, args)
  splash:go("https://www.baidu.com")
  return splash:url()
end
```

`get_cookies()`

获取当前页面的cookies
```
function main(splash, args)
  splash:go("https://www.baidu.com")
  return splash:get_cookies()
end
```

`add_cookie()`

为当前页面添加Cookie
```
cookies = splash:add_cookie{name, value, path=nil, domain=nil, expires=nil, httpOnly=nil, secure=nil}
```
该方法的各个参数代表Cookie的各个属性
```
function main(splash)
    splash:add_cookie{"sessionid", "237465ghgfsd", "/", domain="http://example.com"}
    splash:go("http://example.com/")
    return splash:html()
end
```

`clear_cookies()`

清除所有的Cookies
```
function main(splash)
    splash:go("https://www.baidu.com/")
    splash:clear_cookies()
    return splash:get_cookies()
end
```
返回结果
```
Splash Response: Array[0]
```

`get_viewport_size()`

获取当前浏览器页面的大小，即宽高
```
function main(splash)
    splash:go("https://www.baidu.com/")
    return splash:get_viewport_size()
end
```

`set_viewport_size()`

设置当前浏览器页面的大小，即宽高
```
splash:set_viewport_size(width, height)
```

`set_viewport_full()`

可以设置浏览器全屏显示

`set_user_agent()`

设置浏览器的User-Agent
```
function main(splash)
  splash:set_user_agent('Splash')
  splash:go("http://httpbin.org/get")
  return splash:html()
end
```

`set_custom_headers()`

设置请求头
```
function main(splash)
  splash:set_custom_headers({
     ["User-Agent"] = "Splash",
     ["Site"] = "Splash",
  })
  splash:go("http://httpbin.org/get")
  return splash:html()
end
```

`select()`

该方法可以选中符合条件的第一个节点，如果有多个节点符合条件，则只会返回一个，其参数是CSS选择器。
```
function main(splash)
  splash:go("https://www.baidu.com/")
  input = splash:select("#kw")
  input:send_text('Splash')
  splash:wait(3)
  return splash:png()
end
```

`select_all()`

此方法可以选中所有符合条件的节点，其参数是CSS选择器。
```
function main(splash)
  local treat = require('treat')
  assert(splash:go("http://quotes.toscrape.com/"))
  assert(splash:wait(0.5))
  local texts = splash:select_all('.quote .text')
  local results = {}
  for index, text in ipairs(texts) do
    results[index] = text.node.innerHTML
  end
  return treat.as_array(results)
end
```
这里我们通过CSS选择器选中了节点的正文内容，随后遍历了所有节点，将其中的文本获取下来

`mouse_click()`

可以模拟鼠标点击操作，传入的参数为坐标值x和y。此外，也可以直接选中某个节点，然后调用此方法
```
function main(splash)
  splash:go("https://www.baidu.com/")
  input = splash:select("#kw")
  input:send_text('Splash')
  submit = splash:select('#su')
  submit:mouse_click()
  splash:wait(3)
  return splash:png()
end
```

`focus()`

得到输入框焦点
```
function main(splash, args)
    function focus(sel)
        splash:select(sel):focus()
    end

    assert(splash:go(args.url))
    assert(splash:wait(0.5))
    focus('input[name=username]')
    splash:send_text(args.username)
    assert(splash:wait(0))
    focus('input[name=password]')
    splash:send_text(args.password)
    splash:select('input[type=submit]'):mouse_click()
    assert(splash:wait(0))
    -- Usually, wait for the submit request to finish
    -- ...
end
```

前面介绍了Splash的常用API操作，还有一些API在这不再一一介绍，更加详细和权威的说明可以参见[官方文档](https://splash.readthedocs.io/en/stable/scripting-ref.html), 此页面介绍了Splash对象的所有API操作。另外，还有[针对页面元素的API操作](https://splash.readthedocs.io/en/stable/scripting-element-object.html)

## Splash API调用
前面说明了Splash Lua脚本的用法，但这些脚本是在Splash页面中测试运行的，如何才能利用Splash渲染页面呢？怎样才能和Python程序结合使用并抓取JavaScript渲染的页面呢？

其实Splash给我们提供了一些HTTP API接口，我们只需要请求这些接口并传递相应的参数即可，下面简要介绍这些接口。

### render.html
此接口用于获取JavaScript渲染的页面的HTML代码，接口地址就是Splash的运行地址加此接口名称，例如http://localhost:8050/render.html。可以用curl来测试一下：
```
curl http://localhost:8050/render.html?url=https://www.baidu.com
```
如果用Python实现的话，代码如下：
```
import requests
url = 'http://localhost:8050/render.html?url=https://www.baidu.com&wait=5'
response = requests.get(url)
print(response.text)
```
另外，此接口还可以指定其他参数，比如通过wait指定等待秒数。如果要确保页面完全加载出来，可以增加等待时间

另外，此接口还支持代理设置、图片加载设置、Headers设置、请求方法设置，具体的用法可以参见[官方文档](https://splash.readthedocs.io/en/stable/api.html#render-html)

### render.png
此接口可以获取网页截图，其参数比render.html多了几个，比如通过width和height来控制宽高，它返回的是PNG格式的图片二进制数据。示例如下：
```
import requests

url = 'http://localhost:8050/render.png?url=https://www.jd.com&wait=5&width=1000&height=700'
response = requests.get(url)
with open('taobao.png', 'wb') as f:
    f.write(response.content)
```

### render.jpeg
类似render.png, 不过它返回的是JPEG格式的图片二进制数据

另外，此接口比render.png多了参数quality，它用来设置图片质量

### render.har
此接口用于获取页面加载的HAR数据
```
curl http://localhost:8050/render.har?url=https://www.jd.com&wait=5
```
它的返回结果非常多，是一个JSON格式的数据，其中包含页面加载过程中的HAR数据

### render.json
此接口包含了前面接口的所有功能，返回结果是JSON格式
```
curl http://localhost:8050/render.json?url=https://httpbin.org
```
结果如下
```
{"title": "httpbin(1): HTTP Client Testing Service", "url": "https://httpbin.org/", "requestedUrl": "https://httpbin.org/", "geometry": [0, 0, 1024, 768]}
```
我们可以通过传入不同参数控制其返回结果。比如，传入html=1，返回结果即会增加源代码数据；传入png=1，返回结果即会增加页面PNG截图数据；传入har=1，则会获得页面HAR数据。例如
```
curl http://localhost:8050/render.json?url=https://httpbin.org&html=1&har=1
```
这样返回的JSON结果会包含网页源代码和HAR数据

此外还有更多参数设置，具体可以参考[官方文档](https://splash.readthedocs.io/en/stable/api.html#render-json)

### execute
此接口才是最为强大的接口。前面说了很多Splash Lua脚本的操作，用此接口便可实现与Lua脚本的对接

前面的render.html和render.png等接口对于一般的JavaScript渲染页面是足够了，但是如果要实现一些交互操作的话，它们还是无能为力，这里就需要使用execute接口了。

我们先实现一个最简单的脚本，直接返回数据：
```
function main(splash)
    return 'hello'
end
```
然后将此脚本转化为URL编码后的字符串，拼接到execute接口后面，示例如下：
```
curl http://localhost:8050/execute?lua_source=function+main%28splash%29%0D%0A++return+%27hello%27%0D%0Aend
```
运行结果如下：
```
hello
```
这里我们通过lua_source参数传递了转码后的Lua脚本，通过execute接口获取了最终脚本的执行结果

这里我们更加关心的肯定是如何用Python来实现，上例用Python实现的话，代码如下：
```
import requests
from urllib.parse import quote

lua = '''
function main(splash)
    return 'hello'
end
'''

url = 'http://localhost:8050/execute?lua_source=' + quote(lua)
response = requests.get(url)
print(response.text)
```

我们再通过实例看一下：
```
import requests
from urllib.parse import quote

lua = '''
function main(splash, args)
  local treat = require("treat")
  local response = splash:http_get("http://httpbin.org/get")
    return {
    html=treat.as_string(response.body),
    url=response.url,
    status=response.status
    }
end
'''

url = 'http://localhost:8050/execute?lua_source=' + quote(lua)
response = requests.get(url)
print(response.text)
```
结果如下:
```
{"url": "http://httpbin.org/get", "status": 200, "html": "{\n  \"args\": {}, \n  \"headers\": {\n    \"Accept-Encoding\": \"gzip, deflate\", \n    \"Accept-Language\": \"en,*\", \n    \"Connection\": \"close\", \n    \"Host\": \"httpbin.org\", \n    \"User-Agent\": \"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/602.1 (KHTML, like Gecko) splash Version/9.0 Safari/602.1\"\n  }, \n  \"origin\": \"60.207.237.85\", \n  \"url\": \"http://httpbin.org/get\"\n}\n"}
```
可以看到，返回结果是JSON形式，我们成功获取了请求的URL、状态码和网页源代码。

如此一来，我们之前所说的Lua脚本均可以用此方式与Python进行对接，所有网页的动态渲染、模拟点击、表单提交、页面滑动、延时等待后的一些结果均可以自由控制，获取页面源码和截图也都不在话下。

到现在为止，我们可以用Python和Splash实现JavaScript渲染的页面的抓取了。除了Selenium，本节所说的Splash同样可以做到非常强大的渲染功能，同时它也不需要浏览器即可渲染，使用非常方便。

### splash动态设置设置代理
lua中脚本设置代理和请求头
```bash
function main(splash, args)
    -- 设置代理              
    splash:on_request(function(request)
        request:set_proxy{
            host = "27.0.0.1",
            port = 8000,
        }
        end)

    -- 设置请求头
    splash:set_user_agent("Mozilla/5.0")

    splash:go("https://www.baidu.com/")
    return splash:html()
```

