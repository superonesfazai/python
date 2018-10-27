# coding:utf-8

'''
@author = super_fazai
@File    : ctrip_spider.py
@connect : superonesfazai@gmail.com
'''

"""
携程爬虫
"""

from gc import collect
from fzutils.ip_pools import sesame_ip_pool
from fzutils.spider.async_always import *

class CtripSpider(object):
    def __init__(self):
        self.loop = get_event_loop()

    async def _get_pc_headers(self):
        return {
            'Origin': 'http://hotels.ctrip.com',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': get_random_pc_ua(),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'Cache-Control': 'max-age=0',
            # 'Referer': 'http://hotels.ctrip.com/hotel/shanghai2',
            'Connection': 'keep-alive',
            'If-Modified-Since': 'Thu, 01 Jan 1970 00:00:00 GMT',
        }

    async def _search_hotels_by_pc(self):
        '''
        pc端hotel 搜索
        :return:
        '''
        # TODO 详细请求结果, 可以根据修改data获取
        data = {
            'AllHotelIds': '428365,1496646,393916,473770,4399431,13926223,6874402,15018492,12782071,15018773,8857430,18431318,6245432,436581,16197084,17504638,6338488,1073814,436187,4119594,1583084,437892,6082325,397163,387009',
            'BRev': '',
            'CorpPayType': '',
            'CtripService': '',
            'DealSale': '',
            'DepTime': '2018-10-27',
            'HotelEquipment': '',
            'IsCanReserve': 'F',
            'IsOnlyAirHotel': 'F',
            'Minstate': '',
            'OrderBy': '99',
            'OrderID': '',
            'OrderType': '',
            'PaymentType': '',
            'Paymentterm': '',
            'PromoteDate': '',
            'PromoteEndDate': '',
            'PromoteStartDate': '',
            'PromoteType': '',
            'Resource': '',
            'Room': '',
            'RoomGuestCount': '1,1,0',
            'RoomNum': '',
            'StartTime': '2018-10-26',
            '__VIEWSTATEGENERATOR': 'DB1FBB6D',
            'a': '0',
            'allianceid': '0',
            'bed': '',
            'brand': '',
            'breakfast': '',
            'checkIn': '2018-10-26',
            'checkOut': '2018-10-27',
            'cityCode': '021',
            'cityId': '2',
            'cityLat': '31.2363508011',
            'cityLng': '121.4802384079',
            'cityName': '上海',
            'cityPY': 'shanghai',
            'contrast': '0',
            'contyped': '0',
            'defaultcoupon': '',
            'equip': '',
            'feature': '',
            'group': '',
            'hasPKGHotel': 'F',
            'hidTestLat': '0|0',
            'hotelBrandId': '',
            'hotelId': '',
            'hotelIds': '428365_1_1,1496646_2_1,393916_3_1,473770_4_1,4399431_5_1,13926223_6_1,6874402_7_1,15018492_8_1,12782071_9_1,15018773_10_1,8857430_11_1,18431318_12_1,6245432_13_1,436581_14_1,16197084_15_1,17504638_16_1,6338488_17_1,1073814_18_1,436187_19_1,4119594_20_1,1583084_21_1,437892_22_1,6082325_23_1,397163_24_1,387009_25_1',
            'hotelPriceLow': '',
            'hotelType': 'F',
            'hotelposition': '',
            'htlFrom': 'hotellist',
            'htlPageView': '0',
            'isHuaZhu': 'False',
            'isfromlist': 'T',
            'isusergiftcard': 'F',
            'k1': '',
            'k2': '',
            'keyword': '',
            'keywordLat': '',
            'keywordLon': '',
            'l': '',
            'location': '',
            'markType': '0',
            'operationtype': 'NEWHOTELORDER',
            'other': '',
            'page': '2',
            'positionArea': '',
            'positionId': '',
            'prepay': 'F',
            'price': '',
            'priceRange': '-2',
            'productcode': '',
            'promotion': 'F',
            'promotionf': '',
            'psid': '',
            'pyramidHotels': '',
            'requestTravelMoney': 'F',
            's': '',
            'showTipFlg': '',
            'showwindow': '',
            'sid': '0',
            'sl': '',
            'star': '',
            'txtkeyword': '',
            'type': '',
            'ubt_price_key': 'htl_search_result_promotion',
            'ulogin': '',
            'unBookHotelTraceCode': '',
            'useFG': 'F',
            'viewType': '',
            'zone': ''
        }
        url = 'http://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx'
        body = Requests.get_url_body(method='post', url=url, headers=await self._get_pc_headers(), cookies=None, data=data, ip_pool_type=sesame_ip_pool)
        data = json_2_dict(body)
        pprint(data)

        return data

    async def _fck_run(self):
        await self._search_hotels_by_pc()

    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = CtripSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())