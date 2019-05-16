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
curl 'http://h5vv.video.qq.com/getinfo?callback=tvp_request_getinfo_callback_654434&platform=11001&charge=0&otype=json&ehost=http%3A%2F%2Fpost.mp.qq.com&sphls=0&sb=1&nocache=0&_rnd=1557917186&guid=daf25a829d645f1196b61df6417e87bf&appVer=V2.0Build9502&vids=m0866r0q1xn&defaultfmt=auto&&_qv_rmt=AI5PT6eoA15978I5x=&_qv_rmt2=Kt7fT8OE157116tsw=&sdtfrom=v3010&_=1557917186891' -H 'Referer: http://post.mp.qq.com/kan/video/200553568-3955cc7c7ca772bk-m0866r0q1xn.html?_wv=2281701505&sig=b6e3ce15444e66d4fa4d6b40814b6858&time=1557141250&iid=MTY3MTk0MzU2Mw==' -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)