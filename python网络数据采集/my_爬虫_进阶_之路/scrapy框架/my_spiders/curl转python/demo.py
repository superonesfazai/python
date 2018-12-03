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
curl 'https://kuaibao.qq.com/getVideoRelate?id=20180906V1A30P00&userid=o1006770934&coral_uin=' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: zh-CN,zh;q=0.9' -H 'user-agent: Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1' -H 'accept: application/json, text/plain, */*' -H 'referer: https://kuaibao.qq.com/s/20180906V1A30P00?refer=kb_news&titleFlag=2&omgid=78610c582f61e3b1f414134f9d4fa0ce' -H 'authority: kuaibao.qq.com' -H 'cookie: pgv_pvi=9476041728; pgv_pvid=2375623608; pt2gguin=o1006770934; RK=jKo1uuhANd; ptcz=d1a55f430e13b885d3021c26763d8cfb2a0e50c1c763950ba880d73939a3a837; kb_h5_user_id=KBH5UserId_15406191602060557; o_cookie=1006770934; pac_uid=1_1006770934; tvfe_boss_uuid=b1f4ddefbadae265; uin=o1006770934; skey=@LIsNFImkp' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)