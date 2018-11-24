# coding:utf-8

'''
@author = super_fazai
@File    : tasks.py
@connect : superonesfazai@gmail.com
'''

"""
curl命令 转成原生的python requests代码
"""

from fzutils.curl_utils import curl_cmd_2_py_code

curl_cmd = r'''
curl 'http://m.ziroom.com/v7/room/filter.json?city_code=110000' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9' -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1' -H 'Accept: application/json;version=5' -H 'Referer: http://m.ziroom.com/BJ/search?show=%E6%95%B4%E7%A7%9F&list=2&type=10' -H 'Cookie: CURRENT_CITY_CODE=110000; CURRENT_CITY_NAME=%E5%8C%97%E4%BA%AC; gr_user_id=c870f65f-b601-4265-8339-e094c955ce7f; gr_session_id_8da2730aaedd7628=e741677d-4f63-442d-949f-13d99267aeaf; gr_session_id_8da2730aaedd7628_e741677d-4f63-442d-949f-13d99267aeaf=true; PHPSESSID=647lhmma7bajeepoa25iiuav42; hlwyfb_m_current_city_code=110000; curUrl=index; __utma=14049387.1193983091.1543046015.1543046015.1543046015.1; __utmc=14049387; __utmz=14049387.1543046015.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; __utmb=14049387.1.10.1543046015; city_code=110000' -H 'Connection: keep-alive' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)