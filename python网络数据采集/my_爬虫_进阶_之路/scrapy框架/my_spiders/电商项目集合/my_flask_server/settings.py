# coding:utf-8

'''
@author = super_fazai
@File    : settings.py
@Time    : 2017/10/22 10:07
@connect : superonesfazai@gmail.com
'''

from json import loads
from fzutils.ip_pools import (
    fz_ip_pool,
    ip_proxy_pool,
    tri_ip_pool,)
from fzutils.linux_utils import get_system_type
from fzutils.spider.fz_driver import (
    PHANTOMJS,
    PHONE,)

SYSTEM_TYPE = get_system_type()

"""
服务器运行端口
"""
SERVER_PORT = 5000

if SYSTEM_TYPE == 'Darwin':
    """
    驱动相关设置
    """
    CHROME_DRIVER_PATH = '/Users/afa/myFiles/tools/chromedriver'
    PHANTOMJS_DRIVER_PATH = '/Users/afa/myFiles/tools/phantomjs-2.1.1-macosx/bin/phantomjs'
    FIREFOX_DRIVER_PATH = '/Users/afa/myFiles/tools/geckodriver'

    """
    ip_pool_type: 使用的ip_pool类型
    """
    IP_POOL_TYPE = tri_ip_pool
    """
    db_info_json_path
    """
    db_info_json_path = '/Users/afa/my_company_db_info.json'
    '''
    taobao
    '''
    taobao_u_and_p_path = '/Users/afa/my_username_and_passwd.json'
    """
    日志文件目录
    """
    MY_SPIDER_LOGS_PATH = '/Users/afa/myFiles/my_spider_logs/电商项目'
    """
    是否为后台运行
    """
    IS_BACKGROUND_RUNNING = False

else:
    # server
    CHROME_DRIVER_PATH = '/root/myFiles/linux_drivers/chromedriver'
    PHANTOMJS_DRIVER_PATH = '/root/myFiles/linux_drivers/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'
    FIREFOX_DRIVER_PATH = '/root/myFiles/linux_drivers/geckodriver'
    IP_POOL_TYPE = tri_ip_pool
    db_info_json_path = '/root/my_company_db_info.json'
    taobao_u_and_p_path = '/root/my_username_and_passwd.json'
    MY_SPIDER_LOGS_PATH = '/root/myFiles/my_spider_logs/电商项目'
    IS_BACKGROUND_RUNNING = True

"""
zwm
"""
ZWM_PWD_PATH = '/Users/afa/myFiles/pwd/zwm_pwd.json'

"""
taobao
"""
def get_u_and_p_info():
    try:
        with open(taobao_u_and_p_path, 'r') as f:
            _tmp = loads(f.readline())
    except FileNotFoundError:
        print('严重错误, 数据库初始配置json文件未找到!请检查!')
        return ('', '')
    except Exception as e:
        print('错误如下: ', e)
        return ('', '')

    return _tmp['taobao_username'], _tmp['taobao_passwd']

TAOBAO_USERNAME, TAOBAO_PASSWD = get_u_and_p_info()

TB_COOKIES = ''
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
BASE_SESSION_ID = 25514             # 起始session_id
MAX_SESSION_ID = 32000              # 截止的session_id
SPIDER_START_HOUR = 8               # 每日限时秒杀爬取的开始秒杀时间点
SPIDER_END_HOUR = 16                # 每日限时秒杀爬取的秒杀结束时间点
ZHE_800_SPIKE_SLEEP_TIME = 1.8       # 没抓取一个sleep time的时间,用于避免返回为空的情况
ZHE_800_PINTUAN_SLEEP_TIME = 2.0    # 折800拼团sleep_time

'''
蜜芽 base_number相关
'''
MIA_BASE_NUMBER = 79710         # 起始的base_number
MIA_MAX_NUMBER = 85000          # 截止的base_number
MIA_SPIKE_SLEEP_TIME = 1.8

'''
蘑菇街相关
'''
MOGUJIE_SLEEP_TIME = 2.        # 间歇sleep时间

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

def get_db_info():
    try:
        with open(db_info_json_path, 'r') as f:
            _tmp = loads(f.readline())
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
MIA_SPIDER_2_SHOW_PATH = 'templates/mia_spider_2_show.html'

"""
error_html_code(用于处理: 未登录时进行的非法操作)
"""
ERROR_HTML_CODE = '''
<html><header></header><body>非法操作!请返回登录页面登录后继续相关操作<a href="/"></br></br>返回登录页面</a></body></html>
'''

