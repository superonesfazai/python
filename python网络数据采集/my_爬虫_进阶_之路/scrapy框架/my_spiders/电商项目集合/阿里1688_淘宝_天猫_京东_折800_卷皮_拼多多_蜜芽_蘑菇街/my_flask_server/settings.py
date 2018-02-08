# coding:utf-8

'''
@author = super_fazai
@File    : settings.py
@Time    : 2017/10/22 10:07
@connect : superonesfazai@gmail.com
'''

"""
驱动相关设置
"""
# chrome驱动
CHROME_DRIVER_PATH = '/Users/afa/myFiles/tools/chromedriver'
# phantomjs驱动
PHANTOMJS_DRIVER_PATH = '/Users/afa/myFiles/tools/phantomjs-2.1.1-macosx/bin/phantomjs'

# 我自己服务器上的地址
# CHROME_DRIVER_PATH = '/root/myFiles/linux_drivers/chromedriver'
# PHANTOMJS_DRIVER_PATH = '/root/myFiles/linux_drivers/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'

"""
服务器运行端口
"""
SERVER_PORT = 5000

'''
是否为后台运行
'''
IS_BACKGROUND_RUNNING = False
# jd优选达人推荐
JD_YOUXUAN_DAREN_IS_BACKGROUND_RUNNING = False

'''
淘宝requests间接请求时间
'''
TAOBAO_SLEEP_TIME = 1.4     # 这个在服务器里面可以注释掉为.4s

'''
select.html的name
'''
SELECT_HTML_NAME = 'select.html'

'''
淘宝实时更新的sleep_time
'''
TAOBAO_REAL_TIMES_SLEEP_TIME = 1.8      # 加拿大服务器可以设置为.4s

'''
折800 session_id相关
'''
BASE_SESSION_ID = 15700         # 起始session_id
MAX_SESSION_ID = 19000          # 截止的session_id
SPIDER_START_HOUR = 8           # 每日限时秒杀爬取的开始秒杀时间点
SPIDER_END_HOUR = 16            # 每日限时秒杀爬取的秒杀结束时间点
ZHE_800_SPIKE_SLEEP_TIME = .7   # 没抓取一个sleep time的时间,用于避免返回为空的情况

'''
蜜芽 base_number相关
'''
MIA_BASE_NUMBER = 56000         # 起始的base_number
MIA_MAX_NUMBER = 75000          # 截止的base_number
MIA_SPIKE_SLEEP_TIME = 1.3

'''
蘑菇街相关
'''
MOGUJIE_SLEEP_TIME = 1.3        # 间歇sleep时间

'''
拼多多
'''
PINDUODUO_SLEEP_TIME = 1.4      # sleep时间
PINDUODUO_MIAOSHA_SPIDER_HOUR_LIST = ['08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18']
# 秒杀时长只有30分钟的时间点list，其他时间区间都是1小时
PINDUODUO_MIAOSHA_BEGIN_HOUR_LIST = ['08', '09', '10', '14', '15', '19', '20', '21']

"""
超级管理员账户名密码
"""
ADMIN_NAME = 'yiuxiu_admin'
ADMIN_PASSWD = 'yiuxiu_zy118!'

'''
basic_app_key
'''
BASIC_APP_KEY = 'yiuxiu6688'

"""
数据库相关
"""
# sql_server服务器地址
HOST = '120.26.142.189'
# 用户名
USER = 'caiji2'
# 密码
PASSWORD = 'zy118ZY118'
# 数据库名称
DATABASE = 'Gather'
# 端口号
PORT = 1433

# sql_server服务器地址
HOST_2 = ''
# 用户名
USER_2 = ''
# 密码
PASSWORD_2 = ''
# 数据库名称
DATABASE_2 = ''
# 端口号
PORT_2 = 1433

INIT_PASSWD = 'zy118zy118'

"""
保存的对应cookies文件路径
"""
# linux/mac环境的路径
ALI_1688_COOKIES_FILE_PATH = './cookies/cookies_ali_1688.txt'
TAOBAO_COOKIES_FILE_PATH = './cookies/cookies_taobao.txt'

"""
spider_to_show.html页面path
"""
# linux/mac
ALi_SPIDER_TO_SHOW_PATH = 'templates/ali_spider_to_show.html'
TAOBAO_SPIDER_TO_SHWO_PATH = 'templates/taobao_spider_to_show.html'
TMALL_SPIDER_TO_SHOW_PATH = 'templates/tmall_spider_to_show.html'
JD_SPIDER_TO_SHOW_PATH = 'templates/jd_spider_to_show.html'
ZHE_800_SPIDER_TO_SHOW_PATH = 'templates/zhe_800_spider_to_show.html'
JUANPI_SPIDER_TO_SHOW_PATH = 'templates/juanpi_spider_to_show.html'
PINDUODUO_SPIDER_TO_SHOW_PATH = 'templates/pinduoduo_spider_to_show.html'

"""
headers
"""
HEADERS = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Linux i686; U; en; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 10.51",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12",
    "Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.302.2 Safari/532.8",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.15 Safari/534.13",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Macintosh; U; Mac OS X Mach-O; en-US; rv:2.0a) Gecko/20040614 Firefox/3.0.0 ",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.0.3) Gecko/2008092414 Firefox/3.0.3",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
]

"""
error_html_code(用于处理: 未登录时进行的非法操作)
"""
ERROR_HTML_CODE = '''
<html><header></header><body>非法操作!请返回登录页面登录后继续相关操作<a href="/"></br></br>返回登录页面</a></body></html>
'''

'''
cookies
'''
SINA_COOKIES = 'SINAGLOBAL=1779567549215.5193.1513216238889; un=jc09893445wei@163.com; wvr=6; _s_tentry=login.sina.com.cn; Apache=3819054165673.079.1517320350816; ULV=1517320352333:12:10:4:3819054165673.079.1517320350816:1517281650841; SSOLoginState=1517366105; UOR=www.vaikan.com,widget.weibo.com,blog.csdn.net; YF-V5-G0=c998e7c570da2f8537944063e27af755; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFnCUfIwQh3Usm8xNPAMySy5JpX5KMhUgL.FoqpSoBR1hBNeKM2dJLoIEQLxKML1K-L1h-LxK-LB.qLB-zLxKML1-zLB.eLxKqL1-eL1-ikSozReoqt; ALF=1549000397; SCF=AgK0RDOKrRIOKXzub_Q00Rdmdq_Mtnap4wCdEu4VKbiFXx2qc85MqiD2K4BTDt-BE_omFvqzJtoqNlXuEhr1qiQ.; SUB=_2A253dtsNDeThGeBP7VYZ-CrLyjuIHXVUAkvFrDV8PUNbmtANLWHWkW9NRVESwyfYtEROP7KKUqmnXOnIxmP81tQN; SUHB=0y0JQ5fsI56HNq; wb_cusLike_6164884717=N'