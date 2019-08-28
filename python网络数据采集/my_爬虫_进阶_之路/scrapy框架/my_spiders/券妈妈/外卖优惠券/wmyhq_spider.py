# coding:utf-8

'''
@author = super_fazai
@File    : wmyhq_spider.py
@Time    : 2017/7/19 10:50
@connect : superonesfazai@gmail.com
'''

"""
券妈妈外卖优惠券spider:[每日可用]
"""

from pprint import pprint
from time import sleep
import gc
from scrapy.selector import Selector
import os

from fzutils.spider.fz_requests import MyRequests
from fzutils.spider.fz_phantomjs import MyPhantomjs
from fzutils.internet_utils import get_random_phone_ua
from fzutils.common_utils import (
    json_2_dict,
    save_base64_img_2_local,)

class WMYHQSpider(object):
    def __init__(self):
        self._set_headers()
        self.page_sleep_time = 1.2
        self.phantomjs_sleep_time = 2
        self.my_phantomjs = MyPhantomjs(load_images=True)   # load_images为True才加载图片!
        self.qrcode_base_path = '/Users/afa/myFiles/tmp/外卖券qrcode/'

    def _set_headers(self):
        self.headers = {
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'br, gzip, deflate',
            'Host': 'app.quanmama.com',
            'User-Agent': get_random_phone_ua(),
            'Content-Length': '885',
            'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
        }

    def _get_wm_page_info(self):
        '''
        获取外卖页面的json推荐
        :return:
        '''
        # cookies = {
        #     'ASP.NET_SessionId': 'rxnstx4qhayrkqdne3coeevj',
        # }
        all_rows = []
        print('开始采集券妈妈外卖券!')
        for page_index in range(1, 5):
            print('正在抓取第{0}页...'.format(page_index))
            data = self._set_data(page_index=page_index)

            url = 'https://app.quanmama.com/apios/v5/appZdmList.ashx'
            body = MyRequests.get_url_body(method='post', url=url, headers=self.headers, cookies=None, data=data)
            # print(body)
            if body == '':
                print('获取到的body为空值!此处跳过!')
                continue
            # print(body)

            rows = json_2_dict(json_str=body).get('data', {}).get('rows', [])
            if rows == []:
                print('得到的rows为空值!此处跳过!')
                continue
            # pprint(rows)

            all_rows += rows
            sleep(self.page_sleep_time)

        print('\n@@@@@@ 抓取完毕!')
        wm_list = self._parse_wm_page(all_rows)
        # pprint(wm_list)

        self._deal_with_wm_info(wm_list)

    def _deal_with_wm_info(self, wm_list):
        '''
        处理wm_list
        :param wm_list:
        :return:
        '''
        # 先清空昨日的
        os.system('cd {0} && rm -rf *'.format(self.qrcode_base_path))
        for item in wm_list:
            print('正在处理文章id: {0}'.format(item.get('article_id')))

            exec_code = '''
            self.driver.find_element_by_css_selector('div.go-action a').send_keys(Keys.ENTER)
            sleep({0})
            '''.format(self.phantomjs_sleep_time)
            body = self.my_phantomjs.get_url_body(
                url=item.get('article_link', ''),
                exec_code=exec_code)
            # div.appcoupon-qrcode img

            qrcode_str = Selector(text=body).css('div.appcoupon-qrcode img::attr("src")').extract_first()
            # print(qrcode_str)

            img_file_name = '[代码{0}]'.format(item.get('article_id', '')) + \
                            item.get('article_title', '') + '@' + \
                            item.get('article_vicetitle', '') + '.png'
            save_path = self.qrcode_base_path + img_file_name
            result = save_base64_img_2_local(save_path=save_path, base64_img_str=qrcode_str)
            if result:
                print('[+] {0}'.format(img_file_name))
            else:
                print('[-] {0}'.format(img_file_name))

            sleep(self.page_sleep_time)

        print('@@@ 抓取二维码操作完成!')

        return None

    def _parse_wm_page(self, rows):
        '''
        :param rows:
        :return:
        '''
        _ = []
        for item in rows:
            try:
                article_is_timeout = item.get('article_is_timeout')
                assert article_is_timeout is not None, 'article_is_timeout为None!'
                if article_is_timeout == 1:     # 0 未过期; 1过期
                    continue

                article_id = item.get('article_id')
                assert article_id is not None, 'article_id为空!'

                article_mall = item.get('article_mall', '')
                assert article_mall != '', 'article_mall为空值!'

                article_pic = item.get('article_pic', '')
                assert  article_pic != '', 'article_pic为空值!'

                article_vicetitle = self.replace_chinese_str(item.get('article_vicetitle', ''))
                assert article_vicetitle != '', 'article_vicetitle为空值!'

                article_title = self.replace_chinese_str(item.get('article_title', ''))
                assert article_title != '', 'article_title为空值!'

                article_link = item.get('article_link', '')
                assert article_link != '', 'article_link为空值!'

                article_begin_time = item.get('article_begintime', '')
                assert article_begin_time != '', 'article_begin_time为空值!'

                article_end_time = item.get('article_endtime', '')
                assert article_end_time != '', 'article_end_time为空值!'


            except Exception as e:
                print('遇到错误:', e)
                continue

            _.append({
                'article_id': article_id,                   # 文章id
                'article_mall': article_mall,               # 文章发布至今多久
                'article_pic': article_pic,                 # 文章缩略图
                'article_vicetitle': article_vicetitle,     # 文章子标题
                'article_title': article_title,             # 文章标题
                'article_link': article_link,               # 文章link
                'article_begin_time': article_begin_time,   # 活动开始时间
                'article_end_time': article_end_time,       # 活动结束时间
            })

        return _

    def replace_chinese_str(self, data):
        '''
        replace 中文符号
        :param data:
        :return:
        '''

        return data.replace('：', ':').replace('、', ',').replace('，', ',').replace('/', '|')

    def _set_data(self, page_index):
        '''
        post的data参数
        :return:
        '''
        data = [
            ('AgeType', '2'),
            ('ProfessionType', '2'),
            ('SexType', '1'),
            ('appname', '券妈妈'),
            ('category', '5391'),
            ('code', '532'),
            ('devicename', 'iOS'),
            ('f', 'ios'),
            ('identifiernumber', 'F037B84D-A211-44B3-BA56-D5033A1328D4'),
            # ('imei', 'DA8C3A83-C08C-4881-86A8-1E67849F5BB2'),
            ('isiosmajia', '0'),
            ('localScheme', 'qmm'),
            ('logintype', '4'),
            ('mac', '02:00:00:00:00:00'),
            ('net', '2'),
            ('pageindex', str(page_index)),
            ('phonemodel', 'iPhone'),
            ('phoneversion', '11.0'),
            ('platform', 'App Store'),
            ('rtime', '0_'),
            ('sort', '1'),
            ('test', '0'),
            # ('userphonename', '\uD83D\uDC79\uD83D\uDC79\uD83D\uDC79\uD83D\uDC79\uD83D\uDC79\uD83D\uDC79\uD83D\uDC79'),
            # ('usertoken', '09EAD2E9E9DD9BC28F7C26D004062CA57AD0B2FAD785BBAF2E47EA62C988583E6EB9759E8BD401086322FD88EE3C741CB015E4AE3ADE06EC8FF1F188CF647C4BDA41DD1A3A8D8E20DBFA4E6DB4DCDC9588ACBE676B0EF6F66A137BEDD1B51FC8157FDD1FBC34CCACA97DF5ACE152C83494903ED1CBEEAA283856534EEAB79D678CDC3E6A2FEA9DE2463DCB5D8D61F3D365E2971E17720EDBDC4E0A218616B79ADBD4D86C5BD89C67B8A008DA67139EFD4954DD44301BE380DE25093C216928F7'),
            ('v', '5.3.2'),
        ]

        return data

    def __del__(self):
        try:
            del self.my_phantomjs
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    _ = WMYHQSpider()
    _._get_wm_page_info()
    del _