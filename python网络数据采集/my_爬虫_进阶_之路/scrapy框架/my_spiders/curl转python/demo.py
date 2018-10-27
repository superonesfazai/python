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
curl 'https://m.luckincoffee.com/capi/resource/m/promo/activity/send?q=%7B%22mobile%22:%2218698570079%22,%22invitationCode%22:%22MK20180301001%22,%22needOpenId%22:0,%22_%22:1540616905978%7D' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: zh-CN,zh;q=0.9' -H 'User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36' -H 'Accept: application/json, text/plain, */*' -H 'Referer: https://m.luckincoffee.com/invite/tangwei/MK20180301001' -H 'Cookie: csrfToken=HGm5NPSH1pKU0OwyBjeqdMMV; Hm_lvt_47cb106f7ef77f02dc2d004888b15540=1540616822; LUCKIN_COFFEE_WAP_SID=-wOuAO6HqPDHFTQQePnaGetOy_hy9bz5nOqIUBkh_QgaRBmvrGeHCqM9wgNzZxtw; LUCKIN_COFFEE_WAP_SSID=yIQgw9ZmaDbuMcMLNfVyzHVO0_qIwmVkVMj6tH4EL6Q0horlDVx9akSLy0AfaXGV-fA6iO6ApUzIyX_mjgDJ2WR2ZySEiBXJjKuVRMfWAYZReJKl_akG4DfgfJ_A5W2M2826-67Fo10CfSQYkJqR0IY6BXPDUQhOdLPODXFGEEE=; Hm_lvt_ebe8f44edccfe8af8a8137338a1785fd=1540616842; Hm_lpvt_47cb106f7ef77f02dc2d004888b15540=1540616859; Hm_lpvt_ebe8f44edccfe8af8a8137338a1785fd=1540616873' -H 'Connection: keep-alive' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)