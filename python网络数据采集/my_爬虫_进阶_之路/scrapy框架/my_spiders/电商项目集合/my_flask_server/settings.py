# coding:utf-8

'''
@author = super_fazai
@File    : settings.py
@Time    : 2017/10/22 10:07
@connect : superonesfazai@gmail.com
'''

import json

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
db_info_json_path
"""
# 自己电脑上
db_info_json_path = '/Users/afa/my_company_db_info.json'
# linux服务器
# db_info_json_path = '/root/my_company_db_info.json'

'''
taobao
'''
# 自己电脑
taobao_u_and_p_path = '/Users/afa/my_username_and_passwd.json'
# linux服务器
# taobao_u_and_p_path = '/root/my_username_and_passwd.json'

def get_u_and_p_info():
    try:
        with open(taobao_u_and_p_path, 'r') as f:
            _tmp = json.loads(f.readline())
    except FileNotFoundError:
        print('严重错误, 数据库初始配置json文件未找到!请检查!')
        return ('', '')
    except Exception as e:
        print('错误如下: ', e)
        return ('', '')

    return _tmp['taobao_username'], _tmp['taobao_passwd']

TAOBAO_USERNAME, TAOBAO_PASSWD = get_u_and_p_info()

# 避免登录弹窗
_tmall_cookies = 't=1a77751093aca97df6ff633d179a4153; _tb_token_=e3dfee4bb4eb3; cookie2=1d639cd1684a3541c57c553d6854615a; dnk=zy118; uc1=cookie21=V32FPkk%2Fgi8IDE%2FSq3xx&cookie15=VT5L2FSpMGV7TQ%3D%3D&cookie14=UoTePTIfvOsB5w%3D%3D; uc3=vt3=F8dBz4D6JuPl1o5Emq4%3D&id2=VW8dqnjNBhw%3D&nk2=GdFnyJY%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D; tracknick=zy118; _l_g_=Ug%3D%3D; unb=60387916; lgc=zy118; cookie1=B0Bahel1MMqhEHy5Lu5lvH1XHjVvXnxb65n13jIusnA%3D; login=true; cookie17=VW8dqnjNBhw%3D; _nk_=zy118; sg=869; csg=fe1c2ee8; ucn=unsz; _m_h5_tk=524e6b249bd8003b8d30d129494a7e03_1523702758043; _m_h5_tk_enc=8b107feac79bc4f6b98a3b2838e3913c; cna=xMFYEyS2NhQCAaQ0DFNuhw68; isg=BJycLPyHKn6hed6i9U6YY7ZsbbyOvUCEPiF1fHadrgdqwTxLniUQzxJzJSk5yXiX'

"""
日志文件目录
"""
# 自己电脑上
MY_SPIDER_LOGS_PATH = '/Users/afa/myFiles/my_spider_logs/电商项目'
# linux服务器
# MY_SPIDER_LOGS_PATH = '/root/myFiles/my_spider_logs/电商项目'

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
TAOBAO_SLEEP_TIME = 2     # 这个在服务器里面可以注释掉为.4s

'''
天猫requests间接请求时间
'''
TMALL_SLEEP_TIME = 2      # 这个在服务器里可以注释为.4s

'''
select.html的name
'''
SELECT_HTML_NAME = 'select.html'

'''
淘宝实时更新的sleep_time(接口请求限频,2秒以上比较保险)
'''
TAOBAO_REAL_TIMES_SLEEP_TIME = 2.      # 加拿大服务器可以设置为.4s

'''
天猫实时更新的sleep_time(接口请求限频,2秒以上比较保险)
'''
TMALL_REAL_TIMES_SLEEP_TIME = 2.2      # 加拿大服务器可以设置为.4s

'''
淘抢购抓取时间点设置
'''
TAOBAO_QIANGGOU_SPIDER_HOUR_LIST = ['10', '11', '12', '13', '14', '15', '17']

'''
折800 session_id相关
'''
BASE_SESSION_ID = 19910             # 起始session_id
MAX_SESSION_ID = 25000              # 截止的session_id
SPIDER_START_HOUR = 8               # 每日限时秒杀爬取的开始秒杀时间点
SPIDER_END_HOUR = 16                # 每日限时秒杀爬取的秒杀结束时间点
ZHE_800_SPIKE_SLEEP_TIME = 1.8       # 没抓取一个sleep time的时间,用于避免返回为空的情况
ZHE_800_PINTUAN_SLEEP_TIME = 2.0    # 折800拼团sleep_time

'''
蜜芽 base_number相关
'''
# MIA_BASE_NUMBER = 56000         # 起始的base_number
MIA_BASE_NUMBER = 61000         # 起始的base_number
MIA_MAX_NUMBER = 75000          # 截止的base_number
MIA_SPIKE_SLEEP_TIME = 1.8

'''
蘑菇街相关
'''
MOGUJIE_SLEEP_TIME = 1.8        # 间歇sleep时间

'''
拼多多
'''
PINDUODUO_SLEEP_TIME = 1.8      # sleep时间
PINDUODUO_MIAOSHA_SPIDER_HOUR_LIST = ['08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18']
# 秒杀时长只有30分钟的时间点list，其他时间区间都是1小时
PINDUODUO_MIAOSHA_BEGIN_HOUR_LIST = ['08', '09', '10', '14', '15', '19', '20', '21']

'''
楚楚街
'''
CHUCHUJIE_SLEEP_TIME = 1.8      # sleep时间

'''
唯品会
'''
VIP_SLEEP_TIME = 2            # sleep时间

'''
聚美优品
'''
JUMEIYOUPIN_SLEEP_TIME = 2    # sleep时间
# 下面是服务器最佳timeout 多次测试的结果
JUMEIYOUPIN_PINTUAN_API_TIMEOUT = 2       # 拼团单页面商品 异步抓取接口timeout
JUMEIYOUPIN_PINTUAN_GOODS_TIMEOUT = 3       # 拼团商品页面 异步抓取的timeout

'''
考拉
'''


"""
超级管理员账户名密码
"""
ADMIN_NAME = 'yiuxiu_admin'
ADMIN_PASSWD = 'yiuxiu_zy118!'

'''
basic_app_key
'''
BASIC_APP_KEY = 'yiuxiu6688'

import json

def get_db_info():
    try:
        with open(db_info_json_path, 'r') as f:
            _tmp = json.loads(f.readline())
    except FileNotFoundError:
        print('严重错误, 数据库初始配置json文件未找到!请检查!')
        return ('', '', '', '', 1433)
    except Exception as e:
        print('错误如下: ', e)
        return ('', '', '', '', 1433)

    return (_tmp['HOST'], _tmp['USER'], _tmp['PASSWORD'], _tmp['DATABASE'], _tmp['PORT'])

"""
数据库相关
"""
HOST, USER, PASSWORD, DATABASE, PORT = get_db_info()

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

INIT_PASSWD = 'aaatttyiuxiu'

"""
server
"""
# key 用于加密
key = 21
DEFAULT_USERNAME = '18698570079'

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
VIP_SPIDER_TO_SHOW_PATH = 'templates/vip_spider_to_show.html'
KAOLA_SPIDER_2_SHOW_PATH = 'templates/kaola_spider_2_show.html'
YANXUAN_SPIDER_2_SHOW_PATH = 'templates/yanxuan_spider_2_show.html'
YOUPIN_SPIDER_2_SHOW_PATH = 'templates/youpin_spider_2_show.html'

"""
headers
"""
PHONE_HEADERS = [
    'Mozilla/5.0 (iPhone 84; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14G60 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1',
    'Mozilla/5.0 (Linux; Android 7.0; STF-AL10 Build/HUAWEISTF-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.2.0_730_YYB_D QQ/7.2.0.3270 NetType/4G WebP/0.3.0 Pixel/1080',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en',
    'Mozilla/5.0 (Linux; Android 5.1.1; vivo Xplay5A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.3 baiduboxapp/9.3.0.10 (Baidu; P1 5.1.1)',
    'Mozilla/5.0 (Linux; Android 6.0; LEX626 Build/HEXCNFN5902606111S) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/7.4 baiduboxapp/8.3.1 (Baidu; P1 6.0)',
    'Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; ZUK Z2121 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.6.8.952 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; SM-C7000 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.6.2.948 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; MI 4S Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.1.3',
    'Mozilla/5.0 (Linux; Android 5.1; m3 note Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.3 baiduboxapp/9.3.0.10 (Baidu; P1 5.1)',
    'Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; SM-G9550 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.7.0.953 Mobile Safari/537.36',
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