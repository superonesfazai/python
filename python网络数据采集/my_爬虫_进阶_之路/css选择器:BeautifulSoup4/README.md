## CSS 选择器：BeautifulSoup4
和 lxml 一样，Beautiful Soup 也是一个HTML/XML的解析器，主要的功能也是如何解析和提取 HTML/XML 数据
```html
lxml 只会局部遍历，而Beautiful Soup 是基于HTML DOM的，会载入整个文档，解析整个DOM树，因此时间和内存开销都会大很多，所以性能要低于lxml。

BeautifulSoup 用来解析 HTML 比较简单，API非常人性化，支持CSS选择器、Python标准库中的HTML解析器，也支持 lxml 的 XML解析器。

Beautiful Soup 3 目前已经停止开发，推荐现在的项目使用Beautiful Soup 4。使用 pip 安装即可：pip install beautifulsoup4

官方文档：http://beautifulsoup.readthedocs.io/zh_CN/v4.4.0
```
![](https://i.loli.net/2019/09/24/ocPIRdwhU8FrMN4.png)
```
注意：beautifulsoup还能把不规范的html文件进行规范化
```

## 四大对象种类
Beautiful Soup将复杂HTML文档转换成一个复杂的树形结构,每个节点都是Python对象,所有对象可以归纳为4种:
```html
* Tag
* NavigableString
* BeautifulSoup
* Comment
```
#### 1. Tag
Tag 通俗点讲就是 HTML 中的一个个标签，例如：
```html
<head><title>The Dormouse's story</title></head>
<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
```
上面的 title head a p等等 HTML 标签加上里面包括的内容就是 Tag
#### 2. NavigableString
既然我们已经得到了标签的内容，那么问题来了，我们要想获取标签内部的文字怎么办呢？很简单，用 .string 即可
#### 3. BeautifulSoup
BeautifulSoup 对象表示的是一个文档的内容。大部分时候,可以把它当作 Tag 对象，是一个特殊的 Tag，我们可以分别获取它的类型，名称，以及属性来感受一下
#### 4. Comment
Comment 对象是一个特殊类型的 NavigableString 对象，其输出的内容不包括注释符号。

## 遍历文档树
### 1. 直接子节点 ：.contents .children 属性
##### .content
```
tag 的 .content 属性可以将tag的子节点以列表的方式输出

输出方式为列表，我们可以用列表索引来获取它的某一个元素
```
##### .children
```
它返回的不是一个 list，不过我们可以通过遍历获取所有子节点。

我们打印输出 .children 看一下，可以发现它是一个 list 生成器对象
```
### 2. 所有子孙节点: .descendants属性
```
.contents 和 .children 属性仅包含tag的直接子节点，.descendants 属性可以对所有tag的子孙节点进行递归循环，和 children类似，我们也需要遍历获取其中的内容
```
### 3. 节点内容: .string 属性
如果tag只有一个 NavigableString 类型子节点,那么这个tag可以使用 .string 得到子节点。如果一个tag仅有一个子节点,那么这个tag也可以使用 .string 方法,输出结果与当前唯一子节点的 .string 结果相同。

通俗点说就是：如果一个标签里面没有标签了，那么 .string 就会返回标签里面的内容。如果标签里面只有唯一的一个标签了，那么 .string 也会返回最里面的内容

## 搜索文档树
### find_all(name, attrs, recursive, text, **kwargs)
#### 1）name 参数
```
name 参数可以查找所有名字为 name 的tag,字符串对象会被自动忽略掉
```
##### A.传字符串
```
最简单的过滤器是字符串.在搜索方法中传入一个字符串参数,Beautiful Soup会查找与字符串完整匹配的内容,
```
##### B.传正则表达式
```
如果传入正则表达式作为参数, Beautiful Soup会通过正则表达式的 match() 来匹配内容.
```
##### C.传列表
```
如果传入列表参数,Beautiful Soup会将与列表中任一元素匹配的内容返回
```
#### 2）keyword 参数
```python
soup.find_all(id='link2')
# [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]
```
#### 3）text 参数
```
通过 text 参数可以搜搜文档中的字符串内容，与 name 参数的可选值一样, text 参数接受 字符串 , 正则表达式 , 列表
```

## css选择器
```html
这就是另一种与 find_all 方法有异曲同工之妙的查找方法.
```
```html
* 写 CSS 时，标签名不加任何修饰，类名前加.，id名前加#

* 在这里我们也可以利用类似的方法来筛选元素，用到的方法是 soup.select()，返回类型是 list
```
### （1）通过标签名查找
```python
print soup.select('title') 
#[<title>The Dormouse's story</title>]

print soup.select('a')
#[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

print soup.select('b')
#[<b>The Dormouse's story</b>]
```
### （2）通过类名查找
```python
print soup.select('.sister')
#[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
```
### （3）通过 id 名查找
```python
print soup.select('#link1')
#[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
```
### （4）组合查找
组合查找即和写 class 文件时，标签名与类名、id名进行的组合原理是一样的，例如查找 p 标签中，id 等于 link1的内容，二者需要用空格分开

```python
print soup.select('p #link1')
#[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
```
直接子标签查找，则使用 > 分隔
```python
print soup.select("head > title")
#[<title>The Dormouse's story</title>]
```
### （5）属性查找
查找时还可以加入属性元素，属性需要用中括号括起来，注意属性和标签属于同一节点，所以中间不能加空格，否则会无法匹配到。

```python
print soup.select('a[class="sister"]')
#[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

print soup.select('a[href="http://example.com/elsie"]')
#[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
```
同样，属性仍然可以与上述查找方式组合，不在同一节点的空格隔开，同一节点的不加空格
```python
print soup.select('p a[href="http://example.com/elsie"]')
#[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
```
### (6) 获取内容
以上的 select 方法返回的结果都是列表形式，可以遍历形式输出，然后用 get_text() 方法来获取它的内容
```python
soup = BeautifulSoup(html, 'lxml')
print type(soup.select('title'))
print soup.select('title')[0].get_text()

for title in soup.select('title'):
    print title.get_text()
```


