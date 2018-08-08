#### url
```html
全局资源定位符(universal resource location)
```
#### HTTP响应分为Header和Body两部分（Body是可选项），我们在Network中看到的Header最重要的几行如下：
#### 响应的状态码
    HTTP/1.1 200 OK
200表示一个成功的响应，后面的OK是说明。

如果返回的不是200，那么往往有其他的功能，例如
```
失败的响应有404 Not Found：网页不存在
403     拒绝执行
500 Internal Server Error：服务器内部出错
...等等...
```
#### Content-type:text/html
Content-Type指示响应的内容，这里是text/html表示HTML网页。
```html
请注意，浏览器就是依靠Content-Type来判断响应的内容是网页还是图片，是视频还是音乐。
浏览器并不靠URL来判断响应的内容，
所以，即使URL是http://www.baidu.com/meimei.jpg，它也不一定就是图片。
```

#### HTTP响应的Body就是HTML源码

## 总结
#### HTTP请求
跟踪了新浪的首页，我们来总结一下HTTP请求的流程：
```html
步骤1：浏览器首先向服务器发送HTTP请求，请求包括：
```
```html
方法：GET还是POST，GET仅请求资源，POST会附带用户数据；
路径：/full/url/path；
域名：由Host头指定：Host: www.sina.com
以及其他相关的Header；
如果是POST，那么请求还包括一个Body，包含用户数据
```
```html
步骤2：服务器向浏览器返回HTTP响应，响应包括：
```
```html
响应代码：200表示成功，3xx表示重定向，4xx表示客户端发送的请求有错误，5xx表示服务器端处理时发生了错误；
响应类型：由Content-Type指定；
以及其他相关的Header；
通常服务器的HTTP响应会携带内容，也就是有一个Body，包含响应的内容，网页的HTML源码就在Body中。
```
```html
步骤3：如果浏览器还需要继续向服务器请求其他资源，比如图片，就再次发出HTTP请求，重复步骤1、2
```
```html
Web采用的HTTP协议采用了非常简单的请求-响应模式，
从而大大简化了开发。当我们编写一个页面时，我们只需要在
HTTP请求中把HTML发送出去，不需要考虑如何附带图片、视频等，
浏览器如果需要请求图片和视频，它会发送另一个HTTP请求，
因此，一个HTTP请求只处理一个资源
(此时就可以理解为TCP协议中的短连接，每个链接只获取一个资源，如需要多个就需要建立多个链接)
```
HTTP协议同时具备极强的扩展性，虽然浏览器请求的是http://www.sina.com的首页，但是新浪在HTML中可以链入其他服务器的资源，比如<img src="http://i1.sinaimg.cn/home/2013/1008/U8455P30DT20131008135420.png">，从而将请求压力分散到各个服务器上，并且，一个站点可以链接到其他站点，无数个站点互相链接起来，就形成了World Wide Web，简称WWW。

#### HTTP格式
每个HTTP请求和响应都遵循相同的格式，一个HTTP包含Header和Body两部分，其中Body是可选的。

HTTP协议是一种文本协议，所以，它的格式也非常简单
#### HTTP GET请求的格式：(从服务器获取数据)
```html
    GET /path HTTP/1.1
    Header1: Value1
    Header2: Value2
    Header3: Value3
```
每个Header一行一个，换行符是\r\n
#### HTTP POST请求的格式:(让服务器保存数据)
```html
    POST /path HTTP/1.1
    Header1: Value1
    Header2: Value2
    Header3: Value3

    body data goes here...
```
当遇到连续两个\r\n时，Header部分结束，后面的数据全部是Body。
#### HTTP响应的格式：
```html
    200 OK
    Header1: Value1
    Header2: Value2
    Header3: Value3

    body data goes here...
```
HTTP响应如果包含body，也是通过\r\n\r\n来分隔的。

请再次注意，Body的数据类型由Content-Type头来确定，如果是网页，Body就是文本，如果是图片，Body就是图片的二进制数据。

