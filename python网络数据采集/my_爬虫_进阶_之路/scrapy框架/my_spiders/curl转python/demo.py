# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

"""
curl命令 转成原生的python requests代码
"""

from fzutils.curl_utils import curl_cmd_2_py_code

curl_cmd = r'''
curl 'http://m.maoyan.com/ajax/movie?forceUpdate=1538719939821' -H 'Cookie: _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; _lxsdk_cuid=16642591771c8-0c7b42770a7c79-346a7809-1fa400-16642591772c8; v=3; uuid_n_v=v1; iuuid=D78D54B0C85111E88CF261F13D453A3D36140E6C0657438DBE9D4F1BDFF21C75; webp=true; ci=50%2C%E6%9D%AD%E5%B7%9E; selectci=; from=canary; __mta=48499097.1538711428133.1538711442416.1538711821132.3; __mta=48499097.1538711428133.1538711442416.1538718413212.3; _lxsdk=D78D54B0C85111E88CF261F13D453A3D36140E6C0657438DBE9D4F1BDFF21C75; _lxsdk_s=16642c3b06f-190-b59-58%7C%7C4' -H 'Origin: http://m.maoyan.com' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9' -H 'User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: http://m.maoyan.com/cinema/movie/342166?$from=canary' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data 'movieId=342166&day=2018-10-05&offset=20&limit=20&districtId=-1&lineId=-1&hallType=-1&brandId=-1&serviceId=-1&areaId=-1&stationId=-1&item=&updateShowDay=false&reqId=1538719936817&cityId=50' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)