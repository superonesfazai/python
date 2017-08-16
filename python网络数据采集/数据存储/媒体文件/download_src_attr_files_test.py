#coding:utf-8
__author__ = 'super_fazai'


# 下面的程序会把 http://pythonscraping.com 主页上所有 src 属性的文件都下载下来
# 程序运行注意事项
'''
你知道从网上下载未知文件的那些警告吗?这个程序会把页面上所有的文件
下载到你的硬盘里,可能会包含一些 bash 脚本、.exe 文件系统,甚至可能是恶意
软件(malware)。
如果你之前从没有运行过任何下载到电脑里的文件,电脑就是安全的吗?尤
其是当你用管理员权限运行这个程序时,你的电脑基本已经处于危险之中。
如果你执行了网页上的一个文件,那个文件把自己传送到了 ../../../../usr/bin/
python 里面,会发生什么呢?等下一次你再运行 Python 程序时,你的电脑
就可能会安装恶意软件。
这个程序只是为了演示;请不要随意运行它,因为这里没有对所有下载文件
的类型进行检查,也不应该用管理员权限运行它。记得经常备份重要的文
件,不要在硬盘上存储敏感信息,小心驶得万年船。
'''

'''
这个程序首先使用 Lambda 函数选择首页上所有带 src 属性的标签。
然后对 URL 链接进行清理和标准化,获得文件的绝对路径(而且去掉了外链)。
最后,每个文件都会下载到程序所在文件夹的 downloaded 文件里
这里 Python 的 os 模块用来获取每个下载文件的目标文件夹,建立完整的路径
'''

import os
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup

download_directory = 'downloaded'
base_url = 'http://pythonscraping.com'

def get_absolute_url(base_url, source):
    if source.startswith('http://www.'):
        url = 'http://' + source[11:]
    elif source.startswith('http://'):
        url = source
    elif source.startswith('www.'):
        url = source[4:]
        url = 'http://' + source
    else:
        url = base_url + '/' + source
    if base_url not in url:
        return None
    return url

def get_download_path(base_url, absolute_url, download_directory):
    path = absolute_url.replace('www', '')
    path = path.replace(base_url, '')
    path = download_directory + path
    directory = os.path.dirname(path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    return path

html = urlopen("http://www.pythonscraping.com")
bs_obj = BeautifulSoup(html)
download_list = bs_obj.findAll(src=True)
for download in download_list:
    file_url = get_absolute_url(base_url, download["src"])
    if file_url is not None:
        print(file_url)
urlretrieve(file_url, get_download_path(base_url, file_url, download_directory))