当存在Content-Encoding时，Body数据是被压缩的，最常见的压缩方式是gzip，所以，看到Content-Encoding: gzip时，需要将Body数据先解压缩，才能得到真正的数据。压缩的目的在于减少Body的大小，加快网络传输。

#### PUT(让服务器修改数据)
#### DELETE(让服务器删除资源数据)
HTTP 1.0 使用tcp传输层 默认使用短链接 通过在报文中添加Connection:keep-alive字段 ,可以在HTTP1.0中也启用tcp长连接
HTTP 1.1 默认使用长连接
Content-Length: 110\r\n # 描述请求体部分的数据长度 字节

#### Connection (链接类型)
Connection：表示客户端与服务连接类型
```
1. Client 发起一个包含 Connection:keep-alive 的请求，HTTP/1.1使用 keep-alive 为默认值。

2. Server收到请求后：
    如果 Server 支持 keep-alive，回复一个包含 Connection:keep-alive 的响应，不关闭连接；
    如果 Server 不支持 keep-alive，回复一个包含 Connection:close 的响应，关闭连接。
3. 如果client收到包含 Connection:keep-alive 的响应，向同一个连接发送下一个请求，直到一方主动关闭连接。
```
#### Upgrade-Insecure-Requests (升级为HTTPS请求)
Upgrade-Insecure-Requests：升级不安全的请求，意思是会在加载 http 资源时自动替换成 https 请求，让浏览器不再显示https页面中的http请求警报。

HTTPS 是以安全为目标的 HTTP 通道，所以在 HTTPS 承载的页面上不允许出现 HTTP 请求，一旦出现就是提示或报错
keep-alive在很多情况下能够重用连接，减少资源消耗，缩短响应时间，比如当浏览器需要多个文件时(比如一个HTML文件和相关的图形文件)，不需要每次都去请求建立连接

#### User-Agent (浏览器名称)
User-Agent：是客户浏览器的名称，以后会详细讲

#### Accept (传输文件类型)
Accept：指浏览器或其他客户端可以接受的MIME（Multipurpose Internet Mail Extensions（多用途互联网邮件扩展））文件类型，服务器可以根据它判断并返回适当的文件格式。

举例：
```
Accept: */*：表示什么都可以接收。

Accept：image/gif：表明客户端希望接受GIF图像格式的资源；

Accept：text/html：表明客户端希望接受html文本。

Accept: text/html, application/xhtml+xml;q=0.9, image/*;q=0.8：表示浏览器支持的 MIME 类型分别是 html文本、xhtml和xml文档、所有的图像格式资源。

q是权重系数，范围 0 =< q <= 1，q 值越大，请求越倾向于获得其“;”之前的类型表示的内容。若没有指定q值，则默认为1，按从左到右排序顺序；若被赋值为0，则用于表示浏览器不接受此内容类型。

Text：用于标准化地表示的文本信息，文本消息可以是多种字符集和或者多种格式的；Application：用于传输应用程序数据或者二进制数据
```
#### Referer (页面跳转处)
Referer：表明产生请求的网页来自于哪个URL，用户是从该 Referer页面访问到当前请求的页面。这个属性可以用来跟踪Web请求来自哪个页面，是从什么网站来的等。

有时候遇到下载某网站图片，需要对应的referer，否则无法下载图片，那是因为人家做了防盗链，原理就是根据referer去判断是否是本网站的地址，如果不是，则拒绝，如果是，就可以下载；
#### Accept-Encoding（文件编解码格式）
Accept-Encoding：指出浏览器可以接受的编码方式。编码方式不同于文件格式，它是为了压缩文件并加速文件传递速度。浏览器在接收到Web响应之后先解码，然后再检查文件格式，许多情形下这可以减少大量的下载时间。

举例：Accept-Encoding:gzip;q=1.0, identity; q=0.5, *;q=0

