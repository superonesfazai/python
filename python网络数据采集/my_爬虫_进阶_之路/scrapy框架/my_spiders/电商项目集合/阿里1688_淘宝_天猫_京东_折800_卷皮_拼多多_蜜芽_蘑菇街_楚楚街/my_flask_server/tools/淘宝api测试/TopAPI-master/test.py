# -*- coding: utf8 -*-

import top, json

# api = top.TaoAPI(url="http://gw.api.taobao.com/router/rest",appkey="",secret="")
api = top.TaoAPI(
    url="https://h5api.m.taobao.com/h5/mtop.ju.data.get/1.0/",
    appkey="",
    secret=""
)


# tpwd_param={"url":"http://m.taobao.com","text":"超值活动，惊喜活动多多"}
tpwd_param={
    'jsv': '2.4.8',
    'appKey': '12574478',
    't': 1517284781823,
    'api': 'mtop.ju.data.get',
    'v': '1.0',
    'type': 'jsonp',
    'dataType': 'jsonp',
    'callback': 'mtopjsonp1',
    'data': json.dumps({
        'bizCode': 'tejia_002',
        'optStr': json.dumps({
            'cardType': ['9.9','39','69'],
            'includeForecast': True,
            'topItemIds': [],
        })
    }),
    # {"bizCode":"tejia_002","optStr":{"cardType":["9.9","39","69"],"includeForecast":'true',"topItemIds":[]}}
    # 'bizCode': 'tejia_002',
    # 'optStr': '{\"cardType\":[\"9.9\",\"39\",\"69\"],\"includeForecast\":true,\"topItemIds\":[]}',
}

# api.set_api_info(method="taobao.wireless.share.tpwd.create",tpwd_param=tpwd_param)#设置api信息 api方法 参数
api.set_api_info(method="mtop.ju.data.get", tpwd_param=tpwd_param) # 设置api信息 api方法 参数


print(api.get())


