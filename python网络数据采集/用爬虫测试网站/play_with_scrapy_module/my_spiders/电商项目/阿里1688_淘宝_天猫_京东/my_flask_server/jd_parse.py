# coding:utf-8

'''
@author = super_fazai
@File    : jd_parse.py
@Time    : 2017/11/9 10:41
@connect : superonesfazai@gmail.com
'''

"""
可对应爬取京东常规商品，京东超市，京东秒杀
"""

from settings import HEADERS
from settings import PHANTOMJS_DRIVER_PATH

from random import randint
import requests, json, re, time
from time import sleep
from decimal import Decimal
import datetime
import gc
import pytz
from pprint import pprint

from selenium import webdriver
import selenium.webdriver.support.ui as ui

# phantomjs驱动地址
EXECUTABLE_PATH = PHANTOMJS_DRIVER_PATH

class JdParse(object):
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'acs.m.taobao.com',
            'User-Agent': HEADERS[randint(0, 34)]      # 随机一个请求头
        }
        self.result_data = {}

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
        cap['phantomjs.page.settings.userAgent'] = HEADERS[randint(0, 34)]  # 随机一个请求头
        # cap['phantomjs.page.customHeaders.Cookie'] = cookies
        tmp_execute_path = EXECUTABLE_PATH

        self.driver = webdriver.PhantomJS(executable_path=tmp_execute_path, desired_capabilities=cap)

        wait = ui.WebDriverWait(self.driver, 15)  # 显示等待n秒, 每过0.5检查一次页面是否加载完毕
        print('------->>>初始化完毕<<<-------')
        
    def get_goods_data(self, goods_id):
        '''
        模拟构造得到data的url
        :param goods_id:
        :return: data   类型dict
        '''
        phone_url = 'https://item.m.jd.com/ware/view.action?wareId=' + str(goods_id)
        print('------>>>| 得到的移动端地址为: ', phone_url)

        # 用于得到常规信息
        tmp_url = 'https://item.m.jd.com/ware/detail.json?wareId=' + str(goods_id)

        self.from_ip_pool_set_proxy_ip_to_phantomjs()
        self.driver.set_page_load_timeout(15)       # 设置成15秒避免数据出错

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

        body_1 = re.compile(r'<pre.*?>(.*)</pre>').findall(body)
        if body_1 != []:
            data = body_1[0]
            data = json.loads(data)
            # pprint(data)
            wdis = data.get('wdis', '') # 图文描述
            data = data.get('ware', {})
            try:
                data.pop('wdisHtml')
                data.get('wi', {})['afterServiceList'] = []
            except Exception:
                pass

            # 处理'wi' 'code'
            code = data.get('wi', {}).get('code', '')
            if code != '':
                code = json.loads(code)
                data.get('wi', {})['code'] = code

            # 处理wdis
            data['wdis'] = wdis

            if data != {}:
                self.result_data = data
                # pprint(data)
                return data
            else:
                print('获取到的data的key值ware为空!')
                return {}

        else:
            print('获取到的data为空!')
            return {}

    def deal_with_data(self, goods_id):
        '''
        处理result_data, 返回需要的信息
        :return: 字典类型
        '''
        data = self.result_data
        if data != {}:
            # 店铺名称
            had_shop_name = data.get('shopInfo', {}).get('shop')  # 店铺名字有为空的情况
            if had_shop_name is not None:
                shop_name = data.get('shopInfo', {}).get('shop', {}).get('name', '')
            else:
                shop_name = ''

            # 掌柜
            account = ''

            # 商品名称
            title = data.get('wname', '')

            # 子标题
            sub_title = ''

            # 店铺主页地址
            # 商品库存

            # 商品标签属性名称,  以及商品标签属性对应的值(这个先不做)
            detail_name_list = []
            if data.get('skuColorSize', {}).get('colorSizeTitle', {}) != {}:
                tmp_detail_name_list = data.get('skuColorSize', {}).get('colorSizeTitle', {})
                for key in tmp_detail_name_list.keys():
                    tmp = {}
                    tmp['spec_name'] = tmp_detail_name_list[key]
                    detail_name_list.append(tmp)
            # print(detail_name_list)

            '''
            要存储的每个标签对应规格的价格及其库存(京东无库存抓取, 只有对应规格商品是否可买)
            '''
            # tmp_price_info_list = data.get('skuColorSize', {}).get('colorSize')
            # pprint(tmp_price_info_list)

            price_info_list = []
            if detail_name_list != []:   # 有规格
                tmp_price_info_list = data.get('skuColorSize', {}).get('colorSize')
                # pprint(tmp_price_info_list)
                if tmp_price_info_list is not None:
                    for item in tmp_price_info_list:
                        tmp = {}
                        tmp_spec_value = []
                        if item.get('color') != '*':
                            tmp_spec_value.append(item.get('color'))

                        if item.get('size') != '*':
                            tmp_spec_value.append(item.get('size'))

                        if item.get('spec') != '*':
                            tmp_spec_value.append(item.get('spec'))

                        tmp_spec_value = '|'.join(tmp_spec_value)   # 具体规格
                        # print(tmp_spec_value)

                        sku_id = item.get('skuId')
                        # 对每个sku_id就行一次请求，来获得对应sku_id的价格数据
                        ware_price = self.from_ware_id_get_price_info(ware_id=sku_id)

                        tmp['spec_value'] = tmp_spec_value
                        tmp['detail_price'] = ware_price
                        tmp['rest_number'] = ''
                        tmp['img'] = item.get('image')
                        price_info_list.append(tmp)
            # pprint(price_info_list)

            # 商品价格
            '''
            最高价和最低价处理   从已经获取到的规格对应价格中筛选最高价和最低价即可
            '''
            if detail_name_list == []:  # 说明没有规格，所有价格只能根据当前的goods_id来获取
                price = round(float(self.from_ware_id_get_price_info(ware_id=goods_id)), 2)
                taobao_price = price
            else:
                tmp_price_list = sorted([round(float(item.get('detail_price', '')), 2) for item in price_info_list])
                # print(tmp_price_list)
                if tmp_price_list != []:
                    price = tmp_price_list[-1]
                    taobao_price = tmp_price_list[0]
                else:
                    print('获取最高价最低价时错误')
                    return {}
            # print('最高价: ', price)
            # print('最低价: ', taobao_price)

            # 所有示例图片地址
            if data.get('images') is not None:
                all_img_url = [{
                    'img_url': item.get('bigpath')
                } for item in data.get('images')]
            else:
                all_img_url = []
            # pprint(all_img_url)

            # 详细信息标签名对应属性
            tmp_p_info = data.get('wi', {}).get('code')
            p_info = []
            if tmp_p_info is not None:
                for item in tmp_p_info:
                    tmp = {}
                    tmp['p_name'] = list(item.keys())[0]
                    tmp['p_value'] = list(item.values())[0]
                    p_info.append(tmp)
            else:
                p_info = []
            # pprint(p_info)      # 爬取是手机端的所以没有第一行的，就是手机端的规格

            '''
            详细描述 div_desc
            '''
            wdis = ''
            # 特殊处理script动态生成的
            if data.get('popWareDetailWebViewMap') is not None:
                if data.get('popWareDetailWebViewMap').get('cssContent') is not None:
                    wdis = data.get('popWareDetailWebViewMap', {}).get('cssContent', '')
                    wdis = re.compile(r'&lt;').sub('<',
                                                   wdis)  # self.driver.page_source转码成字符串时'<','>'都被替代成&gt;&lt;此外还有其他也类似被替换
                    wdis = re.compile(r'&gt;').sub('>', wdis)
                    wdis = re.compile(r'&amp;').sub('&', wdis)
                    wdis = re.compile(r'&nbsp;').sub(' ', wdis)
                    wdis = re.compile(r'src=\"https:').sub('src=\"', wdis)  # 先替换部分带有https的
                    wdis = re.compile(r'src="').sub('src=\"https:', wdis)  # 再把所欲的换成https的

            wdis = wdis + data.get('wdis', '')      # 如果获取到script就与wdis重组
            wdis = re.compile(r'&lt;').sub('<', wdis)  # self.driver.page_source转码成字符串时'<','>'都被替代成&gt;&lt;此外还有其他也类似被替换
            wdis = re.compile(r'&gt;').sub('>', wdis)
            wdis = re.compile(r'&amp;').sub('&', wdis)
            wdis = re.compile(r'&nbsp;').sub(' ', wdis)
            wdis = re.compile(r'src=\"https:').sub('src=\"', wdis)  # 先替换部分带有https的
            wdis = re.compile(r'src="').sub('src=\"https:', wdis)  # 再把所欲的换成https的
            div_desc = wdis
            # print(div_desc)

            '''
            是否下架判断
            '''
            is_delete = 0

            result = {
                'shop_name': shop_name,                 # 店铺名称
                'account': account,                     # 掌柜
                'title': title,                         # 商品名称
                'sub_title': sub_title,                 # 子标题
                'price': price,                         # 商品价格
                'taobao_price': taobao_price,           # 淘宝价
                # 'goods_stock': goods_stock,             # 商品库存
                'detail_name_list': detail_name_list,   # 商品标签属性名称
                # 'detail_value_list': detail_value_list, # 商品标签属性对应的值
                'price_info_list': price_info_list,     # 要存储的每个标签对应规格的价格及其库存(京东隐藏库存无法爬取，只能能买或不能买)
                'all_img_url': all_img_url,             # 所有示例图片地址
                'p_info': p_info,                       # 详细信息标签名对应属性
                # 'pc_div_url': pc_div_url,  # pc端描述地址
                'div_desc': div_desc,  # div_desc
                'is_delete': is_delete,  # 是否下架判断
            }
            pprint(result)
            # print(result)
            # wait_to_send_data = {
            #     'reason': 'success',
            #     'data': result,
            #     'code': 1
            # }
            # json_data = json.dumps(wait_to_send_data, ensure_ascii=False)
            # print(json_data)
            gc.collect()
            return result

        else:
            print('待处理的data为空的dict')
            return {}

    def from_ware_id_get_price_info(self, ware_id):
        '''
        得到价格信息，由于过滤了requests所以用phantomjs
        '''
        price_url = 'https://item.m.jd.com/ware/getSpecInfo.json?wareId=' + str(ware_id)

        self.from_ip_pool_set_proxy_ip_to_phantomjs()   # 每次都动态换代理ip比较危险感觉，容易跑死, 但是也不可能拿裸机ip进行爬取，京东有点坑哦，嘿嘿！
        self.driver.set_page_load_timeout(15)  # 设置成15秒避免数据出错

        try:
            self.driver.get(price_url)
            self.driver.implicitly_wait(12)
        except Exception as e:  # 如果超时, 终止加载并继续后续操作
            print('-->>time out after 12 seconds when loading page')
            self.driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
            # pass
        price_body = self.driver.page_source
        price_body = re.compile(r'\n').sub('', price_body)
        price_body = re.compile(r'\t').sub('', price_body)
        price_body = re.compile(r'  ').sub('', price_body)
        # print(price_body)

        price_body_1 = re.compile(r'<pre.*?>(.*)</pre>').findall(price_body)
        if price_body_1 != []:
            price_data = price_body_1[0]
            price_data = json.loads(price_data)
            try:
                price_data.pop('defaultAddress')
                price_data.pop('commonConfigJson')
            except Exception:
                pass
            try:
                price_data.pop('newYanBaoInfo')
            except Exception:
                pass

            # 处理newYanBaoInfo
            new_yan_bao_info = price_data.get('newYanBaoInfo')
            if new_yan_bao_info is not None:
                new_yan_bao_info = json.loads(new_yan_bao_info)
                price_data['newYanBaoInfo'] = new_yan_bao_info

            # 处理allColorSet
            all_color_set = price_data.get('allColorSet')
            if all_color_set is not None:
                all_color_set = json.loads(all_color_set)
                price_data['allColorSet'] = all_color_set

            # 处理allSpecSet
            all_spec_set = price_data.get('allSpecSet')
            if all_spec_set is not None:
                all_spec_set = json.loads(all_spec_set)
                price_data['allSpecSet'] = all_spec_set

            # 处理allSizeSet
            all_size_set = price_data.get('allSizeSet')
            if all_size_set is not None:
                all_size_set = json.loads(all_size_set)
                price_data['allSizeSet'] = all_size_set

            # pprint(price_data)
            return price_data.get('warePrice', '')
        else:
            # print('获取到的price_data为空!')
            return ''

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
    
    def get_goods_id_from_url(self, jd_url):
        # https://detail.1688.com/offer/559526148757.html?spm=b26110380.sw1688.mof001.28.sBWF6s
        is_jd_url = re.compile(r'https://item.jd.com/.*?').findall(jd_url)
        if is_jd_url != []:
            goods_id = re.compile(r'https://item.jd.com/(.*?).html.*?').findall(jd_url)[0]
            print('------>>>| 得到的京东商品id为:', goods_id)
            return goods_id
        else:
            print('京东商品url错误, 非正规的url, 请参照格式(https://item.jd.com/)开头的...')
            return ''

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    jd = JdParse()
    while True:
        jd_url = input('请输入待爬取的京东商品地址: ')
        jd_url.strip('\n').strip(';')
        goods_id = jd.get_goods_id_from_url(jd_url)
        data = jd.get_goods_data(goods_id=goods_id)
        jd.deal_with_data(goods_id=goods_id)
        