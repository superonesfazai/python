# coding:utf-8

'''
@author = super_fazai
@File    : jd_youxuan_talent_recommend.py
@Time    : 2017/12/5 15:14
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

import requests
import re
import json
import gc, os
from random import randint
from json import dumps
from pprint import pprint
from settings import IS_BACKGROUND_RUNNING, JD_YOUXUAN_DAREN_IS_BACKGROUND_RUNNING, PHANTOMJS_DRIVER_PATH
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from scrapy.selector import Selector

from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from jd_parse import JdParse
import pytz, datetime, time

from fzutils.internet_utils import get_random_pc_ua

# phantomjs驱动地址
EXECUTABLE_PATH = PHANTOMJS_DRIVER_PATH

'''
京东购物圈达人推荐
https://wqs.jd.com/shopping/daren.html

jd优选达人推荐文章的地址为:
https://wq.jd.com/shopgroup_feed/FeedDetail?shareid=xxxxxxxxxxxx
# 存在skuid:"0"的情况    就没有推荐商品

# 推荐详情的地址(咱们可以直接将其在之前数据中得到)
# recommend_goods_info_url = 'https://wqs.jd.com/shoppingv2/detail.html?shareid=1091423620317126735'
'''

class JdTalentRecommend(object):
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'wq.jd.com',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
            # 'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://wqs.jd.com/shopping/daren.html',  # 必须的参数
            # 'Cookie': 'mobilev=html5; webp=1; sc_width=414; shshshfpa=d66b90d1-e35b-4d2b-f376-e769e8f394ad-1512455224; wq_area=15_1213_0%7C; ipLoc-djd=1-72-2799-0; weather_timestamp=; __jdv=122270672%7Cdirect%7Ct_1000072661_17003_001%7Cweixin%7C-%7C1512456060372; rurl=http%3A%2F%2Fwqs.jd.com%2Fmy%2Findexv2.shtml%3Fshownav%3D1%26ptag%3D137196.10.4; TrackerID=GmU1QO9JecAa0YMIlS0iSwrcL_xL5sd7vXMXM7wJwc652plPJuY-HnzrBoLozFAayHuhURAQPfUmDIG4vxyGc3oHUXmlmcsWwpcfIdfT6yIRa3z5FRbClkwuz6rmigCAAIQz--5H5cJXblOMMqgpqg; pt_key=AAFaJj-8ADAiVqaGUebHBuYpIeFbGw0v6__-VM3z3yYYL1susCYjgvnvAaNZYNY3cITO5d2uKH8; pt_pin=jd_42a8fb51f9966; pt_token=ny81i9qi; pwdt_id=jd_42a8fb51f9966; buy_uin=15277665150; jdpin=jd_42a8fb51f9966; pin=jd_42a8fb51f9966; wq_skey=zm3D538945DC4C21823A8A61723FBE6550FE8BFEE3B88AA0E0ED63ACF55DB12AF36AAE7247E099C5B96BB167F955CC6CC6; wq_uin=15277665150; wq_logid=1512457148.1210098481; __jdu=1512454812735826109527; 3AB9D23F7A4B3C9B=E3J6QKDLSEMGLT6NNWSHD7D7WDL2WJMRIN3HWD3Y4P5YVRZPAZ2QMXWURQHIJLVPQPUFWOLHHUTYKI2OHUJFDCFJUE; __jda=122270672.1512454812735826109527.1512454813.1512454813.1512454813.1; __jdb=122270672.28.1512454812735826109527|1.1512454813; __jdc=122270672; mba_muid=1512454812735826109527; mba_sid=15124548495135409042709132064.24; sid=02ca8d35bacedc8cde4bd1e8890ff8bb; shshshfp=05f67ee8e0a575e4b0736225d3ecb2d2; shshshsID=f813878eddcc340213f6300f1fb4f7e8_42_1512457566857; shshshfpb=24603a59721c4492483e385e8a96854835a12b625c92e2942ce263c391; wxa_level=1; retina=1; cid=3; __wga=1512457589199.1512455224147.1512455224147.1512455224147.37.1; PPRD_P=EA.17003.4.1-UUID.1512454812735826109527-CT.39283.1.4-DAP.3550786096544613541%3A4316454547851%3A696%3A656007-FOCUS.FO4O604%253A3OA02873O2DEB74O5DC64O248A03%253A7O99CFA62DO23O19O3ED00BD718B5O2B8031F25E4475D045769',
        }
        self.init_phantomjs()

    def get_all_user_and_their_recommend_goods_list(self):
        for index in range(1, 100):
            t = str(time.time().__round__()) + str(randint(100, 999))  # time.time().__round__() 表示保留到个位

            # 达人推荐的地址(ajax请求)
            tmp_url = 'https://wq.jd.com/shopgroup_feed/GetDarenFeeds?pageno={}&pagesize=5&darenType=0&perDarenFeedNum=3&totalpage=1&_={}&callback=jsonpCBKC&g_ty=ls'.format(
                str(index), t
            )

            self.from_ip_pool_set_proxy_ip_to_phantomjs()
            self.driver.set_page_load_timeout(15)  # 设置成15秒避免数据出错

            try:
                self.driver.get(tmp_url)
                self.driver.implicitly_wait(15)
            except Exception as e:  # 如果超时, 终止加载并继续后续操作
                print('-->>time out after 15 seconds when loading page')
                self.driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
                # pass

            body = self.driver.page_source
            body = re.compile(r'\n').sub('', body)
            body = re.compile(r'\t').sub('', body)
            body = re.compile(r'  ').sub('', body)
            # print(body)
            body = re.compile(r'square\((.*)\)').findall(body)

            if body != []:
                body = body[0]
                try:
                    data = json.loads(body)
                    # pprint(data)
                except:
                    print('json.loads转换body得到data时出错!')
                    return []

                if data.get('user_list') is None:   # 表示没有数据了，返回的为 square({"errmsg":"","iRet":0,"totalnum":347} )
                    print('body中获取的user_list为None!')
                    pass

                else:
                    user_list = data.get('user_list', [])
                    # pprint(user_list)

                    for item in user_list:
                        # 达人昵称
                        nick_name = item.get('nickname', '')

                        # 达人头像
                        head_url = item.get('headurl', '')
                        head_url = re.compile(r'http:').sub('', head_url)
                        if re.compile(r'^http').findall(head_url) != []:
                            pass
                        else:
                            head_url = 'http:' + head_url

                        # 个性签名
                        profile = item.get('profile', '')

                        my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                        sql_str = r'select SiteID, GoodsID, IsDelete, MyShelfAndDownTime, Price, TaoBaoPrice from dbo.GoodsInfoAutoGet where SiteID=7 or SiteID=8 or SiteID=9 or SiteID=10'
                        _ = my_pipeline._select_table(sql_str=sql_str)
                        db_goods_id = [j[1] for j in list(_)] if _ is not None else []
                        # print(db_goods_id)
                        sql_str = r'select share_id from dbo.jd_youxuan_daren_recommend'
                        db_share_id = [j[0] for j in list(my_pipeline._select_table(sql_str=sql_str))]
                        # print(db_share_id)
                        jd = JdParse()

                        # 达人推荐的商品info
                        feed_list = item.get('feed_list', [])
                        for feed_list_item in feed_list:
                            if feed_list_item.get('shareid', '') in db_share_id:
                                print('该share_id({})已存在于数据库中, 此处跳过!'.format(feed_list_item.get('shareid', '')))
                                pass
                            else:
                                # share_id
                                share_id = feed_list_item.get('shareid', '')
                                article_url = 'https://wqs.jd.com/shoppingv2/detail.html?shareid=' + share_id
                                print('------>>>| 正在抓取的jd优选达人推荐文章的地址为: ', 'https://wqs.jd.com/shoppingv2/detail.html?shareid=' + share_id)

                                # 图片的信息
                                tmp_share_img_url_list = []
                                for item2 in feed_list_item.get('sharepicurl', '').split(','):
                                    if re.compile(r'^//').findall(item2) == []:
                                        tmp_share_img_url = 'https://img14.360buyimg.com/evalpic/s800x800_' + item2
                                    else:
                                        tmp_share_img_url = 'http:' + item2
                                    tmp_share_img_url_list.append(tmp_share_img_url)
                                share_img_url_list = [{'img_url': item5} for item5 in tmp_share_img_url_list]

                                # 处理得到达人的自拍图片div
                                tmp_img_div_desc = ''
                                for item4 in tmp_share_img_url_list:
                                    tmp_img_div = r'<img src="{}" style="height:auto;width:100%;"/>'.format(item4)
                                    tmp_img_div_desc += tmp_img_div
                                my_img_div = '<div>' + tmp_img_div_desc + '</div>'
                                # print(my_img_div)

                                # 获取到goods_id 和 fisrt_text
                                share_url = 'https://wq.jd.com/shopgroup_feed/FeedDetail?shareid=' + feed_list_item.get('shareid', '') + '&g_tk=1975813451'
                                try:
                                    self.from_ip_pool_set_proxy_ip_to_phantomjs()
                                    self.driver.get(share_url)
                                    self.driver.implicitly_wait(15)
                                except Exception as e:  # 如果超时, 终止加载并继续后续操作
                                    print('-->>time out after 15 seconds when loading page')
                                    self.driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
                                    # pass
                                feed_detail_body = self.driver.page_source
                                feed_detail_body = re.compile(r'\n').sub('', feed_detail_body)
                                feed_detail_body = re.compile(r'\t').sub('', feed_detail_body)
                                feed_detail_body = re.compile(r'  ').sub('', feed_detail_body)

                                feed_data = re.compile(r'square\((.*)\)').findall(feed_detail_body)
                                # print(feed_data)

                                if feed_data != []:
                                    feed_data = feed_data[0]
                                    try:
                                        feed_data = json.loads(feed_data)
                                    except:
                                        print('json.loads转换feed_data失败，此处跳过!')
                                        break   # 跳出后执行后面的外层的else

                                    # 文章标题
                                    title = feed_data.get('feeddata', {}).get('title', '')
                                    title = re.compile(r'12.12').sub('', title)

                                    # 达人评论内容
                                    tmp_comment_content = feed_data.get('feeddata', {}).get('commentcontent', '')
                                    tmp_comment_content = re.compile(r'&amp;').sub('', tmp_comment_content)
                                    tmp_comment_content = re.compile(r'\n').sub('', tmp_comment_content)
                                    tmp_comment_content = re.compile(r'12.12').sub('', tmp_comment_content)
                                    tmp_comment_content = re.compile(r'11.11').sub('', tmp_comment_content)
                                    comment_content = tmp_comment_content

                                    if title == '':
                                        # 由于获取到title为空, 所有title = comment_content, 并把comment_content = ''
                                        title = comment_content
                                        comment_content = ''
                                    # print('该文章的标题为: ', title)
                                    # print('达人的评论内容为: ', comment_content)

                                    # first_text(文章的第一段评论内容)
                                    first_text = feed_data.get('feeddata', {}).get('firsttext', '')
                                    first_text = re.compile(r'12.12').sub('', first_text)
                                    first_text = re.compile(r'11.11').sub('', first_text)
                                    # print('first_text为: ', first_text)

                                    sku_id = feed_data.get('feeddata', {}).get('skuid')
                                    if sku_id == '0':
                                        # 如果sku_id = '0'表示没有sku_id
                                        sku_id = ''
                                    # print('sku_id为: ', sku_id)

                                    share_id = feed_list_item.get('shareid', '')
                                    tmp_div_body_dict = self.get_div_body(share_id=share_id)
                                    # pprint(tmp_div_body_dict)

                                    if tmp_div_body_dict['sku_info'] == [] and sku_id != '':
                                        # 表示如果tmp_div_body_dict['sku_info']为[]，则第二部分没有goods_id，所有将第一个sku_id赋值给sku_info
                                        goods_id_list = [{'goods_id': sku_id}]
                                    else:
                                        # 这篇文章推荐的商品goods_id的list(第一个为没有div_body时的goods_id)
                                        goods_id_list = [{'goods_id': item6} for item6 in tmp_div_body_dict['sku_info']]
                                    tmp_div_body = '<div>' + '<h3>{}</h3>'.format(title) + '<p>{}</p>'.format(comment_content) + my_img_div + tmp_div_body_dict['div_body']
                                    # print('该文章推荐的商品goods_id的list为: ', goods_id_list)
                                    # print(tmp_div_body)

                                else:
                                    print('获取feed_data失败!')
                                    return []

                                # 后期处理
                                if comment_content == '':
                                    comment_content = first_text

                                '''
                                时区处理，时间处理到上海时间
                                '''
                                tz = pytz.timezone('Asia/Shanghai')  # 创建时区对象
                                now_time = datetime.datetime.now(tz)
                                # 处理为精确到秒位，删除时区信息
                                now_time = re.compile(r'\..*').sub('', str(now_time))
                                # 将字符串类型转换为datetime类型
                                now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
                                create_time = now_time      # 创建的时间

                                result = {
                                    'nick_name': nick_name,                     # 达人昵称
                                    'head_url': head_url,                       # 达人头像
                                    'profile': profile,                         # 个性签名
                                    'share_id': share_id,                       # 分享的share_id
                                    'article_url': article_url,                 # 文章原地址
                                    'title': title,                             # 文章标题
                                    'comment_content': comment_content,         # 达人的评论内容
                                    'share_img_url_list': share_img_url_list,   # 达人自拍照片list
                                    # 'first_text': first_text,                   # 文章的第一段评论文字
                                    'goods_id_list':goods_id_list,              # 文章中所有推荐的商品的goods_id的list
                                    'div_body': tmp_div_body,                   # 文章主体div
                                    'create_time': create_time,                 # 文章创建的时间
                                }
                                # pprint(result)
                                print(result)
                                params = self._get_db_insert_params(item=result)
                                sql_str = r'insert into dbo.jd_youxuan_daren_recommend(nick_name, head_url, profile, share_id, gather_url, title, comment_content, share_img_url_list, goods_id_list, div_body, create_time) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                                my_pipeline._insert_into_table(sql_str=sql_str, params=params)

                                print('准备开始抓取该文章中的所有推荐商品'.center(30, '-'))
                                for i in goods_id_list:
                                    if i.get('goods_id', '') in db_goods_id:
                                        print('该goods_id({})已经存在于数据库中, 此处跳过!'.format(i.get('goods_id', '')))
                                        pass
                                    else:
                                        tmp_goods_id_url = 'https://item.jd.com/' + i.get('goods_id', '') + '.html'
                                        goods_id = jd.get_goods_id_from_url(jd_url=tmp_goods_id_url)
                                        jd.get_goods_data(goods_id=goods_id)
                                        tmp_jd_data = jd.deal_with_data(goods_id=goods_id)
                                        tmp_jd_data['spider_url'] = tmp_goods_id_url
                                        tmp_jd_data['username'] = '18698570079'
                                        tmp_jd_data['goods_id'] = goods_id[1]

                                        jd.insert_into_jd_table(data=tmp_jd_data, pipeline=my_pipeline)
                                print('该文章内推荐的商品全部抓取完毕'.center(30, '-'))

            else:
                print('body为空list!')

    def _get_db_insert_params(self, item):
        params = (
            item['nick_name'],
            item['head_url'],
            item['profile'],
            item['share_id'],
            item['article_url'],
            item['title'],
            item['comment_content'],
            dumps(item['share_img_url_list'], ensure_ascii=False),
            dumps(item['goods_id_list'], ensure_ascii=False),
            item['div_body'],
            item['create_time'],
        )

        return params

    def get_div_body(self, share_id):
        '''
        获取详细描述的div块(1. 有些share_id会有 2. 有些没有(没有的就是简单的单个描述后面跟自己的所有图片))
        :param share_id: 分享的id号
        :return:
        '''
        # https://storage.360buyimg.com/bigfeeds/6699435734675287505.jsonp
        # 设置代理ip
        self.proxies = self.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
        self.proxy = self.proxies['http'][randint(0, len(self.proxies) - 1)]

        tmp_proxies = {
            'http': self.proxy,
        }
        # print('------>>>| 正在使用代理ip: {} 进行爬取... |<<<------'.format(self.proxy))
        try:
            div_url = 'https://storage.360buyimg.com/bigfeeds/' + share_id + '.jsonp'
            # print(div_url)
            ## 用requests去请求待下载的文件
            response = requests.get(div_url, proxies=tmp_proxies, timeout=15, verify=True)
            div_body = response.content.decode('utf-8')
            # print(div_body)
            div_body = re.compile(r'\n').sub('', div_body)
            div_body = re.compile(r'\t').sub('', div_body)
            div_body = re.compile(r'  ').sub('', div_body)
            div_body = re.compile(r'try{ bigfeedCBK\((.*)\) }catch\(e\){}').findall(div_body)
        except Exception:
            print('requests.get()请求超时....')
            div_body = []
            pass

        if div_body != []:
            div_body = div_body[0]
            try:
                div_body = json.loads(div_body)
                # pprint(div_body)
            except:
                div_body = '{}'

            if div_body != {}:
                try:
                    sku_info = div_body.get('skuinfo', '[]')
                    sku_info = json.loads(sku_info)
                    # print(sku_info)
                except:
                    print('json.loads转换sku_info出错')
                    sku_info = []
                    pass
                sku_info = [item3.get('skuId') for item3 in sku_info]
                # print(sku_info)

                '''
                处理div_body
                '''
                try:
                    tmp_div_body = div_body.get('content', '')
                    tmp_div_body = re.compile(r'&nbsp;').sub(' ', tmp_div_body)
                    tmp_div_body = re.compile(r'京东').sub('', tmp_div_body)
                    tmp_div_body = re.compile(r'12.12').sub('', tmp_div_body)
                    # * 此处替换的是最后面的推荐商品(都是一行一个推荐的那种)后期要插入咱们的商品就可以在<a data-item="href"></a>中进行插入 *
                    tmp_div_body = re.compile(r'<a data-item="href".*?>.*?</a>')\
                        .sub('<a data-item=\"href\"></a>', tmp_div_body)
                    # * 多个goods_list的时候，非一行一行推荐而是一行好几个goods_id的时候的情况(是script动态生成的所以没法替换)
                    tmp_div_body = re.compile(r'<a class="feedback_coll_goods_item".*?>.*?</a>')\
                        .sub('<a class=\"feedback_coll_goods_item\"></a>', tmp_div_body)
                    # tmp_div_body = re.compile(r'<div class="feedback_coll_goods.*?>.*?</div>')\
                    #     .sub('<div class=\"feedback_coll_goods\"></div>', tmp_div_body)
                    div_body = '<div>' + tmp_div_body + '</div>'
                except AttributeError as e:
                    print('div_body获取content时出错如下: ', e)
                    div_body = ''

            else:
                sku_info = []
                div_body = ''

        else:
            sku_info = []
            div_body = ''
        # print(div_body)

        result = {
            'sku_info': sku_info,
            'div_body': div_body,
        }
        return result

    def init_phantomjs(self):
        """
        初始化带cookie的驱动，之所以用phantomjs是因为其加载速度很快(快过chrome驱动太多)
        """
        '''
        研究发现, 必须以浏览器的形式进行访问才能返回需要的东西
        常规requests模拟请求会被服务器过滤, 并返回请求过于频繁的无用页面
        '''
        print('--->>>初始化phantomjs驱动中<<<---')
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap['phantomjs.page.settings.resourceTimeout'] = 1000  # 1秒
        cap['phantomjs.page.settings.loadImages'] = False
        cap['phantomjs.page.settings.disk-cache'] = True
        cap['phantomjs.page.settings.userAgent'] = get_random_pc_ua()  # 随机一个请求头
        # cap['phantomjs.page.customHeaders.Cookie'] = cookies
        tmp_execute_path = EXECUTABLE_PATH

        self.driver = webdriver.PhantomJS(executable_path=tmp_execute_path, desired_capabilities=cap)

        wait = ui.WebDriverWait(self.driver, 15)  # 显示等待n秒, 每过0.5检查一次页面是否加载完毕
        print('------->>>初始化完毕<<<-------')

    def from_ip_pool_set_proxy_ip_to_phantomjs(self):
        ip_list = self.get_proxy_ip_from_ip_pool().get('http')
        proxy_ip = ''
        try:
            proxy_ip = ip_list[randint(0, len(ip_list) - 1)]        # 随机一个代理ip
        except Exception:
            print('从ip池获取随机ip失败...正在使用本机ip进行爬取!')
        # print('------>>>| 正在使用的代理ip: {} 进行爬取... |<<<------'.format(proxy_ip))
        proxy_ip = re.compile(r'http://').sub('', proxy_ip)     # 过滤'http://'
        proxy_ip = proxy_ip.split(':')                          # 切割成['xxxx', '端口']

        try:
            tmp_js = {
                'script': 'phantom.setProxy({}, {});'.format(proxy_ip[0], proxy_ip[1]),
                'args': []
            }
            self.driver.command_executor._commands['executePhantomScript'] = ('POST', '/session/$sessionId/phantom/execute')
            self.driver.execute('executePhantomScript', tmp_js)
        except Exception:
            print('动态切换ip失败')
            pass

    def get_proxy_ip_from_ip_pool(self):
        '''
        从代理ip池中获取到对应ip
        :return: dict类型 {'http': ['http://183.136.218.253:80', ...]}
        '''
        base_url = 'http://127.0.0.1:8000'
        result = requests.get(base_url).json()

        result_ip_list = {}
        result_ip_list['http'] = []
        for item in result:
            if item[2] > 7:
                tmp_url = 'http://' + str(item[0]) + ':' + str(item[1])
                result_ip_list['http'].append(tmp_url)
            else:
                delete_url = 'http://127.0.0.1:8000/delete?ip='
                delete_info = requests.get(delete_url + item[0])
        # pprint(result_ip_list)
        return result_ip_list

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass
        gc.collect()


def daemon_init(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    '''
    杀掉父进程，独立子进程
    :param stdin:
    :param stdout:
    :param stderr:
    :return:
    '''
    sys.stdin = open(stdin, 'r')
    sys.stdout = open(stdout, 'a+')
    sys.stderr = open(stderr, 'a+')
    try:
        pid = os.fork()
        if pid > 0:     # 父进程
            os._exit(0)
    except OSError as e:
        sys.stderr.write("first fork failed!!" + e.strerror)
        os._exit(1)

    # 子进程， 由于父进程已经退出，所以子进程变为孤儿进程，由init收养
    '''setsid使子进程成为新的会话首进程，和进程组的组长，与原来的进程组、控制终端和登录会话脱离。'''
    os.setsid()
    '''防止在类似于临时挂载的文件系统下运行，例如/mnt文件夹下，这样守护进程一旦运行，临时挂载的文件系统就无法卸载了，这里我们推荐把当前工作目录切换到根目录下'''
    os.chdir("/")
    '''设置用户创建文件的默认权限，设置的是权限“补码”，这里将文件权限掩码设为0，使得用户创建的文件具有最大的权限。否则，默认权限是从父进程继承得来的'''
    os.umask(0)

    try:
        pid = os.fork()  # 第二次进行fork,为了防止会话首进程意外获得控制终端
        if pid > 0:
            os._exit(0)  # 父进程退出
    except OSError as e:
        sys.stderr.write("second fork failed!!" + e.strerror)
        os._exit(1)

    # 孙进程
    #   for i in range(3, 64):  # 关闭所有可能打开的不需要的文件，UNP中这样处理，但是发现在python中实现不需要。
    #       os.close(i)
    sys.stdout.write("Daemon has been created! with pid: %d\n" % os.getpid())
    sys.stdout.flush()  # 由于这里我们使用的是标准IO，这里应该是行缓冲或全缓冲，因此要调用flush，从内存中刷入日志文件。

def just_fuck_run():
    while True:
        print('一次大更新即将开始'.center(30, '-'))
        tmp = JdTalentRecommend()
        tmp.get_all_user_and_their_recommend_goods_list()
        try:
            del tmp
        except:
            pass
        gc.collect()
        print('一次大更新完毕'.center(30, '-'))

def main():
    '''
    这里的思想是将其转换为孤儿进程，然后在后台运行
    :return:
    '''
    print('========主函数开始========')  # 在调用daemon_init函数前是可以使用print到标准输出的，调用之后就要用把提示信息通过stdout发送到日志系统中了
    daemon_init()  # 调用之后，你的程序已经成为了一个守护进程，可以执行自己的程序入口了
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    # time.sleep(10)  # daemon化自己的程序之后，sleep 10秒，模拟阻塞
    just_fuck_run()

if __name__ == '__main__':
    if JD_YOUXUAN_DAREN_IS_BACKGROUND_RUNNING:
        main()
    else:
        just_fuck_run()
