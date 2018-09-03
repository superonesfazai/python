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

# ip池最大代理数
MAX_PROXY_NUM = 500

# 检索剩余ip数量的sleep time 单位秒
WAIT_TIME = 6

# 检测proxy时超时设置
CHECK_PROXY_TIMEOUT = 5

# 存储proxy_list的key 的name
proxy_list_key_name = 'proxy_tasks'
# 存储高匿名可用的redis key name
high_proxy_list_key_name = 'h_proxy_list'

# 测试地址
TEST_URL = 'http://ip111.cn'
TEST_IP = 'http://httpbin.org/ip'
TEST_HTTP_HEADER = 'http://httpbin.org/get'
TEST_HTTPS_HEADER = 'https://httpbin.org/get'
# 现在使用检测的网址是httpbin.org, 但是即使ip通过了验证和检测
# ** 也只能说明通过此代理ip可以到达httpbin.org, 但是不一定能到达用户爬取的网址

# 可扩展的代理抓取对象
parser_list = [
    {
        'urls': ['https://www.kuaidaili.com/free/inha/{}'.format(page_num) for page_num in range(1, 101)],
        'charset': 'utf-8',
        'type': 'css',
        'part': 'div#list table tbody tr',
        'position': {
            'ip': 'td:nth-child(1)',
            'port': 'td:nth-child(2)',
            'ip_type': 'td:nth-child(4)',
        }
    },
    # {
    #     'urls': ['http://www.66ip.cn/{}.html'.format(page_num)for page_num in ['index'] + list(range(2, 12))],
    #     'charset': 'gb2312',
    #     'type': 'css',
    #     'part': 'div.containerbox table tr',
    #     'position': {
    #         'ip': 'td:nth-child(1)',
    #         'port': 'td:nth-child(2)',
    #         'ip_type': 'td:nth-child(4)',
    #     }
    # },
]