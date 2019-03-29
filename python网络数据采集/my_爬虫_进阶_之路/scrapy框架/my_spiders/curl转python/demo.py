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
curl 'http://huayu.zongheng.com/rank/c0/u14/p13/v0/ALL.html' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8' -H 'Cookie: ZHID=F4D6CA8DF9AC6BF04DEBE6339E83FA5F; JSESSIONID=abct8r-OQLCte8nCQjiNw; v_user=%7Chttp%3A%2F%2Fhuayu.zongheng.com%2Frank%2Fc0%2Fu14%2Fp1%2Fv0%2FALL.html%7C82708904; UM_distinctid=169c826b45c367-0bd4e883a6c78e-12316d51-1fa400-169c826b45d65f; CNZZDATA30058113=cnzz_eid%3D1908027181-1553839461-%26ntime%3D1553839461; zh_visitTime=1553841173610; zhffr=0; Hm_lvt_349a543900e207d0a48208f3318136b4=1553841174; Hm_lvt_c202865d524849216eea846069349eb9=1553841176; CNZZDATA30037065=cnzz_eid%3D2060897567-1553836312-%26ntime%3D1553841712; Hm_lpvt_349a543900e207d0a48208f3318136b4=1553842483; Hm_lpvt_c202865d524849216eea846069349eb9=1553842483' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)