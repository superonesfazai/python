# fz_ip_pool
*分布式并发可扩展的代理ip池*

旨在: 获取真实高匿可复用的免费proxy ip, 并且实时更新ip pool

## 架构
celery + redis + httpbin + spiders

## 依赖安装
```bash
$ pip3 install fzutils
```

## 本地安装proxy ip检测环境
- 安装前提: 机器的80端口对快开放(否则无需设置, 跳过)
```bash
# pull
$ docker pull kennethreitz/httpbin 
# 启动
$ docker run -p 80:80 kennethreitz/httpbin
# 修改settings.py
TEST_HTTP_HEADER = 'http://0.0.0.0:80/get'
# TEST_HTTP_HEADER = 'http://httpbin.org/get'
```

## ip_pools启动
#### 1. redis
- 安装redis
```bash
# mac
$ brew install redis
```
- 启动redis
```bash
# server
$ redis-server

# cli客户端
$ redis-cli 
```

#### 2. 运行proxy_spiders_tasks worker
- 单一worker
```bash
# info
$ celery -A proxy_tasks worker -l info
# debug
$ celery -A proxy_tasks worker -l debug
```
- worker多开(推荐)
```bash
$ celery multi start w1 w2 w3 w4 w5 -A proxy_tasks 
> Starting nodes...
	> w1@afahostdeiMac.local: OK
Stale pidfile exists - Removing it.
	> w2@afahostdeiMac.local: OK
Stale pidfile exists - Removing it.
	> w3@afahostdeiMac.local: OK
Stale pidfile exists - Removing it.
	> w4@afahostdeiMac.local: OK
Stale pidfile exists - Removing it.
	> w5@afahostdeiMac.local: OK
Stale pidfile exists - Removing it.
```
*开5个worker的网络并发状态*

![](./images/2.png)

#### 3. python3 main.py

## API demo
eg: api.py's IpPoolsObj class

## tasks状态监控
```bash
$ pip3 install flower
```
- 启动
```bash
$ celery -A proxy_tasks flower --address=127.0.0.1 --port=5555
$ open http://localhost:5555
```
![](images/12.png)

## Extendable
```python
# 设置代理抓取对象
parser_list = [
    # {
    #     'urls': 'https://www.kuaidaili.com/free/inha/{}',
    #     'charset': 'utf-8',
    #     'type': 'css',
    #     'part': 'div#list table tbody tr',
    #     'position': {
    #         'ip': 'td:nth-child(1)',
    #         'port': 'td:nth-child(2)',
    #         'ip_type': 'td:nth-child(4)',
    #     }
    # },
    {
        'urls': 'http://www.66ip.cn/{}.html',
        'charset': 'gb2312',
        'type': 'css',
        'part': 'div.containerbox table tr',
        'position': {
            'ip': 'td:nth-child(1)',
            'port': 'td:nth-child(2)',
            'ip_type': 'td:nth-child(4)',
        }
    },
    ...
]
```

## 版权和保修
此发行版中的代码为版权所有 (c) super_fazai, 除非另有明确说明.

fzutils根据MIT许可证提供, 包含的LICENSE文件详细描述了这一点.

## 贡献者
-  super_fazai

## 作者
super_fazai

<author_email: superonesfazai@gmail.com>

