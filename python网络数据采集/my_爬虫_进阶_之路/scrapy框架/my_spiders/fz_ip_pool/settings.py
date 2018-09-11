# coding:utf-8

'''
@author = super_fazai
@File    : settings.py
@connect : superonesfazai@gmail.com
'''

"""
请根据需求进行相应修改
"""

# 日志存储路径
SPIDER_LOG_PATH = '/Users/afa/myFiles/my_spider_logs/fz_ip_pool/'

# 匿名度未知的ip池最大代理数
MAX_PROXY_NUM = 500

# 检索剩余ip数量的sleep time 单位秒
WAIT_TIME = 10

# 检测proxy时超时设置
CHECK_PROXY_TIMEOUT = 7

# 存储proxy_list的key 的name
proxy_list_key_name = 'proxy_tasks'
# 存储高匿名可用的redis key name
high_proxy_list_key_name = 'h_proxy_list'

# 高匿proxy低于以下分数就删除, 默认100
MIN_SCORE = 60

# 测试地址
TEST_URL = 'http://ip111.cn'
TEST_IP = 'http://httpbin.org/ip'
# TEST_HTTP_HEADER = 'http://0.0.0.0:80/get'
TEST_HTTP_HEADER = 'http://httpbin.org/get'
REMOTE_TEST_HTTPS_HEADER = 'https://httpbin.org/get'
# 现在使用检测的网址是httpbin.org, 但是即使ip通过了验证和检测
# ** 也只能说明通过此代理ip可以到达httpbin.org, 但是不一定能到达用户爬取的网址

# 可扩展的代理抓取对象
parser_list = [
    {
        'urls': 'http://www.66ip.cn/{}.html',
        'charset': 'gb2312',
        'type': 'css',
        'part': 'div.containerbox table tr',
        'position': {
            'ip': 'td:nth-child(1)',
            'port': 'td:nth-child(2)',
            'ip_type': 'td:nth-child(4)',
        },
        'page_range': {
            'min': 1,       # 最小页码
            'max': 1300,    # 最大页码
        }
    },
    {
        'urls': 'http://www.mimiip.com/gngao/{}',
        'charset': 'utf-8',
        'type': 'css',
        'part': 'div.content table.list tr',
        'position': {
            'ip': 'td:nth-child(1)',
            'port': 'td:nth-child(2)',
            'ip_type': 'td:nth-child(5)',
        },
        'page_range': {
            'min': 1,
            'max': 680,
        }
    },
    {
        'urls': 'http://www.ip3366.net/?stype=1&page={}',
        'charset': 'gb2312',
        'type': 'css',
        'part': 'div#list tbody tr',
        'position': {
            'ip': 'td:nth-child(1)',
            'port': 'td:nth-child(2)',
            'ip_type': 'td:nth-child(4)',
        },
        'page_range': {
            'min': 1,
            'max': 100,
        }
    },
    {
        'urls': 'http://www.data5u.com/free/gngn/index{}.shtml',
        'charset': 'utf-8',
        'type': 'css',
        'part': 'div.wlist ul.l2',
        'position': {
            'ip': 'span:nth-child(1) li:nth-child(1)',
            'port': 'span:nth-child(2) li:nth-child(1)',
            'ip_type': 'span:nth-child(4) li:nth-child(1)',
        },
        'page_range': {
            'min': 1,
            'max': 100,
        }
    },
    {
        'urls': 'http://ip.jiangxianli.com/?page={}',
        'charset': 'utf-8',
        'type': 'css',
        'part': 'table tr',
        'position': {
            'ip': 'td:nth-child(2)',
            'port': 'td:nth-child(3)',
            'ip_type': 'td:nth-child(5)',
        },
        'page_range': {
            'min': 1,
            'max': 26,
        }
    },

    # 下面为弃用代理
    # {   # 西刺代理可用质量过低, 弃用
    #     'urls': 'http://www.xicidaili.com/nn/{}',
    #     'charset': 'utf-8',
    #     'type': 'css',
    #     'part': 'table#ip_list tr',
    #     'position': {
    #         'ip': 'td:nth-child(2)',
    #         'port': 'td:nth-child(3)',
    #         'ip_type': 'td:nth-child(6)',
    #     },
    # }
    # {
    #     'urls': 'https://www.kuaidaili.com/free/inha/{}',
    #     'charset': 'utf-8',
    #     'type': 'css',
    #     'part': 'div#list table tbody tr',
    #     'position': {
    #         'ip': 'td:nth-child(1)',
    #         'port': 'td:nth-child(2)',
    #         'ip_type': 'td:nth-child(4)',
    #     },
    # },
]