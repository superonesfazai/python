# coding:utf-8

'''
@author = super_fazai
@File    : tmp.py
@Time    : 2017/9/22 13:24
@connect : superonesfazai@gmail.com
'''

from urllib2 import Request, urlopen
from urllib2 import HTTPError
import json
from pprint import pprint
import time
import openpyxl
import os


class ShanDongEnvir(object):
    def __init__(self):
        self.city_deal_info_items = []
        self.is_alive = True

    def save_excel(self):
        result = self.city_deal_info_items

        if os.path.exists('datas'):
            save_path = os.getcwd() + '/datas/'

            now_year = time.localtime().tm_year
            now_month = time.localtime().tm_mon
            now_day = time.localtime().tm_mday
            now_hour = time.localtime().tm_hour
            file_name = '%d年%d月%d号_%d时_的数据' % (now_year, now_month, now_day, now_hour)

            wb = openpyxl.Workbook()  # class实例化
            ws = wb.active  # 激活工作表

            ws.append(
                ['city_name', 'area_name', 'pname', 'subid', 'AQI', '首要污染物', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'])
            for i in range(0, len(result) - 1):
                ws.append([
                    result[i]['city_name'].encode('utf-8').decode('utf-8'),
                    result[i]['area_name'],
                    result[i]['pname'],
                    result[i]['subid'],
                    result[i]['api'],
                    result[i]['pol'],
                    result[i]['pm25'],
                    result[i]['pm10'],
                    result[i]['so2'],
                    result[i]['no2'],
                    result[i]['co'],
                    result[i]['o3']
                ])

            wb.save(save_path + '%s.xls' % file_name)
            print file_name + '文件保存完毕!'

        else:
            os.mkdir('datas')


    def run_forever(self):
        now_year = time.localtime().tm_year
        now_month = time.localtime().tm_mon
        now_day = time.localtime().tm_mday
        now_hour = time.localtime().tm_hour

        print ('正在进行爬取 %d年%d月%d日 %d时的数据' % (now_year, now_month, now_day, now_hour)).center(50, '*')

        tmp_url = 'http://58.56.98.78:8801/AirDeploy.Web/Ajax/AirQuality/AirQuality.ashx?Method=GetStationMarkOnMap&date=0.4310850290974302'
        tmp_request = Request(tmp_url)

        try:
            tmp_response = urlopen(tmp_request)
        except HTTPError as e:
            self.is_alive = False

            print '无网络连接...无法继续爬取...'
            self.sendSMS()
        else:
            if tmp_response == '':
                print 'response为空值'
                self.sendSMS()
            else:
                city_info_json = json.loads(tmp_response.read())

                # pprint(city_info_json)
                items = city_info_json['items']
                # pprint(items)
                for i in range(len(items)-1):
                    city_deal_info_item = {}
                    city_deal_info_item['city_name'] = items[i]['cityName']
                    city_deal_info_item['area_name'] = items[i]['areaName']
                    city_deal_info_item['subid'] = items[i]['subid']
                    city_deal_info_item['pname'] = items[i]['pname']

                    # 获取细节气象数据
                    url = 'http://58.56.98.78:8801/AirDeploy.Web/Ajax/AirQuality/AirQuality.ashx?Method=GetQualityItemsValues&StationID=%s' % city_deal_info_item['subid']
                    request = Request(url)
                    response = urlopen(request)
                    deal_json = json.loads(response.read())
                    # pprint deal_json
                    try:
                        print city_deal_info_item['subid']   # 用于测试得出官方未提供某数据的subid
                        city_deal_info_item['api'] = deal_json['AQI']
                        city_deal_info_item['pol'] = deal_json['POL'].strip()
                        try:
                            city_deal_info_item['pm25'] = '%.f' % (float(deal_json['PM25']) * 1000)
                        except Exception, e:
                            city_deal_info_item['pm25'] = '官方提供数据为空'
                        try:
                            city_deal_info_item['pm10'] = '%.f' % (float(deal_json['PM10']) * 1000)
                        except Exception, e:
                            city_deal_info_item['pm10'] = '官方提供数据为空'
                        try:
                            city_deal_info_item['so2'] = '%.f' % (float(deal_json['SO2']) * 1000)
                        except Exception, e:
                            city_deal_info_item['so2'] = '官方提供数据为空'
                        try:
                            city_deal_info_item['no2'] = '%.f' % (float(deal_json['NO2']) * 1000)
                        except Exception, e:
                            city_deal_info_item['no2'] = '官方提供数据为空'
                        try:
                            city_deal_info_item['co'] = float(deal_json['CO'])
                        except Exception, e:
                            city_deal_info_item['co'] = '官方提供数据为空'
                        try:
                            city_deal_info_item['o3'] = '%.f' % (float(deal_json['O3']) * 1000)
                        except Exception, e:
                            city_deal_info_item['o3'] = '官方提供数据为空'

                        print city_deal_info_item

                        self.city_deal_info_items.append(city_deal_info_item)

                    except Exception as e:
                        print e
                print '这个点的数据已经爬取完毕'.center(50, '*')
                # print self.city_deal_info_items

    # def sendSMS(self):
    #     '''
    #     这是我用自己短信api
    #     :return:
    #     '''
    #     from twilio.rest import Client
    #
    #     # 下面认证信息的值在你得twilio账户里可以找到
    #     account_sid = 'ACxxxxxxxxxd'
    #     auth_token = 'ee504a7c6xxxxxxxxxxb56435420220d'
    #
    #     client = Client(account_sid, auth_token)
    #
    #     message = client.messages.create(
    #         # to = '+8615661611306',
    #         to='+8615661611306',
    #         from_='+16506812561',
    #         body='大哥，您的爬虫(ID=山东省城市环境空气质量小爬虫)不跑了，请检查!'
    #     )

    def sendSMS(self):
        '''
        下面是吴哥公司短信api,由于我无法测试，还得吴哥自己测试
        :return:
        '''

        import urllib2
        url = 'http://m.5c.com.cn/api/send/index.php'  # 如连接超时，可能是您服务器不支持域名解析，请将下面连接中的：【m.5c.com.cn】修改为IP：【115.28.23.78】
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        encode = 'UTF-8'  # 页面编码和短信内容编码为GBK。重要说明：如提交短信后收到乱码，请将GBK改为UTF-8测试。如本程序页面为编码格式为：ASCII/GB2312/GBK则该处为GBK。如本页面编码为UTF-8或需要支持繁体，阿拉伯文等Unicode，请将此处写为：UTF-8
        username = 'filter'  # 用户名
        password_md5 = '1ADBB3178591FD5BB0C248518F39BF6D'  # 32位MD5密码加密，不区分大小写
        apikey = '36e74088db48842ce54ee65643b8667a'  # apikey秘钥（请登录 http://m.5c.com.cn 短信平台-->账号管理-->我的信息 中复制apikey）
        mobile = '18610310068'  # 手机号,只发一个号码：13800000001。发多个号码：13800000001,13800000002,...N 。使用半角逗号分隔。
        content = '大哥，您的爬虫(ID=山东省城市环境空气质量小爬虫)不跑了，请检查!'  # 要发送的短信内容，特别注意：签名必须设置，网页验证码应用需要加添加【图形识别码】。
        values = {
            'username': username,
            'password_md5': password_md5,
            'apikey': apikey,
            'mobile': mobile,
            'content': content,
            'encode': encode
        }

        headers = {
            'User-Agent': user_agent
        }

        data = urllib2.parse.urlencode(values)
        req = urllib2.Request(url + '?' + data)
        response = urllib2.urlopen(req)
        the_page = response.read()
        print the_page

if __name__ == '__main__':
    envir = ShanDongEnvir()

    while True:
        envir.run_forever()
        envir.save_excel()
        time.sleep(3600)

