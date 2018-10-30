# coding = utf-8

'''
@author = super_fazai
@File    : tasks.py
@Time    : 2017/8/20 10:33
@connect : superonesfazai@gmail.com
'''

"""
Scrapy选择器是Selector通过传递文本或TextResponse 对象构造的类的实例。
它根据输入类型自动选择最佳解析规则(XML vs HTML)
"""

from scrapy.selector import Selector
from scrapy.http import HtmlResponse

# 从文本构建
body = '<html><body><span>good</span></body></html>'
print(Selector(text=body).xpath('//span/text()').extract())

# 从response(响应)中构建
response = HtmlResponse(url='https://sebastianraschka.com/blog/index.html', body=body, encoding='utf-8')
print(Selector(response=response).xpath('//*/h1[@class="post-title"]/text()').extract())
# 上面那句等价于下面这句
print(response.selector.xpath('//*/h1[@class="post-title"]/text()').extract())

response = r"""
<html>
 <head>
  <base href='http://example.com/' />
  <title>Example website</title>
 </head>
 <body>
  <div id='images'>
   <a href='image1.html'>Name: My image 1 <br /><img src='image1_thumb.jpg' /></a>
   <a href='image2.html'>Name: My image 2 <br /><img src='image2_thumb.jpg' /></a>
   <a href='image3.html'>Name: My image 3 <br /><img src='image3_thumb.jpg' /></a>
   <a href='image4.html'>Name: My image 4 <br /><img src='image4_thumb.jpg' /></a>
   <a href='image5.html'>Name: My image 5 <br /><img src='image5_thumb.jpg' /></a>
  </div>
 </body>
</html>
"""

'''
使用选择器
'''
print('使用选择器'.center(60, '-'))
print(Selector(text=response).xpath('//title/text()'))
# 要实际提取文本数据, 必须调用extract()
print(Selector(text=response).css('img').xpath('@src').extract())

# 通过extract_first(default=)来设置默认值, 避免出错率
print(Selector(text=response).xpath('//div[@id="not-exists"]/text()').extract_first(default='not-found'))

print(Selector(text=response).xpath('//a[contains(@href, "image")]/@href').extract())
# 同上
print(Selector(text=response).css('a[href*=image]::attr(href)').extract())

'''
嵌套选择器
'''
print('嵌套选择器'.center(60, '-'))
# .xpath() 和 .css() -> return 一个selectors的类实例对象
links = Selector(text=response).xpath('//a[contains(@href, "image")]')
print(links.extract())

for index, link in enumerate(links):    # 通过enumerate(links)来得到对应属性
    args = (index, link.xpath('@href').extract(), link.xpath('img/@src').extract())
    print('Link number %d points to url %s and image %s' % args)

'''
使用正则表达式的selector
'''
print('使用正则表达式的selector'.center(60, '-'))
print(Selector(text=response).xpath('//a[contains(@href, "image")]/text()').re(r'Name:\s*(.*)'))
# .re_first()
print(Selector(text=response).xpath('//a[contains(@href, "image")]/text()').re_first(r'Name:\s*(.*)'))

'''
使用相对xpath
'''
print('使用相对xpath'.center(60, '-'))
# 请记住,如果您正在嵌套选择器并使用以XPath开头的XPath '/'
# 那么XPath对于文档是绝对的, 而不是相对于 Selector您所调用
divs = Selector(text=response).xpath('//div')
# for p in divs.xpath('//a'):     # 这是错的
#     print(p.extract())

# 这是正确的方法(注意.//pXPath 前面的点)：
for p in divs.xpath('.//a'):  # 提取出所有内部的<P>
    print(p.extract())
# 另外一种常见的情况是提取所有直接的子p
for p in divs.xpath('a'):
    print(p.extract())

'''
xpath表达式中的变量
'''
print('xpath表达式中的变量'.center(60, '-'))
# XPath允许您使用$somevariable语法在XPath表达式中引用变量。
# 这有点类似于SQL世界中的参数化查询或准备语句，您可以使用占位符替换查询中的一些参数?，然后将其替换为使用查询传递的值
print(Selector(text=response).xpath('//div[@id=$val]/a/text()', val='images').extract_first())

# 这是另一个例子,找到<div>包含五个<a>孩子的标签的“id”属性（这里我们将 值5 作为整数传递）
print(Selector(text=response).xpath('//div[count(a)=$cnt]/@id', cnt=5).extract_first())
# 记住：所有变量引用在调用时都必须具有绑定值.xpath() (否则会得到异常)。这是通过传递尽可能多的命名参数来完成的