如果有多个Encoding同时匹配, 按照q值顺序排列，本例中按顺序支持 gzip, identity压缩编码，支持gzip的浏览器会返回经过gzip编码的HTML页面。 如果请求消息中没有设置这个域服务器假定客户端对各种内容编码都可以接受。
#### Accept-Charset（字符编码）

Accept-Charset：指出浏览器可以接受的字符编码。

举例：Accept-Charset:iso-8859-1,gb2312,utf-8
```
* ISO8859-1：通常叫做Latin-1。Latin-1包括了书写所有西方欧洲语言不可缺少的附加字符，英文浏览器的默认值是ISO-8859-1.
* gb2312：标准简体中文字符集;
* utf-8：UNICODE 的一种变长字符编码，可以解决多种语言文本显示问题，从而实现应用国际化和本地化。
```
```
如果在请求消息中没有设置这个域，缺省是任何字符集都可以接受
```
#### Cookie （Cookie）
Cookie：浏览器用这个属性向服务器发送Cookie。Cookie是在浏览器中寄存的小型数据体，它可以记载和服务器相关的用户信息，也可以用来实现会话功能

## 服务端HTTP响应
HTTP响应也由四个部分组成，分别是： 状态行、消息报头、空行、响应正文
![](./images/01_response.jpg)
```html
HTTP/1.1 200 OK
Server: Tengine
Connection: keep-alive
Date: Wed, 30 Nov 2016 07:58:21 GMT
Cache-Control: no-cache
Content-Type: text/html;charset=UTF-8
Keep-Alive: timeout=20
Vary: Accept-Encoding
Pragma: no-cache
X-NWS-LOG-UUID: bd27210a-24e5-4740-8f6c-25dbafa9c395
Content-Length: 180945

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" ....
```
#### Cache-Control：must-revalidate, no-cache, private。
这个值告诉客户端，服务端不希望客户端缓存资源，在下次请求资源时，必须要从新请求服务器，不能从缓存副本中获取资源。
```
* Cache-Control是响应头中很重要的信息，当客户端请求头中包含Cache-Control:max-age=0请求，明确表示不会缓存服务器资源时,Cache-Control作为作为回应信息，通常会返回no-cache，意思就是说，"那就不缓存呗"。

* 当客户端在请求头中没有包含Cache-Control时，服务端往往会定,不同的资源不同的缓存策略，比如说oschina在缓存图片资源的策略就是Cache-Control：max-age=86400,这个意思是，从当前时间开始，在86400秒的时间内，客户端可以直接从缓存副本中读取资源，而不需要向服务器请求。
```
#### Pragma:no-cache
这个含义与Cache-Control等同
#### Transfer-Encoding：chunked
这个响应头告诉客户端，服务器发送的资源的方式是分块发送的。一般分块发送的资源都是服务器动态生成的，在发送时还不知道发送资源的大小，所以采用分块发送，每一块都是独立的，独立的块都能标示自己的长度，最后一块是0长度的，当客户端读到这个0长度的块时，就可以确定资源已经传输完了

#### 常见状态码：
```
* 100~199：表示服务器成功接收部分请求，要求客户端继续提交其余请求才能完成整个处理过程。

* 200~299：表示服务器成功接收请求并已完成整个处理过程。常用200（OK 请求成功）。

* 300~399：为完成请求，客户需进一步细化请求。例如：请求的资源已经移动一个新地址、常用302（所请求的页面已经临时转移至新的url）、307和304（使用缓存资源）。
* 400~499：客户端的请求有错误，常用404（服务器无法找到被请求的页面）、403（服务器拒绝访问，权限不够）。
* 500~599：服务器端出现错误，常用500（请求未完成。服务器遇到不可预知的情况）
```
#### Cookie 和 Session：

服务器和客户端的交互仅限于请求/响应过程，结束之后便断开，在下一次请求时，服务器会认为新的客户端。

为了维护他们之间的链接，让服务器知道这是前一个用户发送的请求，必须在一个地方保存客户端的信息。
```
Cookie：通过在 客户端 记录的信息确定用户的身份。
Session：通过在 服务器端 记录的信息确定用户的身份
```