'''
文章资讯可扩展抽取
'''
ARTICLE_ITEM_LIST = [
    {
        'short_name': 'wx',
        'debug': True,
        'obj_origin': 'mp.weixin.qq.com',
        'article_id': None,
        'title': {
            'method': 'css',
            'selector': 'div#img-content h2 ::text',
        },
        'video_title': None,
        'author': {
            'method': 'css',
            'selector': 'div#meta_content span a ::text',
        },
        'head_url': {
            'method': 're',
            'selector': 'var ori_head_img_url = \"(.*?)\";',
        },
        'create_time': {
            'method': 're',
            'selector': 'var publish_time = \"(.*?)\" ',
        },
        'content': {
            'method': 'css',
            'selector': 'div.rich_media_content',
        },
        'comment_num': None,
        'fav_num': None,
        'praise_num': None,
        'tags_list': None,
        'profile': None,
    },
    {
        'short_name': 'tt',
        'debug': True,
        'obj_origin': 'www.toutiao.com',
        'article_id': {
            'method': 're',
            'selector': 'www\.toutiao\.com/(\w+)/',
        },
        'title': {
            'method': 're',
            'selector': 'title: \'(.*?)\'\.slice\(6, -6\),',
        },
        'video_title': None,
        'author': {
            'method': 're',
            'selector': 'name: \'(.*?)\',avatar:',
        },
        'head_url': {
            'method': 're',
            'selector': 'avatar: \'(.*?)\',openUrl:',
        },
        'create_time': {
            'method': 're',
            'selector': 'time: \'(.*?)\'',
        },
        'content': {
            'method': 're',
            'selector': 'content: \'(.*)\'\.slice\(6, -6\),groupId',
        },
        'comment_num': {
            'method': 're',
            'selector': 'comments_count: (\d+),',
        },
        'tags_list': {
            'method': 're',
            'selector': '{\"name\":\"(.*?)\"}',
        },
        'fav_num': None,
        'praise_num': None,
        'profile': None,
    },
    {
        'short_name': 'js',
        'debug': True,
        'obj_origin': 'www.jianshu.com',
        'article_id': {
            'method': 're',
            'selector': 'www\.jianshu\.com/p/(\w+)',
        },
        'title': {
            'method': 'css',
            'selector': 'h1.title ::text',
        },
        'video_title': None,
        'author': {
            'method': 'css',
            'selector': 'div.author div.info span.name a ::text',
        },
        'head_url': {
            'method': 'css',
            'selector': 'div.author a img ::attr("src")',               # 'https:' + xxx
        },
        'create_time': {
            'method': 'css',
            'selector': 'span.publish-time ::text',
        },
        'content': {
            'method': 'css',
            'selector': 'div.show-content',
        },
        'comment_num': {
            'method': 're',
            'selector': '\"comments_count\":(\d+),',
        },
        # 'tags_list': {
        #     'method': 'css',
        #     'selector': 'div.include-collection div.name ::text',       # extract()
        # },
        'tags_list': None,                                              # 可以获取即通过driver得到完整html, 此处不获取
        'praise_num': {
            'method': 're',
            'selector': '\"likes_count\":(\d+),',
        },
        # 'profile': {
        #     'method': 'css',
        #     'selector': 'div.signature ::text',
        # },
        'profile': None,                                                # driver才可获取，此处不获取
        'fav_num': None,
    },
    {
        'short_name': 'kd',
        'debug': True,
        'obj_origin': 'post.mp.qq.com',
        'article_id': {
            'method': 're',
            'selector': 'article_id=(\d+)',
        },
        'title': {
            'method': 're',
            'selector': 'data-article-title=\"(.*?)\"',
        },
        'video_title': {
            'method': 're',
            'selector': 'data-article-title=\"(.*?)\"',
        },
        'author': {
            'method': 're',
            'selector': 'data-mp-name=\"(.*?)\"',
        },
        'video_author': {
            'method': 're',
            'selector': 'data-mp-name=\"(.*?)\"',
        },
        'head_url': {
            'method': 're',
            'selector': 'data-mp-icon=\"(.*?)\"',               # 'https:' + xxx
        },
        'video_head_url': {
            'method': 're',
            'selector': 'data-mp-icon=\"(.*?)\"',               # 'https:' + xxx
        },
        'create_time': {
            'method': 're',
            'selector': 'data-timestamp=\"(\d+)\"',
        },
        'video_create_time': {
            'method': 're',
            'selector': 'data-timestamp=\"(\d+)\"',
        },
        'content': {
            'method': 'css',
            'selector': 'div#main-content',
        },
        'video_article_content': None,
        'comment_num': None,
        'tags_list': {
            'method': 're',
            'selector': 'data-tags=\"(.*?)\"',       # '军舰,海军,舰艇,扫雷舰,水雷,地雷'
        },
        'video_tags_list': {
            'method': 're',
            'selector': 'data-tags=\"(.*?)\"',       # '军舰,海军,舰艇,扫雷舰,水雷,地雷'
        },
        'praise_num': None,
        'profile': {
            'method': 're',
            'selector': 'data-mp-desc=\"(.*?)\"',
        },                                                # driver才可获取，此处不获取
        'fav_num': None,
    },
    {
        'short_name': 'kb',
        'debug': True,
        'obj_origin': 'kuaibao.qq.com',
        'article_id': {
            'method': 're',
            'selector': 'omgid=(\w+)',
        },
        'article_id2': {
            'method': 're',
            'selector': '/s/(\w+)\?',
        },
        'title': {
            'method': 're',
            'selector': '\'title\': \'(.*?)\',',
        },
        'video_title': {
            'method': 'css',
            'selector': 'article.video-art div.video-title-container h1 ::text',
        },
        'video_title2': {
            'method': 'css',
            'selector': 'div.main-title ::text',
        },
        'video_title3': {
            'method': 'css',
            'selector': 'h1.video-title ::text',
        },
        'author': {
            'method': 're',
            'selector': '\'src\': \'(.*?)\'',
        },
        'video_author': {
            'method': 'css',
            'selector': 'article.media-art h1 ::text',
        },
        'video_author2': {
            'method': 'css',
            'selector': 'div.media-name ::text',
        },
        'video_author3': {
            'method': 'css',
            'selector': 'h1.channel-name ::text',
        },
        'head_url': {
            'method': 'css',
            'selector': 'div.artinfo div.img-wrap img ::attr("src")',               # 'https:' + xxx
        },
        'video_head_url': {
            'method': 'css',
            'selector': 'div.media-img img ::attr("src")',
        },
        'video_head_url2': {
            'method': 'css',
            'selector': 'div.media-icon-wrapper img ::attr("src")',
        },
        'create_time': {
            'method': 'css',
            'selector': 'div.artinfo span.time ::text',
        },
        'content': {
            'method': 'css',
            'selector': 'div.content-box',
        },
        'video_article_content': {
            'method': 'css',
            'selector': 'txpdiv.txp_video_container video',
        },
        'comment_num': None,
        'tags_list': None,
        'praise_num': None,
        'profile': None,
        'fav_num': None,
    },
    {
        'short_name': 'df',
        'debug': True,
        'obj_origin': 'toutiao.eastday.com',
        'article_id': {
            'method': 're',
            'selector': '/(\d+)\.html',
        },
        'title': {
            'method': 'css',
            'selector': 'h1.title ::text',
        },
        'video_title': {
            'method': 'css',
            'selector': 'div.video-title h1 ::text',
        },
        'author': {
            'method': 're',
            'selector': '&nbsp;来源：(.*?)</span>',
        },
        'head_url': None,
        'create_time': {
            'method': 're',
            'selector': '<div class=\"article-src-time\"><span class=\"src\">(\d+-\d+-\d+ \d+:\d+)&nbsp;&nbsp;&nbsp;&nbsp;来源',
        },
        'content': {
            'method': 'css',
            'selector': 'div#content',
        },
        'comment_num': None,
        'tags_list': None,
        'praise_num': None,
        'profile': None,
        'fav_num': None,
    },
    {
        'short_name': 'sg',
        'debug': True,
        'obj_origin': 'sa.sogou.com',
        'article_id': None,
        'title': {
            'method': 'css',
            'selector': 'h1#articleTitle ::text',
        },
        'video_title': {
            'method': 'css',
            'selector': 'h1.trans-video-tit ::text',
        },
        'author': {
            'method': 'css',
            'selector': 'p.w-from span:nth-child(1) ::text',
        },
        'video_author': {
            'method': 'css',
            'selector': 'div.trans-video-mes span:nth-child(1) ::text',
        },
        'head_url': None,
        'create_time': {
            'method': 'css',
            'selector': 'p.w-from span ::text',
        },
        'video_create_time': {
            'method': 'css',
            'selector': 'div.trans-video-mes span:nth-child(2) ::text',
        },
        'content': {
            'method': 'css',
            'selector': 'div#articleContent',
        },
        'comment_num': None,
        'tags_list': None,
        'praise_num': None,
        'profile': None,
        'fav_num': None,
    },
    {
        'short_name': 'bd',
        'debug': True,
        'obj_origin': 'm.baidu.com',
        'article_id': {
            'method': 're',
            'selector': 'news_(\d+)',
        },
        'video_id': {
            'method': 're',
            'selector': 'vid%253D(\d+)',
        },
        'video_id2': {
            'method': 're',
            'selector': 'sv_(\d+)',
        },
        'title': {
            'method': 'css',
            'selector': 'h1.titleSize ::text',
        },
        'video_title': {
            'method': 'css',
            'selector': 'h1.c-title ::text',
        },
        'author': {
            'method': 'css',
            'selector': 'div.extraInfo a.authorName ::text',
        },
        'video_author': {
            'method': 'css',
            'selector': 'span.name-text ::text'
        },
        'head_url': {
            'method': 'css',
            'selector': 'a.borderLine img ::attr("src")',
        },
        'create_time': {
            'method': 're',
            'selector': '\"updatetime\":(.*?),',
        },
        'video_create_time': None,
        'content': {
            'method': 'css',
            'selector': 'div.mainContent',
        },
        'comment_num': None,
        'tags_list': {
            'method': 're',
            'selector': '},\"tag\":(.*?)],'
        },
        'praise_num': None,
        'profile': None,
        'fav_num': None,
    },
    {
        'short_name': 'zq',
        'debug': True,
        'obj_origin': 'focus.youth.cn',
        'article_id': {
            'method': 're',
            'selector': '\/detail\/id\/(\d+)',
        },
        'title': {
            'method': 'css',
            'selector': 'h2.rich_media_title ::text',
        },
        'video_title': None,
        'author': {
            'method': 'css',
            'selector': 'div.rich_media_meta_list a.laiyuan ::text',
        },
        'video_author': None,
        'head_url': None,
        'create_time': {
            'method': 're',
            'selector': '<em class=\"rich_media_meta text\">(.*?)<a class=\"laiyuan\"',
        },
        'video_create_time': None,
        'content': {
            'method': 'css',
            'selector': 'div.rich_media_content',
        },
        'comment_num': None,
        'tags_list': None,
        'praise_num': None,
        'profile': None,
        'fav_num': None,
    },
    {
        'short_name': 'yg',
        'debug': True,
        'obj_origin': 'www.365yg.com',
        'article_id': {
            'method': 're',
            'selector': '\.com/(\w+)/',
        },
        'title': {
            'method': 'css',
            'selector': 'h2.title ::text',
        },
        'video_title': None,
        'author': {
            'method': 'css',
            'selector': 'div.bui-left span.name ::text',
        },
        'video_author': None,
        'head_url': {
            'method': 'css',
            'selector': 'div.bui-left i.avatar img ::attr("src")',
        },
        'create_time': None,
        'video_create_time': None,
        'content': None,
        'comment_num': None,
        'tags_list': None,
        'praise_num': None,
        'profile': None,
        'fav_num': None,
    },
    {
        'short_name': 'fh',
        'debug': True,
        'obj_origin': 'news.ifeng.com',
        'article_id': {
            'method': 're',
            'selector': '/c/(\w+)',
        },
        'title': {
            'method': 'css',
            'selector': 'div#root h1 ::text',
        },
        'video_title': {
            'method': 'css',
            'selector': 'title ::text'
        },
        'author': {
            'method': 'css',
            'selector': 'span[class^="source-"] a ::text',
        },
        'video_author': {
            'method': 're',
            'selector': '\"columnName\":\"(.*?)\",\"categoryData\"',
        },
        'head_url': None,
        'create_time': {
            'method': 'css',
            'selector': 'span[class^="date-"] ::text',
        },
        'create_time2': {
            'method': 'css',
            'selector': 'div[class^="titleLine-"] p span ::text',
        },
        'video_create_time': {
            'method': 're',
            'selector': '\"creator\":\"weMedia\",\"newsTime\":\"(.*?)\",',
        },
        'content': {
            'method': 'css',
            'selector': 'div[class^="main_content-"]',      # 原先div[class^="main_content-"] div[class^="text-"], 但是遇到video在其中穿插的, 故不设置div[class^="text-"]
        },
        'content2': {
            'method': 'css',
            'selector': 'div[class^="left_articleArea-"] div[class^="text-"]',
        },
        'video_article_content': None,
        'comment_num': None,
        'tags_list': None,
        'praise_num': None,
        'profile': None,
        'fav_num': None,
    },
    {
        'short_name': 'ys',
        'debug': True,
        'obj_origin': 'www.51jkst.com',
        'article_id': {
            'method': 're',
            'selector': '/article/(\d+)/',
        },
        'title': {
            'method': 'css',
            'selector': 'div.content h1 ::text',
        },
        'video_title': None,
        'author': None,
        'video_author': None,
        'head_url': None,
        'create_time': None,
        'video_create_time': None,
        'content': {
            'method': 'css',
            'selector': 'div.art_content',
        },
        'video_article_content': None,
        'comment_num': None,
        'tags_list': None,
        'praise_num': None,
        'profile': None,
        'fav_num': None,
    },
    {
        'short_name': 'cn',
        'debug': True,
        'obj_origin': 'm.cnys.com',
        'article_id': {
            'method': 're',
            'selector': '/(\d+)\.html',
        },
        'title': {
            'method': 'css',
            'selector': 'div.title h2 ::text',
        },
        'video_title': {
            'method': 'css',
            'selector': 'div.title h2 ::text',
        },
        'author': {
            'method': 're',
            'selector': '\"fromSrc\": \"(.*?)\"',
        },
        'video_author': {
            'method': 'css',
            'selector': 'div.daren-title ::text',
        },
        'head_url': None,
        'create_time': {
            'method': 're',
            'selector': '\"upDate\": \"(.*?)\",'
        },
        'video_create_time': {
            'method': 're',
            'selector': '\"upDate\": \"(.*?)\",'
        },
        'content': {
            'method': 'css',
            'selector': 'div.article-content',
        },
        'video_article_content': {
            'method': 'css',
            'selector': 'div.content-text ::text',
        },
        'comment_num': None,
        'tags_list': None,
        'praise_num': None,
        'profile': None,
        'fav_num': None,
    },
    {
        'short_name': 'if',
        'debug': True,
        'obj_origin': 'www.ifanr.com',
        'article_id': {
            'method': 're',
            'selector': '\.com/.*?(\d+)',
        },
        'title': {
            'method': 'css',
            'selector': 'h1.c-single-normal__title ::text',
        },
        'video_title': {
            'method': 'css',
            'selector': 'h1.c-single-video-title ::text',
        },
        'author': {
            'method': 'css',
            'selector': 'p.c-card-author__name ::text',
        },
        'video_author': {
            'method': 'css',
            'selector': 'p.c-article-header-meta__category ::text',
        },
        'head_url': {
            'method': 'css',
            'selector': 'a.c-card-author__info__avatar img ::attr("src")'
        },
        'create_time': {
            'method': 're',
            'selector': '\"datePublished\": \"(.*?)\",'
        },
        'video_create_time': {
            'method': 're',
            'selector': '\"datePublished\": \"(.*?)\",'
        },
        'content': {
            'method': 'css',
            'selector': 'article.c-article-content',
        },
        'video_article_content': None,
        'comment_num': {
            'method': 'css',
            'selector': 'p.js-placeholder-comments-counter ::text',
        },
        'tags_list': {
            'method': 'css',
            'selector': 'div.c-article-tags a ::text',
        },
        'praise_num': None,
        'profile': None,
        'fav_num': None,
    },
    {
        'short_name': 'ss',
        'debug': True,
        'obj_origin': 'songshuhui.net',
        'article_id': {
            'method': 're',
            'selector': '/archives/(\d+)',
        },
        'title': {
            'method': 'css',
            'selector': 'div.atrctitle h2 a ::text',
        },
        'video_title': None,
        'author': {
            'method': 'css',
            'selector': 'div.atrctitle div.metax_single a:nth-child(1) ::text',
        },
        'video_author': None,
        'head_url': None,
        'create_time': {
            'method': 're',
            'selector': '发表于 (.*?)<em> \| Tags',
        },
        'video_create_time': None,
        'content': {
            'method': 'css',
            'selector': 'div.entry',
        },
        'video_article_content': None,
        'comment_num': None,
        'tags_list': {
            'method': 'css',
            'selector': 'div.metax_single em a ::text',
        },
        'praise_num': None,
        'profile': None,
        'fav_num': None,
    },
    {
        'short_name': 'jm',
        'debug': True,
        'obj_origin': 'www.jiemian.com',
        'article_id': {
            'method': 're',
            'selector': '/article/(\d+)\.html',
        },
        'video_id': {
            'method': 're',
            'selector': '/video/(\w+).html',
        },
        'title': {
            'method': 'css',
            'selector': 'div.article-header h1 ::text',
        },
        'video_title': {
            'method': 'css',
            'selector': 'div.article-header h1 ::text',
        },
        'author': {
            'method': 'css',
            'selector': 'div.article-info span.author a ::text',
        },
        'video_author': {
            'method': 'css',
            'selector': 'div.author-name span.name ::text',
        },
        'head_url': None,
        'create_time': {
            'method': 'css',
            'selector': 'div.article-info span:not(.author):nth-child(2) ::text',
        },
        'video_create_time': {
            'method': 're',
            'selector': '<p>发布时间：(.*?)</p>',
        },
        'content': {
            'method': 'css',
            'selector': 'div.article-main',
        },
        'video_article_content': {
            'method': 'css',
            'selector': 'div.article-main',
        },
        'comment_num': None,
        'tags_list': None,
        'praise_num': None,
        'profile': None,
        'fav_num': None,
    },
    {
        'short_name': 'pp',
        'debug': True,
        'obj_origin': 'm.thepaper.cn',
        'article_id': {
            'method': 're',
            'selector': '/newsDetail_forward_(\d+)',
        },
        'video_id': None,
        'title': {
            'method': 'css',
            'selector': 'h1.t_newsinfo ::text',
        },
        'video_title': {
            'method': 'css',
            'selector': 'div.news_video_name ::text',
        },
        'author': {
            'method': 'css',
            'selector': 'p.about_news:nth-child(2) ::text',
        },
        'author2': {
            'method': 'css',
            'selector': 'div.name a ::text',
        },
        'video_author': None,                               # 默认都为空值
        'head_url': None,
        'create_time': {
            'method': 're',
            'selector': '<p class=\"about_news\" style=\"padding-bottom:15px;\">(.*?)&nbsp;.*?</p>',
        },
        'video_create_time': None,
        'content': {
            'method': 'css',
            'selector': 'div.news_part',
        },
        'video_article_content': {
            'method': 'css',
            'selector': 'p#vdetail_sum_p',
        },
        'comment_num': None,
        'tags_list': None,
        'praise_num': None,
        'profile': None,
        'fav_num': None,
    },
    {
        'short_name': 'hx',
        'debug': True,
        'obj_origin': 'm.huxiu.com',
        'article_id': {
            'method': 're',
            'selector': '/article/(\d+)\.',
        },
        'video_id': None,
        'title': {
            'method': 'css',
            'selector': 'div#article div.title ::text',
        },
        'video_title': {
            'method': 'css',
            'selector': 'div#article div.title ::text',
        },
        'author': {
            'method': 'css',
            'selector': 'div#article span.username ::text',
        },
        'video_author': {
            'method': 'css',
            'selector': 'div#article span.username ::text',
        },
        'head_url': {
            'method': 'css',
            'selector': 'div.face-box.fl img ::attr("data-original")',
        },
        'video_head_url': {
            'method': 'css',
            'selector': 'div.face-box.fl img ::attr("data-original")',
        },
        'create_time': {
            'method': 'css',
            'selector': 'span.m-article-time ::text',
        },
        'video_create_time': {
            'method': 'css',
            'selector': 'span.m-article-time ::text',
        },
        'article_main_img': {                               # 文章最上方主图
            'method': 'css',
            'selector': 'div.article-content-img',
        },
        'content': {
            'method': 'css',
            'selector': 'div.article-content',
        },
        'video_article_content': {
            'method': 'css',
            'selector': 'div.article-content',
        },
        'comment_num': None,
        'tags_list': None,
        'praise_num': None,
        'profile': None,
        'fav_num': None,
    },
    {
        'short_name': 'nfzm',
        'debug': True,
        'obj_origin': 'www.infzm.com',
        'article_id': {
            'method': 're',
            'selector': '/content/(\d+)',
        },
        'video_id': None,
        'title': None,
        'video_title': None,
        'author': None,
        'video_author': None,
        'head_url': None,                   # 默认''
        'video_head_url': None,
        'create_time': None,
        'video_create_time': None,
        'content': None,
        'video_article_content': None,
        'comment_num': None,
        'tags_list': None,
        'praise_num': None,
        'profile': None,
        'fav_num': None,
    },
    {
        'short_name': 'hqx',
        'debug': True,
        'obj_origin': 'm.qdaily.com',
        'article_id': {
            'method': 're',
            'selector': '/articles/(\d+)\.html',
        },
        'video_id': None,
        'title': {
            'method': 'css',
            'selector': 'h1.title ::text',
        },
        'video_title': None,
        'author': {
            'method': 'css',
            'selector': 'div.author span.name ::text',
        },
        'video_author': None,
        'head_url': {
            'method': 'css',
            'selector': 'div.author span.avatar img ::attr("src")',
        },
        'video_head_url': None,
        'create_time': {
            'method': 'css',
            'selector': 'span.date ::attr("data-origindate")',
        },
        'video_create_time': None,
        'article_main_img': {                               # 文章最上方主图
            'method': 'css',
            'selector': 'div.banner',
        },
        'content': {
            'method': 'css',
            'selector': 'div.detail',
        },
        'video_article_content': None,
        'comment_num': None,
        'tags_list': None,
        'praise_num': None,
        'profile': None,
        'fav_num': None,
    },
    {
        'short_name': 'xg',
        'debug': True,
        'obj_origin': 'www.ixigua.com',
        'article_id': {
            'method': 're',
            'selector': '\.com/(\w+)/',
        },
        'title': {
            'method': 'css',
            'selector': 'div h1 ::text',
        },
        'video_title': {
            'method': 'css',
            'selector': 'div h1 ::text',
        },
        'author': {
            'method': 'css',
            'selector': 'a.videoDesc__userName ::text',
        },
        'video_author': {
            'method': 'css',
            'selector': 'a.videoDesc__userName ::text',
        },
        'head_url': None,
        'create_time': None,
        'video_create_time': None,
        'content': None,
        'video_article_content': None,
        'comment_num': None,
        'tags_list': None,
        'praise_num': None,
        'profile': None,
        'fav_num': None,
    },
    {
        'short_name': 'ck',
        'debug': True,
        'obj_origin': 'www.vmovier.com',
        'article_id': {
            'method': 're',
            'selector': '\.com/(\d+)\?',
        },
        'video_id': None,
        'title': None,
        'video_title': None,
        'author': None,
        'video_author': None,
        'head_url': None,                   # 默认''
        'video_head_url': None,
        'create_time': None,
        'video_create_time': None,
        'content': None,
        'video_article_content': None,
        'comment_num': None,
        'tags_list': None,
        'praise_num': None,
        'profile': None,
        'fav_num': None,
    },
    {
        'short_name': 'lsp',
        'debug': True,
        'obj_origin': 'www.pearvideo.com',
        'article_id': {
            'method': 're',
            'selector': '/video_(\d+)',
        },
        'title': None,
        'video_title': {
            'method': 'css',
            'selector': 'h1.video-tt ::text',
        },
        'author': None,
        'video_author': {
            'method': 'css',
            'selector': 'div.col-name ::text',
        },
        'head_url': None,
        'video_head_url': {
            'method': 'css',
            'selector': 'div.col-name i.col-icon img ::attr("src")',
        },
        'create_time': None,
        'video_create_time': {
            'method': 'css',
            'selector': 'div.date ::text',
        },
        'content': None,
        'video_article_content': {
            'method': 'css',
            'selector': 'div.summary',
        },
        'comment_num': None,
        'tags_list': {
            'method': 'css',
            'selector': 'div.tags a span.tag ::text',
        },
        'praise_num': None,
        'profile': None,
        'fav_num': {
            'method': 'css',
            'selector': 'div.fav ::text'
        },
    },
    {
        'short_name': 'amz',
        'debug': True,
        'obj_origin': 'aimozhen.com',
        'article_id': {
            'method': 're',
            'selector': '/view/(\d+)/',
        },
        'title': {
            'method': 'css',
            'selector': 'div#video-headline ::text',
        },
        'video_title': None,
        'author': {
            'method': 'css',
            'selector': 'div#video-user-name ::text',
        },
        'video_author': None,
        'head_url': {
            'method': 'css',
            'selector': 'a.user-avatar img ::attr("src")',
        },
        'video_head_url': None,
        'create_time': None,                                # 默认null
        'video_create_time': None,
        'content': {
            'method': 'css',
            'selector': 'div#video-content',
        },
        'video_article_content': None,
        'video_iframe': {
            'method': 're',
            'selector': 'var player = \'(.*?)\'',
        },
        'client_id': {
            'method': 're',
            'selector': 'client_id: \'(.*?)\'',
        },
        'vid': {
            'method': 're',
            'selector': 'vid: \'(.*?)\'',
        },
        'comment_num': None,
        'tags_list': None,
        'praise_num': None,
        'profile': None,
        'fav_num': None,
    },
    {
        'short_name': 'mp',
        'debug': True,
        'obj_origin': 'www.meipai.com',
        'article_id': {
            'method': 're',
            'selector': '/media/(\d+)',
        },
        'title': {
            'method': 'css',
            'selector': 'title ::text',
        },
        'video_title': None,
        'author': {
            'method': 're',
            'selector': '<meta property=\"og:video:director\" content=\"(.*?)\">',
        },
        'video_author': None,
        'head_url': {
            'method': 'css',
            'selector': 'div.user-info img.avatar ::attr("src")',
        },
        'video_head_url': None,
        'create_time': {
            'method': 're',
            'selector': '<meta property=\"og:video:release_date\" content=\"(.*?)\">'
        },
        'video_create_time': None,
        'content': {
            'method': 're',
            'selector': '<meta name=\"description\" content=\"(.*?)\">',
        },
        'video_article_content': None,
        'comment_num': {                                # 评价数和喜欢数, 可从pc找到对应数字, 再在m站找位置
            'method': 're',
            'selector': '\"comments_count\":(\d+),',
        },
        'tags_list': None,
        'praise_num': None,
        'profile': None,
        'fav_num': {
            'method': 're',
            'selector': '\"likes_count\":(\d+),',
        },
    },
    {
        'short_name': 'hk',
        'debug': True,
        'obj_origin': 'haokan.baidu.com',
        'article_id': {
            'method': 're',
            'selector': 'vid=(\d+)',
        },
        'title': {
            'method': 'css',
            'selector': 'div#content h1 ::text',
        },
        'video_title': None,
        'author': {
            'method': 'css',
            'selector': 'div.detail span.name-text ::text',
        },
        'video_author': None,
        'head_url': {
            'method': 'css',
            'selector': 'span.face-wrap img.face ::attr("src")',
        },
        'video_head_url': None,
        'create_time': {
            'method': 're',
            'selector': '<div class=\"c-gap-top-small c-gray date\">发布时间：(.*?)</div>'
        },
        'video_create_time': None,
        'content': None,
        'video_article_content': None,
        'comment_num': {
            'method': 're',
            'selector': '(\d+)人对此视频发表评论',
        },
        'tags_list': None,
        'praise_num': {
            'method': 're',
            'selector': ',有(\d+)人点赞,'
        },
        'profile': None,
        'fav_num':None,
    },
]