'''
使用EXSLT扩展
'''
# 正在构建在lxml之上，Scrapy选择器还支持一些EXSLT扩展
# 并附带这些预先注册的命名空间以在XPath表达式中使用：
# 字首	    命名空间	                                用法
# re	    http://exslt.org/regular-expressions	正则表达式
# set(组) 	http://exslt.org/sets	                设置操纵

# 例如，当XPath starts-with()或者contains()不够的时候，这个功能可以证明是非常有用的 。

# 在列表项中选择链接，“class”属性以数字结尾：
print('使用EXSLT扩展'.center(60, '-'))
from scrapy import Selector
doc = r"""
<div>
    <ul>
        <li class="item-0"><a href="link1.html">first item</a></li>
        <li class="item-1"><a href="link2.html">second item</a></li>
        <li class="item-inactive"><a href="link3.html">third item</a></li>
        <li class="item-1"><a href="link4.html">fourth item</a></li>
        <li class="item-0"><a href="link5.html">fifth item</a></li>
    </ul>
</div>
"""
sel = Selector(text=doc, type="html")
print(sel.xpath('//li//@href').extract())
print(sel.xpath('//li[re:test(@class, "item-\d$")]//@href').extract())
# 警告:
#   C库libxslt本身不支持EXSLT正则表达式，所以lxml的实现使用钩子到Python的re模块。
#   因此，在XPath表达式中使用正则表达式函数可能会增加一些小的性能损失

'''
设置操作
'''
# 在提取文本元素之前，这些可以方便地排除文档树的部分

# 从示范组和相应的itemprops中提取微数据(从http://schema.org/Product获取的样本内容)示例：
print('设置操作'.center(60, '-'))
doc = r"""
<div itemscope itemtype="http://schema.org/Product">
    <span itemprop="name">Kenmore White 17" Microwave</span>
    <img src="kenmore-microwave-17in.jpg" alt='Kenmore 17" Microwave' />
    <div itemprop="aggregateRating"
        itemscope itemtype="http://schema.org/AggregateRating">
        Rated <span itemprop="ratingValue">3.5</span>/5
        based on <span itemprop="reviewCount">11</span> customer reviews
    </div>
 
    <div itemprop="offers" itemscope itemtype="http://schema.org/Offer">
        <span itemprop="price">$55.00</span>
        <link itemprop="availability" href="http://schema.org/InStock" />In stock
    </div>

    Product description:
    <span itemprop="description">0.7 cubic feet countertop microwave.
    Has six preset cooking categories and convenience features like
    Add-A-Minute and Child Lock.</span>
    
    Customer reviews:
    <div itemprop="review" itemscope itemtype="http://schema.org/Review">
        <span itemprop="name">Not a happy camper</span> -
        by <span itemprop="author">Ellie</span>,
        <meta itemprop="datePublished" content="2011-04-01">April 1, 2011
        <div itemprop="reviewRating" itemscope itemtype="http://schema.org/Rating">
            <meta itemprop="worstRating" content = "1">
            <span itemprop="ratingValue">1</span>/
            <span itemprop="bestRating">5</span>stars
        </div>
        <span itemprop="description">The lamp burned out and now I have to replace
        it. </span>
    </div>
    
    <div itemprop="review" itemscope itemtype="http://schema.org/Review">
        <span itemprop="name">Value purchase</span> -
        by <span itemprop="author">Lucas</span>,
        <meta itemprop="datePublished" content="2011-03-25">March 25, 2011
        <div itemprop="reviewRating" itemscope itemtype="http://schema.org/Rating">
            <meta itemprop="worstRating" content = "1"/>
            <span itemprop="ratingValue">4</span>/
            <span itemprop="bestRating">5</span>stars
        </div>
        <span itemprop="description">Great microwave for the price. It is small and
        fits in my apartment.</span>
    </div>
    ...
</div>
"""
sel = Selector(text=doc, type="html")
for scope in sel.xpath('//div[@itemscope]'):
    print("current scope:", scope.xpath('@itemtype').extract())
    props = scope.xpath('''
        set:difference(./descendant::*/@itemprop,
        .//*[@itemscope]/*/@itemprop)''')
    print("    properties:", props.extract())
# 在这里，我们首先迭代itemscope元素，
# 对于每个元素, 我们寻找所有itemprops元素，
# 并将那些本身排除在另一个元素之外的元素itemscope。

'''
注意//node[1]和(// node)[1]之间的区别
'''
# //node[1] 选择在其各自父母下首先出现的所有节点。
# (//node)[1] 选择文档中的所有节点，然后只获取其中的第一个节点。