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
curl 'http://z.go2.cn/supplier/0-0-0-all/' -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3' -H 'Referer: http://z.go2.cn/supplier/0-T-5-all/' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8' -H 'Cookie: _ga=GA1.2.454316160.1553938516; go2_session=a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22edb44b693f8a22d173fac9ee473941f6%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A14%3A%22113.215.180.39%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A120%3A%22Mozilla%2F5.0+%28Macintosh%3B+Intel+Mac+OS+X+10_14_2%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F73.0.3683.86+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1554084815%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7Da18941c52be69ec1b16c2d1b78bfe363; utm_unique=748A0DA1-DC24-9EEF-93AF-5AAB2016F70F; _gid=GA1.2.1356485757.1554084819; Hm_lvt_d632121f6fa73f8db725c6dfcb8cf041=1553938517,1553940350,1554084820; Hm_lvt_80e798ed6dd8a1596a3a77ceb1ee88ae=1553938517,1553940351,1554084820; Hm_lvt_c474c6da0ac1239117a1f6abbbc48d32=1553938518,1553940351,1554084821; Hm_lvt_fa5da7a6f80ec2247f5c8de677f76041=1553938518,1553940351,1554084821; aliyungf_tc=AQAAAMy1uD8owAMAJ7TXcZghHV57XQ8h; PHPSESSID=hq2pcgmt7u315l5uhsbmvb98q2; __51cke__=; Hm_lvt_f6cad666dd7696b74db974d3d5aab4f3=1553938529,1553938573,1554084851; Hm_lvt_e838809e282b973abda9a75260600a0f=1553938529,1553938573,1554084851; Hm_lvt_9d0abdf1f48a92c8ad9b5078b24ed864=1553938529,1553938573,1554084851; Hm_lvt_726778d4d8b40b8c83bc2a1367cfd7d6=1553938529,1553938573,1554084851; Hm_lvt_966bafbde46979d2c64b80725ec1fbb3=1553938529,1553938573,1554084851; Hm_lvt_dd6c5448d9747b21983d4d4db20831a0=1553938529,1553938573,1554084851; Hm_lvt_d2ede7bff5cdac94f9cc9d8ce9b27277=1553938529,1553938574,1554084851; Hm_lvt_62b3cf2b6595100cabc31cda24169e39=1553938529,1553938574,1554084851; Hm_lvt_b943c4774942276062c9b2dfcff5f0b1=1553938529,1553938574,1554084851; __tins__4621821=%7B%22sid%22%3A%201554084850199%2C%20%22vd%22%3A%2010%2C%20%22expires%22%3A%201554086712924%7D; __51laig__=10; Hm_lpvt_e838809e282b973abda9a75260600a0f=1554084913; Hm_lpvt_f6cad666dd7696b74db974d3d5aab4f3=1554084913; Hm_lpvt_9d0abdf1f48a92c8ad9b5078b24ed864=1554084913; Hm_lpvt_80e798ed6dd8a1596a3a77ceb1ee88ae=1554084913; Hm_lpvt_726778d4d8b40b8c83bc2a1367cfd7d6=1554084913; Hm_lpvt_dd6c5448d9747b21983d4d4db20831a0=1554084913; Hm_lpvt_966bafbde46979d2c64b80725ec1fbb3=1554084913; Hm_lpvt_c474c6da0ac1239117a1f6abbbc48d32=1554084913; Hm_lpvt_d2ede7bff5cdac94f9cc9d8ce9b27277=1554084913; Hm_lpvt_62b3cf2b6595100cabc31cda24169e39=1554084913; Hm_lpvt_fa5da7a6f80ec2247f5c8de677f76041=1554084913; Hm_lpvt_b943c4774942276062c9b2dfcff5f0b1=1554084913; Hm_lpvt_d632121f6fa73f8db725c6dfcb8cf041=1554084913' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)