'''
企业商家信息可扩展
'''
COMPANY_ITEM_LIST = [
    {
        'short_name': 'ty',
        'debug': True,
        'obj_origin': 'www.tianyancha.com',
        'province_city_info': {
            'zhixia_city_name': {
                'method': 'css',
                'selector': 'div.item.-single ::text',
            },
            'zhixia_city_url': {                                                                 # 直辖市
                'method': 'css',
                'selector': 'div.item.-single ::attr("href")',
            },
            'province_name': {
                'method': 'css',
                'selector': 'a.link-hover-click.overflow-width ::text',
            },
            'province_url': {
                'method': 'css',
                # div.row a.link-hover-click.overflow-width
                'selector': 'a.link-hover-click.overflow-width ::attr("href")',
            },
            'city_name': {
                'method': 'css',
                'selector': 'a.link-hover-click.item ::text',
            },
            'city_url': {
                'method': 'css',
                'selector': 'a.link-hover-click.item ::attr("href")',
            },
        },
        'company_url': {
            'method': 'css',
            'selector': 'div.header a.name ::attr("href")',
        },
        'unique_id': {                                      # 企业唯一的id
            'method': 're',
            'selector': '/company/(\d+)',
        },
        'company_status': {
            'method': 'css',
            'selector': 'div.header div.tag ::text',      # 公司状态, 1: 暂无 or 存续
        },
        'company_link': {                               # 企业的官网地址
            'method': 'css',
            'selector': 'a.company-link ::attr("title")',
        },
        'company_name': {
            'method': 'css',
            'selector': 'h1.name ::text',
        },
        'legal_person': {
            'method': 'css',
            'selector': 'div.name a.link-click ::text',                    # 法人
        },
        'phone': {
            'method': 'css',
            'selector': 'div.detail div.in-block span.hidden ::text',      # ["0311-66572560","0311-66572558","0311-66572557"]
        },
        'email_address': {
            'method': 'css',
            'selector': 'div.detail div.in-block span ::text',              # index 7
        },
        'address': {
            'method': 'css',
            'selector': 'div#_container_baseInfo tr td[colspan=\"4\"] ::text', # index 0
        },
        'brief_introduction': {             # company简介
            'method': 'css',
            'selector': 'div.summary script#company_base_info_detail ::text',
        },
        'business_range': {                 # 经营范围
            'method': 'css',
            'selector': 'span.js-full-container.hidden ::text',                   # is_first=False, 取第一个
        },
        'founding_time': {                  # 成立时间
            'method': 're',
            'selector': '\"pubDate\":\"(.*?)\",',
        },
        'employees_num': None,
    },
    {
        'short_name': 'hy',         # 中国黄页
        'debug': True,
        'obj_origin': 'm.huangye88.com',
        'trade_type_info': {
            'trade_type_name': {    # list
                'method': 'css',
                'selector': 'ul.qiyecont li a ::attr("title")',
            },
            'trade_type_url': {     # list
                'method': 'css',
                'selector': 'ul.qiyecont li a ::attr("href")',
            },
            'trade_type_province': {    # 分类的省份
                'method': 'css',
                'selector': 'a ::attr("href")',
            },
        },
        'unique_id': {
            'method': 're',
            'selector': '/qiye(\d+)/',
        },
        'company_status': None,     # 公司状态, 1: 在业 or 续存
        'company_link': {           # 公司网站(最后一个)
            'method': 'css',
            'selector': 'ul.pro-list li ::text',
        },
        'company_info_detail_li': {    # 公司信息的li
            'method': 'css',
            'selector': 'ul.pro-list li',
        },
        'company_name': {           # 第一个
            'method': 'css',
            'selector': 'ul.pro-list li ::text',
        },
        'legal_person': {
            'method': 'css',
            'selector': 'ul.pro-list li ::text',                    # 法人
        },
        'phone': {
            'method': 'css',
            'selector': 'ul.pro-list li ::text',
        },
        'email_address': {
            'method': 'css',
            'selector': 'ul.pro-list li ::text',
        },
        'address': {
            'method': 'css',
            'selector': 'div.contact li a ::text',
        },
        'brief_introduction': {     # 用css筛选的不完整, 用re
            'method': 're',
            # 'selector': 'div.com-intro p.p1 ::text',
            'selector': '<p class=\"p1\".*?>(.*?)</p>',
        },
        'business_range': {                 # 经营范围(hy:主营产品)
            'method': 'css',
            'selector': 'ul.pro-list li ::text',
        },
        'founding_time': {                  # 成立时间
            'method': 'css',
            'selector': 'ul.pro-list li ::text',
        },
        'employees_num': {                  # 员工人数
            'method': 'css',
            'selector': 'ul.pro-list li ::text',
        },
        'lng': None,
        'lat': None,
    },
    {
        'short_name': 'al',         # 1688
        'debug': True,
        'obj_origin': 'm.1688.com',
        'trade_type_info': {
            'type_name_sub': {      # 第二类分类name type: list
                'method': 'css',
                'selector': 'ul.sub-cate-list li a ::attr("href")',
            },
            'type_name_third': {    # 第三类分类name type:list
                'method': 'css',
                'selector': 'div.third-cate-list a ::text',
            },
        },
        'unique_id': {
            'method': 're',
            'selector': '/company/(.*?)\.html',
        },
        'company_status': None,     # 公司状态, 1: 在业 or 续存
        'company_link': None,       # 公司网站
        'company_info_detail_li': { # 公司信息的li
            'method': 'css',
            'selector': 'ul.info-item li div',
        },
        'company_name': None,       # 在company_info_detail_li中
        'legal_person': None,       # 在company_info_detail_li中
        'phone': {                  # list
            'method': 'css',
            'selector': 'div.phone ::text',
        },
        'email_address': None,
        'address': None,            # 在company_info_detail_li中
        'brief_introduction': None, # al: 此处拿来存放主营产品
        'business_range': None,     # 在company_info_detail_li中
        'founding_time': None,      # 在company_info_detail_li中
        'employees_num': None,
        'lng': None,
        'lat': None,
    },
    {
        'short_name': '114',
        'debug': True,
        'orj_origin': 'www.114pifa.com',
        'trade_type_info': {
            'type_url_sub': {       # 第二类分类url: list
                'method': 'css',
                'selector': 'div.detail a ::attr("href")',
            },
            'type_name_sub': {      # 第二类分类name type: list
                'method': 'css',
                'selector': 'div.detail a ::text',
            },
            'type_url_third': {     # 第三类分类url: list
                'method': 'css',
                'selector': 'ul.classifyList li a ::attr("href")',
            },
            'type_name_third': {    # 第三类分类name type:list
                'method': 'css',
                'selector': 'ul.classifyList li a ::text',
            },
            'type_url_number': {    # url中number筛选, eg: /c-17.html
                'method': 're',
                'selector': 'c-(\d+)',
            },
            'one_type_url_list': {  # 一个子分类的厂家url
                'method': 'css',
                'selector': 'div.f12.c6.unit a ::attr("href")',
            },
            'one_type_url_list_item': {  # 一个子分类的厂家介绍url的list 的item
                'method': 're',
                'selector': '\/c\/(\w+)',
            },
        },
        'unique_id': {
            'method': 're',
            'selector': '\/ca\/(\w+)',
        },
        'company_status': None,     # 公司状态, 1: 在业 or 续存
        'company_link': None,       # 公司网站
        'company_info_detail_li_1': { # 公司信息的li (详细信息部分)
            'method': 'css',
            'selector': 'div.control li',
        },
        'company_info_detail_li_2': { # 公司信息的li (联系我们部分)
            'method': 'css',
            'selector': 'div.contact-way1 p.text-in11 small',
        },
        'company_name': {
            'method': 'css',
            'selector': 'div.com-name ::text'
        },
        'legal_person': None,       # 在company_info_detail_li_1中
        'phone': None,              # 在company_info_detail_li_2中
        'email_address': None,
        'address': None,            # 在company_info_detail_li_2中
        'brief_introduction': {     # 简介
            'method': 'css',
            'selector': 'div.info-word1 ::text',
        },
        'business_range': None,     # 在company_info_detail_li_1中
        'founding_time': None,      # 在company_info_detail_li_1中
        'employees_num': None,      # 在company_info_detail_li_1中
        'lng': None,
        'lat': None,
    },
    {
        'short_name': 'ic',
        'debug': True,
        'orj_origin': 'cn.made-in-china.com',
        'trade_type_info': {
            'type_url_sub': {       # 第二类分类url: list
                'method': 'css',
                'selector': 'li.item a.item-text ::attr("href")',
            },
            'type_name_sub': {      # 第二类分类name type: list
                'method': 'css',
                'selector': 'li.item a.item-text ::text',
            },
            'type_url_third': {     # 第三类分类url: list
                'method': 'css',
                'selector': 'li.item a.item-text ::attr("href")',
            },
            'type_name_third': {    # 第三类分类name type:list
                'method': 'css',
                'selector': 'li.item a.item-text ::text',
            },
            'one_type_url_list': {  # 一个子分类的厂家url
                'method': 'css',
                'selector': 'div.pro-img a ::attr("href")',
            },
        },
        'unique_id': {
            'method': 're',
            'selector': '\/company-(\w+)\/',
        },
        'company_status': None,     # ''
        'company_link': None,       # ''
        'company_info_detail_li_1': { # 公司信息的li (详细信息部分)
            'method': 'css',
            'selector': 'div.gropone div.dtl-item table.tb-dtl tr',
        },
        'company_info_detail_li_2': { # 公司信息的li (联系我们部分)
            'method': 'css',
            'selector': 'div.gropone div.dtl-item table.tb-dtl tr',
        },
        'company_name': {
            'method': 'css',
            'selector': 'h1.h a#comName ::text'
        },
        'legal_person': None,       # ''
        'phone': None,              # 在company_info_detail_li_2中(th:手机 and 电话两个字段的值)
        'email_address': None,
        'address': None,            # 在company_info_detail_li_2中(th:地址)
        'brief_introduction': {     # 简介
            # 'method': 'css',
            # 'selector': 'div.co-des ::text',  # 获取信息不完整
            'method': 're',
            'selector': '<div class=\"co-des js-comDescript\".*?>(.*?)<\/div>',
        },
        'business_range': None,     # 在company_info_detail_li_1中(th:主营产品)
        'founding_time': None,      # 赋默认值
        'employees_num': None,      # 在company_info_detail_li_1中(th:员工人数)
        'lng': None,
        'lat': None,
    },
    {
        'short_name': 'yw',
        'debug': True,
        'orj_origin': 'www.yiwugo.com',
        'trade_type_info': {
            'type_url_sub': {       # 第二类分类的cate id: list
                'method': 'css',
                'selector': 'div#categoryBarHook ul.category-bar li ::attr("data-uppertype")',
            },
            'type_name_sub': {      # 第二类分类name type: list
                'method': 'css',
                'selector': 'div#categoryBarHook ul.category-bar li ::text',
            },
        },
        'unique_id': {
            'method': 're',
            'selector': '\/hu\/(\w+)',
        },
        'company_status': None,     # ''
        'company_link': None,       # ''
        'company_info_detail_li_1': { # 公司信息的li (详细信息部分)
            'method': 'css',
            'selector': 'ul.shop_introduce li',
        },
        'company_name': {
            'method': 'css',
            'selector': 'li.temp-company-v span.blod ::text'
        },
        'legal_person': None,       # ''
        'phone': None,              # yw不在此处取值!从phone1 手机 phone2座机中取值!
        'phone1': {
            'method': 'css',
            'selector': 'ul.shop_introduce li.ico-shop-02 ::text',
        },
        'phone2': {
            'method': 'css',
            'selector': 'ul.shop_introduce li.ico-shop-03 ::text',
        },
        'email_address': {
            'method': 'css',
            'selector': 'ul.shop_introduce li.ico-shop-04 ::text',
        },
        'address': None,            # 在company_info_detail_li_1中(span.c999:商铺地址：)
        'brief_introduction': {     # 简介
            'method': 'css',
            'selector': 'div.mt15 p.c999 span#shop-int ::text',
        },
        'business_range': None,     # 在company_info_detail_li_1中(span.c999:主营商品：)
        'founding_time': None,      # 赋默认值
        'employees_num': None,      # ''
        'lng': None,
        'lat': None,
    },
    {
        'short_name': 'hn',
        'debug': True,
        'orj_origin': 'www.huoniuniu.com',
        'trade_type_info': {
            'type_cid_sub': {       # 第二类分类的cate id: list
                'method': 'css',
                'selector': 'div.list-item ::attr("data-cid")',
            },
            'type_name_sub': {      # 第二类分类name type: list
                'method': 'css',
                'selector': 'p.item-nav-p.cf a ::text',
            },
            'city_name': {
                'method': 'css',
                'selector': 'div.ds-city.cf a ::text',
            },
            'city_url': {           # 城市路由地址
                'method': 'css',
                'selector': 'div.ds-city.cf a ::attr("href")',
            },
            'shop_item': {
                'method': 'css',
                'selector': 'div.findstyle_left div.ps-item1 div.shopname_box a.shopname.max_width ::attr("href")',     # 此处要过滤掉最新上架的
            },
            'w3': {
                'method': 're',
                'selector': ':\/\/(\w+)\.',
            },
        },
        'unique_id': {
            'method': 're',
            'selector': '\/shop\/(\d+)',
        },
        'company_status': None,     # ''
        'company_link': None,       # ''
        'company_info_detail_li_1': { # 公司信息的li (详细信息部分)
            'method': 'css',
            'selector': 'div.shop-item.cf',
        },
        'company_name': {
            'method': 'css',
            'selector': 'div.shop-jieshao span.title ::text'
        },
        'legal_person': None,       # ''
        'phone': None,              # 在company_info_detail_li_1中(div.left span.title:电话)
        'email_address': None,      # ''
        'address': None,            # 在company_info_detail_li_1中(div.left span.title:地址)
        'brief_introduction': None, # 简介 ''
        'business_range': None,     # 主营范围 ''
        'founding_time': None,      # 赋默认值
        'employees_num': None,      # ''
        'lng': None,
        'lat': None,
    },
    {
        'short_name': 'pk',
        'debug': True,
        'orj_origin': 'www.ppkoo.com',
        'trade_type_info': {
            'type_name_sub': {      # 第二类分类name type: list
                'method': 'css',
                'selector': 'div.item p.text ::text',
            },
        },
        'unique_id': {
            'method': 're',
            'selector': '\/shop\/(\d+)',
        },
        'company_status': None,     # ''
        'company_link': None,       # ''
        'company_name': None,       # data.get('shop_name', '')
        'legal_person': None,       # ''
        'phone': None,              # data.get('phone_mob', '')
        'email_address': None,      # ''
        'address': None,            # 在ori_address中
        'brief_introduction': None, # 简介 ''
        'business_range': None,     # 主营范围 ''
        'founding_time': None,      # 赋默认值
        'employees_num': None,      # ''
        'lng': None,
        'lat': None,
    },
    {
        'short_name': 'ng',
        'debug': True,
        'orj_origin': 'www.nanguo.cn',
        'trade_type_info': {
            'type_url_sub': {       # 第二类分类url: list
                'method': 'css',
                'selector': 'li.category-li a ::attr("href")',
            },
            'type_id_sub': {      # 第二类分类id
                'method': 're',
                'selector': 'id=(\d+)',
            },
            'type_name_third': {    # 第三类分类name type:list
                'method': 'css',
                'selector': 'div.box a ::text',
            },
            'one_type_cate_id_list': {  # 一个子分类的厂家cate_id
                'method': 'css',
                'selector': 'div.j_AddCartBtn.j_AddCartBtn ::attr("data-coaid")',
            },
        },
        'unique_id': {
            'method': 're',
            'selector': '\/id\/(\d+)',
        },
        'company_status': None,     # 公司状态, 1: 在业 or 续存
        'company_link': None,       # 公司网站
        'company_info_detail_li_1': { # 公司信息的li (详细信息部分)
            'method': 'css',
            'selector': 'div.companyContact-companyName',
        },
        'company_info_detail_li_2': { # 公司信息的li (电话, 固话)
            'method': 'css',
            'selector': 'span.companyContactConsultContent',
        },
        'company_name': None,       # 在company_info_detail_li_1中(span:店铺名称, 其值::text)
        'legal_person': None,       # ''
        'phone': None,              # 在company_info_detail_li_2中(div.companyContactConsultTouch:电话客服 or 手机客服)
        'email_address': None,
        'address': {
            'method': 'css',
            'selector': 'span.companyContact-adressValue ::text',
        },
        'brief_introduction': None,
        'business_range': {
            'method': 'css',
            'selector': 'div.companyBasicShelling.wbg ::text'
        },
        'founding_time': None,
        'employees_num': None,
        'lng': None,
        'lat': None,
    },
    {
        'short_name': 'gt',
        'debug': True,
        'orj_origin': 'www.go2.cn',
        'trade_type_info': {
            'shoes_attr_name1': {
                'method': 'css',
                'selector': 'ul li.more-attr-item ol li a ::text',
            },
            'shoes_attr_name2': {
                'method': 'css',
                'selector': 'ul.filter-list li label a ::text',
            },
            'company_url': {
                'method': 'css',
                'selector': 'div.product-hover-info p.item span a ::attr("href")',
            },
        },
        'unique_id': {
            'method': 're',
            'selector': '\/\/(\w+)\.go2\.cn',
        },
        'company_status': None,     # 公司状态, 1: 在业 or 续存
        'company_link': None,       # 公司网站
        'company_info_detail_li_1': { # 公司信息的li (详细信息部分, 此处用来获取province, city, 在label(城市：))
            'method': 'css',
            'selector': 'div.merchant-info-item.text',
        },
        'company_name': {
            'method': 'css',
            'selector': 'a.merchant-title ::text',
        },
        'legal_person': None,       # ''
        'phone': {
            'method': 'css',
            'selector': 'span.contact-tel span ::text',
        },
        'email_address': None,
        'address': {
            'method': 'css',
            'selector': 'span.merchant-info-addr ::text',   # 有两个值, 取第一个(即is_first=True)
        },
        'brief_introduction': {
            'method': 'css',
            'selector': 'div.main-content div.int-letter ::text'
        },
        'business_range': None,
        'founding_time': None,
        'employees_num': None,
        'lng': None,
        'lat': None,
    },
    {
        'short_name': 'mt',
        'debug': True,
        'obj_origin': 'i.meituan.com',
        'categroy_info': {
            'ul_list': {
                'method': 'css',
                'selector': 'ul.box.table',
            },
            'ul_li': {
                'method': 'css',
                'selector': 'li',
            },
            'one_type_url': {
                'method': 'css',
                'selector': 'a.react ::attr(href)',
            },
            'one_type_name': {
                'method': 'css',
                'selector': 'a.react ::text',
            },
            'cid': {
                'method': 're',
                'selector': 'cid=(\d+)',
            },
            'cate_type': {
                'method': 're',
                'selector': 'cateType=(\w+)',
            }
        },
        'unique_id': {
            'method': 're',
            'selector': '/poi/(\d+)',
        },
        'shop_url': {                       # mt 店铺的url
            'method': 'css',
            'selector': 'dl.list dd.poi-list-item a.react ::attr("href")',
        },
        'company_link': None,
        'company_name': {
            'method': 're',
            'selector': '\"name\":\"(.*?)\",',
        },
        'legal_person': None,
        'phone': {
            'method': 're',
            'selector': '\"phone\":\"(.*?)\",',
        },
        'email_address': None,
        'address': {
            'method': 're',
            'selector': '\"addr\":\"(.*?)\",',
        },
        'brief_introduction': None,
        'business_range': None,
        'founding_time': None,
        'employees_num': None,
        'lng': {
            'method': 're',
            'selector': '\"lng\":(.*?),',
        },
        'lat': {
            'method': 're',
            'selector': '\"lat\":(.*?),',
        },
    },
    {
        'short_name': 'bd',
        'debug': True,
        'obj_origin': 'api.map.baidu.com',
        'unique_id': None,
        'shop_url': None,
        'company_link': None,
        'company_name': None,
        'legal_person': None,
        'phone': None,
        'email_address': None,
        'address': None,
        'brief_introduction': None,
        'business_range': None,
        'founding_time': None,
        'employees_num': None,
        'lng': None,
        'lat': None,
    },
    {
        'short_name': 'gd',
        'debug': True,
        'obj_origin': 'restapi.amap.com',
        'unique_id': None,
        'shop_url': None,
        'company_link': None,
        'company_name': None,
        'legal_person': None,
        'phone': None,
        'email_address': None,
        'address': None,
        'brief_introduction': None,
        'business_range': None,
        'founding_time': None,
        'employees_num': None,
        'lng': None,
        'lat': None,
    },
    {
        'short_name': 'qcc',
        'debug': True,
        'obj_origin': 'www.qichacha.com',
        'province_city_info': {
            'zhixia_city_name': None,                       # 直辖市已在省份中
            'zhixia_city_url': None,
            'province_name': {
                'method': 'css',
                'selector': 'li.areatext-center a ::text',  # 原先是li.area.text-center a, 但是清洗后是li.areatext-center a
            },
            'province_url': {
                'method': 'css',
                'selector': 'li.areatext-center a ::attr("href")',
            },
            'city_name': None,                              # 无法单独根据城市筛选, 提示搜索太广泛
            'city_url': None,
        },
        'company_url': {
            'method': 'css',
            'selector': 'section#searchlist a.list-group-item ::attr("href")',
        },
        'unique_id': {                                      # 企业唯一的id
            'method': 're',
            'selector': 'firm_(\w+)\.',
        },
        'company_status': {
            'method': 'css',
            'selector': 'section#searchlist span.clear span.label ::text',      # 公司状态, 1: 在业 or 续存
        },
        'company_link': None,
        'company_name': {
            'method': 'css',
            'selector': 'div.company-name ::text',
        },
        'legal_person': {
            'method': 'css',
            'selector': 'a.oper ::text',                    # 法人
        },
        'phone': {
            'method': 'css',
            'selector': 'a.phone ::text',
        },
        'email_address': {
            'method': 'css',
            'selector': 'a.email ::text',
        },
        'address': {
            'method': 'css',
            'selector': 'div.address ::text',
        },
        'brief_introduction': None,
        'business_range': {                 # 经营范围
            'method': 'css',
            'selector': 'div.basic-item div.basic-item-right ::text',
        },
        'founding_time': {                  # 成立时间
            'method': 'css',
            'selector': 'div.basic-item div.basic-item-right ::text',
        },
        'employees_num': None,
        'lng': None,
        'lat': None,
    },
]

'''
goods item
'''
GOODS_ITEM_LIST = [
    {
        'short_name': 'al',
        'log_save_path': MY_SPIDER_LOGS_PATH + '/1688/_/',
        'is_use_driver': True,
        'driver_type': PHANTOMJS,
        'driver_executable_path': PHANTOMJS_DRIVER_PATH,
        'user_agent_type': PHONE,
        'goods_id_info': {
            'goods_id': {
                'method': 're',
                'selector': 'detail\.1688\.com\/offer\/(.*?).html',
            }
        }
    }
]

'''
cookies
'''
SINA_COOKIES = ''
TB_COOKIES = None
try:
    with open('/Users/afa/myFiles/cookies/tb_cookies.txt', 'r') as f:
        TB_COOKIES = f.readline().replace('\n', '')
except:
    pass