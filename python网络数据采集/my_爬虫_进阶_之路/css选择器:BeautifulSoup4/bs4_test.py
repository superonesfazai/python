# coding = utf-8

'''
@author = super_fazai
@File    : bs4_test.py
@connect : superonesfazai@gmail.com
'''

from bs4 import BeautifulSoup

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

# 创建 Beautiful Soup 对象
# soup = BeautifulSoup(html)
soup = BeautifulSoup(html, 'lxml')  # 通过指明解析器从而不报自带的没指明解析器的错误

# 打开本地 HTML 文件的方式来创建对象
# soup = BeautifulSoup(open('index.html'))

# 格式化输出 soup 对象的内容
print(soup.prettify())

'''
运行结果中会有以下警告:
 UserWarning: No parser was explicitly specified, so I'm using the best available HTML parser for this system ("lxml"). This usually isn't a problem, but if you run this code on another system, or in a different virtual environment, it may use a different parser and behave differently.

The code that caused this warning is on line 25 of the file /Users/afa/myFiles/codeDoc/PythonDoc/python网络数据采集/用爬虫测试网站/css选择器:BeautifulSoup4/bs4_test.py. To get rid of this warning, change code that looks like this:

 BeautifulSoup(YOUR_MARKUP})

to this:

意思是，如果我们没有显式地指定解析器，所以默认使用这个系统的最佳可用HTML解析器(“lxml”)。
如果你在另一个系统中运行这段代码，或者在不同的虚拟环境中，使用不同的解析器造成行为不同

但是我们可以通过soup = BeautifulSoup(html,“lxml”)方式指定lxml解析器
'''