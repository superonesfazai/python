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
curl 'http://i.meituan.com/select/shijiazhuang/page_2.html?cid=11&bid=-1&sid=defaults&p=2&ciid=76&bizType=area&csp=&cateType=poi&nocount=true&stid_b=_b2' -H 'Cookie: _lxsdk_cuid=1676292f6c1c8-0ea87c189c2bd2-35677607-1fa400-1676292f6c2c8; iuuid=A85D4740516D38394B11E7F381524E1D8BB583503232059BDD3624DAC81FA129; _hc.v=5324fb85-48d4-1e15-e55a-fd996a060470.1543547291; _lxsdk=A85D4740516D38394B11E7F381524E1D8BB583503232059BDD3624DAC81FA129; __utmz=74597006.1543556280.2.2.utmcsr=meishi.meituan.com|utmccn=(referral)|utmcmd=referral|utmcct=/i/; rvct=1; a2h=4; wm_order_channel=mtib; _lx_utm=utm_source%3D60030; ci=76; cityname=%E7%9F%B3%E5%AE%B6%E5%BA%84; JSESSIONID=363ghio0km3b1k7ola12m7jjb; IJSESSIONID=363ghio0km3b1k7ola12m7jjb; __utmc=74597006; uuid=028f16e9-fee8-4c76-979a-5f45ea11767e; ci3=1; __utma=74597006.1692471204.1543547094.1544768918.1544773017.11; __mta=254140087.1543547103185.1544768974656.1544773017379.20; i_extend=C_b3Gimthomepagecategory299999H__a100265__b11; latlng=; _lxsdk_s=167aba59b00-0d6-ee9-4f9%7C%7C5; __utmb=74597006.3.10.1544773017' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9' -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1' -H 'Accept: text/html' -H 'Referer: http://i.meituan.com/shijiazhuang/all/?cid=11&p=2&cateType=poi' -H 'X-Requested-With: XMLHttpRequest' -H 'Proxy-Connection: keep-alive' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)