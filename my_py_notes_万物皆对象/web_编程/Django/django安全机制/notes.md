## 1. xss
django 已经能防范95%的xss问题，主要原理就是将<,>,&做了转化，但是如下情况还是无能为力

（1）属性有动态内容，正确：<img alt="{{good}}">,错误：<img alt={{bad}}>,请确保加上双引号。

（2）插入到CSS中的数据(style 标签和属性),以及javascript(script标签,事件处理器,onclick等其他属性),在这些标签内请手动escape.

（3）还有就是使用了mark_safe跳过了template默认机制或者autoescape关闭了。

（4）涉及到dom类型的xss，如document.write等

（5）HttpResponse返回动态内容

另外注意属性中包含url(href,img src)时验证url协议在白名单内(如http,https,mailto,ftp)

## 2. csrf
1，确保django.middleware.csrf.CsrfViewMiddleware已经开启 在settings.py中，默认是存在的。

2，在所有的post表单中中添加了csrf_token，如

{% csrf_token %}

3，在相应的view函数中，使用了django.template.context_processors.csrf，用法有两种，一个是RequestContext,另外就是手工引入,如下是手工引入:
```python
from django.shortcuts import render_to_response
from django.template.context_processors import csrf
def my_view(request):
    c = {}
    c.update(csrf(request))
    # ... view code here
    return render_to_response("a_template.html", c)
```
@csrf_exempt装饰器是去除csrf防护,另外内置的CSRF保护机制对子域也是无能为力,比如应用在example.com,有一个子域alice.example.com放置用户可控制的内容,这个时候csrf机制是不起作用的.

最后注意不要使用get请求去做增删改操作,否则内置的CSRF机制也是无效的.

## 3. sql注入
直接拼接的sql会有注入风险，那如何避免呢？使用django的数据库api，会根据对应的数据库加过滤，但是有两个例外：

（1）extra方法中的where参数处,这个参数是故意设计成接受原始SQL；

extra的正确用法：

Entry.objects.extra(where=['headline=%s'], params=['Lennon'])

错误用法：

Entry.objects.extra(where=["headline='Lennon'"])

（2）直接使用低层次的数据库api，如execute，raw，可以采用cursor.execute(sql, [user])方式避免，但是部分时候是失效的，如表的位置，列的位置，这种情况下可以使用django.db.connection.ops.quote_name来自己手工加过滤

在有params的情况下，django会正确的转义，没有params的情况则不行。正确做法:
```python
from django.db import connection
 
def user_contacts(request):
    user = request.GET['username']
    sql = "SELECT * FROM user_contacts WHERE username = %s"
    cursor = connection.cursor()
    cursor.execute(sql, [user])
    # ... do something with the results
```

## 4. 点击劫持
django已经有X-Frame-Options middleware来处理，强烈建议添加

## 5. host头验证
使用django.http.HttpRequest.get_host() 可以获取到host，有伪造的话直接报错了，如果直接访问request.META则没有这效果

## 6. 文件上传
django的imageField只会判断上传的文件是否有一个合法的png头，所以基本上无法限制有害文件的上传。

（1）另建一个文件服务器

（2）限制文件大小，防止dos攻击，如设置apache的LimitRequestBody大小

（3）确保文件不可执行

（4）传到二级域名上，比如说传到usercontent-example.com上而不是usercontent.example.com上

（5）限制文件上传的类型

## 7. email头注入
用于发送垃圾邮件，hacker发送如下：hello\ncc:spamvictim@example.com 就转变成了
To: hardcoded@example.com Subject: hello cc: spamvictim@example.com 可使用djaong.core.mail来发送，他是不允许任意字段中包含newlines

## 8. 目录遍历
目录遍历也算一种注入,主要是突破目录限制读取或者写入文件,django中内置的静态内容视图就是一个做转义很好的例子(django.views.static),相关代码如下:
```python
import os
import posixpath
 
path = posixpath.normpath(urllib.unquote(path))
newpath = ''
for part in path.split('/'):
    if not part:
        # strip empty path components
        continue
 
    drive, part = os.path.splitdrive(part)
    head, part = os.path.split(part)
    if part in (os.curdir, os.pardir):
        # strip '.' and '..' in path
        continue
 
    newpath = os.path.join(newpath, part).replace('\\', '/')
```
