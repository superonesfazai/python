```bash
███████╗███████╗██╗   ██╗████████╗██╗██╗     ███████╗
██╔════╝╚══███╔╝██║   ██║╚══██╔══╝██║██║     ██╔════╝
█████╗    ███╔╝ ██║   ██║   ██║   ██║██║     ███████╗
██╔══╝   ███╔╝  ██║   ██║   ██║   ██║██║     ╚════██║
██║     ███████╗╚██████╔╝   ██║   ██║███████╗███████║
╚═╝     ╚══════╝ ╚═════╝    ╚═╝   ╚═╝╚══════╝╚══════╝                                                   
```
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
from fzutils.ip_pools import MyIpPools

# 高匿
ip_obj = MyIpPools(high_conceal=True)
# 得到一个随机ip, eg: 'http://175.6.2.174:8088'
proxy = ip_obj._get_random_proxy_ip()
```
```python
from fzutils.spider.fz_phantomjs import MyPhantomjs

_ = MyPhantomjs(executable_path='xxx')
exec_code = '''
js = 'document.body.scrollTop=10000'
self.driver.execute_script(js) 
'''
body = _.use_phantomjs_to_get_url_body(url='xxx', exec_code=exec_code)
```
```python
from fzutils.spider.fz_requests import MyRequests

body = MyRequests.get_url_body(method='get', url='xxx')
```
```python
import asyncio
from fzutils.spider.fz_aiohttp import MyAiohttp

async def tmp():
    _ = MyAiohttp(max_tasks=5)
    return await _.aio_get_url_body(url='xxx')
```
```python
from fzutils.time_utils import (
    fz_set_timeout,
    fz_timer,)
from time import sleep
import sys

# 设置执行超时
@fz_set_timeout(2)
def tmp():
    sleep(3)

# 计算函数用时, 支持sys.stdout.write or logger.info
@fz_timer(print_func=sys.stdout.write)
def tmp_2():
    sleep(3)
    
tmp()
tmp_2()
```
```python
from fzutils.log_utils import set_logger
from logging import INFO, ERROR

logger = set_logger(log_file_name='path', console_log_level=INFO, file_log_level=ERROR)
```
```python
from fzutils.auto_ops_utils import auto_git

# 自动化git
auto_git(path='xxx/path')
```
```python
from fzutils.path_utils import cd

# cd 到目标上下文并进行其他操作
with cd('path'):
    pass
```
```python
from fzutils.sql_utils import (
    BaseSqlServer,
    pretty_table,)

_ = BaseSqlServer(host='host', user='user', passwd='passwd', db='db', port='port')
# db美化打印
pretty_table(
    cursor=_._get_one_select_cursor(
        sql_str='sql_str', 
        params=('some_thing',)))
```
```python
from fzutils.linux_utils import (
    kill_process_by_name,
    process_exit,)

# 根据process_name kill process
kill_process_by_name(process_name='xxxx')
# 根据process_name 判断process是否存在
process_exit(process_name='xxxx')
```
```python
from fzutils.linux_utils import daemon_init

def run_forever():
    pass

# 守护进程
daemon_init()
run_forever()
```
```python
from fzutils.internet_utils import (
    get_random_pc_ua,
    get_random_phone_ua,)

# 随机user-agent
pc_user_agent = get_random_pc_ua()
phone_user_agent = get_random_phone_ua()
```
```python
from fzutils.common_utils import _print

# 支持sys.stdout.write or logger
_print(msg='xxx', logger=logger, exception=e, log_level=2)
```
```python
from fzutils.auto_ops_utils import (
    upload_or_download_files,
    local_compress_folders,
    remote_decompress_folders,)
from fabric.connection import Connection

connect_obj = Connection()
# local 与 server端 上传或下载文件
upload_or_download_files(
    method='put',
    connect_object=connect_obj,
    local_file_path='/Users/afa/myFiles/tmp/my_spider_logs.zip',
    remote_file_path='/root/myFiles/my_spider_logs.zip'
)
# 本地解压zip文件
local_compress_folders(
    father_folders_path='/Users/afa/myFiles',
    folders_name='my_spider_logs',
    default_save_path='xxxxxx'
)
# 远程解压zip文件
remote_decompress_folders(
    connect_object=connect_obj,
    folders_path='/root/myFiles/my_spider_logs.zip',
    target_decompress_path='/root/myFiles/'
)
```
```python
from fzutils.common_utils import json_2_dict

# json转dict, 处理部分不规范json
_dict = json_2_dict(json_str='json_str', logger=logger, encoding='utf-8')
```
```python
from fzutils.auto_ops_utils import judge_whether_file_exists
from fabric.connection import Connection

connect_obj = Connection()
# 判断server文件是否存在
result = judge_whether_file_exists(connect_object=connect_obj, file_path='file_path')
```
```python
from fzutils.email_utils import FZEmail

_ = FZEmail(user='xxx', passwd='密码 or smtp授权码')
_.send_email(to=['xxx@gmail.com',], subject='邮件正文', text='邮件内容')
```
```python
from requests import sessions
from fzutils.common_utils import (
    save_obj,
    get_obj,)

s = sessions()
# 对象持久化存储
save_obj(s, 's.txt')
get_obj('s.txt')
```
```python
from fzutils.data.str_utils import (
    char_is_chinese,
    char_is_alphabet,
    char_is_number,
    char_is_other,)

# 单字符判断其类型
print(char_is_chinese('你'))
print(char_is_alphabet('a'))
print(char_is_number('1'))
print(char_is_other('_'))
```
```python
from fzutils.algorithm_utils import merge_sort

# 归并排序
print(merge_sort([-1, 2, 1]))
# 还有很多其他排序方法
```
```python
from fzutils.spider.auto import auto_generate_crawler_code

# 爬虫基本代码自动生成器
auto_generate_crawler_code()
"""
shell输出如下: 
#--------------------------------
# 爬虫模板自动生成器 by super_fazai
#--------------------------------
@@ 下面是备选参数, 无输入则取默认值!!
请输入author:super_fazai
请输入email:superonesfazai@gmail.com
请输入创建的文件名(不含.py):fz_spider_demo
请输入class_name:FZSpiderDemo

创建爬虫文件fz_spider_demo.py完毕!
enjoy!🍺
"""
```
```python
# 还有很多其他常用函数, 待您探索...
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

