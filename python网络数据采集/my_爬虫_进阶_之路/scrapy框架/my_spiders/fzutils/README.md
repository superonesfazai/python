[![Build Status](https://travis-ci.org/EasyWeChat/site.svg?branch=master)](https://github.com/superonesfazai/fzutils)
[![GitHub license](https://img.shields.io/github/license/superonesfazai/fzutils.svg)](https://github.com/superonesfazai/fzutils/blob/master/LICENSE.txt)
[![GitHub forks](https://img.shields.io/github/forks/superonesfazai/fzutils.svg)](https://github.com/superonesfazai/fzutils/network)
[![GitHub stars](https://img.shields.io/github/stars/superonesfazai/fzutils.svg)](https://github.com/superonesfazai/fzutils/stargazers)
![](https://img.shields.io/github/issues/superonesfazai/fzutils.svg)
[![Twitter](https://img.shields.io/twitter/url/https/github.com/superonesfazai/fzutils.svg?style=social)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Fsuperonesfazai%2Ffzutils)

# fzutils

## 这是什么?
这是fz的python utils包, for Spider.

## Install
```bash
pip3 install fzutils
```

## 要求
-  Python 3或更高版本.
-  依靠的代理池是IPProxyPool < https://github.com/qiyeboy/IPProxyPool >

## simple use
```bash
$ cd xxx/IPProxyPool && python3 IPProxy.py
```
```python
from fzutils.spider.fz_phantomjs import MyPhantomjs

_ = MyPhantomjs(executable_path='xxx')
_.use_phantomjs_to_get_url_body(url='xxx', exec_code='xxx')

import asyncio
from fzutils.spider.fz_aiohttp import MyAiohttp

async def tmp():
    _ = MyAiohttp()
    return await _.aio_get_url_body(url='xxx')

from fzutils.spider.fz_requests import MyRequests
_ = MyRequests()
_.get_url_body(method='get', url='xxx')

# 还有很多其他常用函数, 待您探索...
from fzutils.time_utils import fz_set_timeout
from time import sleep

# 设置执行超时
@fz_set_timeout(2)
def tmp():
    sleep(3)
tmp()
    
```

## 资源
fzutils的home < https://www.github.com/superonesfazai/python >

## 版权和保修
此发行版中的代码为版权所有 (c) super_fazai, 除非另有明确说明.

fzutils根据MIT许可证提供, 包含的LICENSE文件详细描述了这一点.

## 贡献者
-  super_fazai

## 作者
super_fazai

<author_email: superonesfazai@gmail.com>
