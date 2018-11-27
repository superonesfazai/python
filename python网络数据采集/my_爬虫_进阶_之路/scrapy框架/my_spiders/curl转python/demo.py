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
curl 'https://post.mp.qq.com/kan/article/2184322959-232584629.html?_wv=2147483777&sig=24532a42429f095b9487a2754e6c6f95&article_id=232584629&time=1542933534&_pflag=1&x5PreFetch=1&web_ch_id=0&s_id=gnelfa_3uh3g5&share_source=0' -H 'authority: post.mp.qq.com' -H 'cache-control: max-age=0' -H 'upgrade-insecure-requests: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: zh-CN,zh;q=0.9' -H 'cookie: pgv_pvi=9476041728; pgv_pvid=2375623608; pt2gguin=o1006770934; RK=jKo1uuhANd; ptcz=d1a55f430e13b885d3021c26763d8cfb2a0e50c1c763950ba880d73939a3a837; uin=o1006770934; p_uin=o1006770934; pt4_token=y1UxRZF6GGnV86TGyV9bcnnD1XDym0sxI-nzcmmLNp0_; p_skey=6nf-*OexsqQxjgjIv-SLMKEjiQKTKxd4B58yzKMTeHE_; pgv_info=ssid=s2191392944; ts_uid=8637113824; pgv_si=s9364407296; o_cookie=1006770934; pac_uid=1_1006770934; pt_local_token=1; tvfe_boss_uuid=b1f4ddefbadae265; ci_session=a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22c7a51d753d4e0afa053e1aef63cdf2db%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A12%3A%2210.56.114.17%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A120%3A%22Mozilla%2F5.0+%28Macintosh%3B+Intel+Mac+OS+X+10_14_0%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F70.0.3538.102+Safari%2F537.3%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1543282508%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7Dbd3645f2b41502d0ec5663b4f1c212cecffacaee; ts_last=post.mp.qq.com/kan/article/2184322959-232584629.html' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)