# coding:utf-8

'''
@author = super_fazai
@File    : demo_2.py
@Time    : 2018/3/22 22:36
@connect : superonesfazai@gmail.com
'''

"""
大文件下载

比如视频等. requests 能让你下一点, 保存一点, 
而不是要全部下载完才能保存去另外的地方. 这就是一个 chunk 一个 chunk 的下载. 
使用 r.iter_content(chunk_size) 来控制每个 chunk 的大小 
然后在文件中写入这个 chunk 大小的数据.
"""

import requests

image_url = 'https://avatars3.githubusercontent.com/u/23206773?s=460&v=4'

r = requests.get(image_url, stream=True)    # stream loading
with open('./images/image_2.png', 'wb') as f:
    for chunk in r.iter_content(chunk_size=32):
        f.write(chunk)