# coding = utf-8

'''
@author = super_fazai
@File    : urllib_urlencode.py
@Time    : 2017/8/27 20:45
@connect : superonesfazai@gmail.com
'''

"""
python 2中 urllib 提供 urlencode 方法用来GET查询字符串的产生
python 中 urllib.parse 提供urlencode()进行编码查询
"""

# urllib 和 urllib2 都是接受URL请求的相关模块，
# 但是提供了不同的功能。两个最显著的不同如下:
'''
    * urllib 仅可以接受URL，不能创建 设置了headers 的Request 类实例；

    * 但是 urllib 提供 urlencode 方法用来GET查询字符串的产生，
      而 urllib2 则没有。(这是 urllib 和 urllib2 经常一起使用的主要原因）

    * 编码工作使用urllib的urlencode()函数，帮我们将key:value这样的键值对转换成"key=value"这样的字符串，解码工作可以使用urllib的unquote()函数。（注意，不是urllib2.urlencode() )
'''
import urllib.parse

word = {
    'wd': 'xxxx'
}

tmp = urllib.parse.urlencode(word)
print(tmp)
print(urllib.parse.unquote(tmp))

'''
一般HTTP请求提交数据，需要编码成 URL编码格式，
然后做为url的一部分，或者作为参数传到Request对象中
'''