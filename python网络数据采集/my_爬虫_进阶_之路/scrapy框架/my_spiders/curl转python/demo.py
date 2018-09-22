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
curl 'https://headline.taobao.com/feed/feedQuery.do?columnId=0&publishId=0' -H 'cookie: cna=2svqE2mvXBoCAXHXtPCLe5oQ; thw=cn; miid=9181261871026670022; hng=CN%7Czh-CN%7CCNY%7C156; t=8f06ca31d89f46259fd1468bf31f8403; tg=0; enc=RNzYvdKS2dpjU9b%2FVVlCv6H5w6aj6gV%2BRMAtZ8DxyuVlDBHKFr4axoTGJ7D%2BRtvO7Q73CtAluIncTFgKW7uEVw%3D%3D; tracknick=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; lgc=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; v=0; cookie2=318163a7a42a28bda33e07401ffc7a18; _tb_token_=71111e58e41e; UM_distinctid=165fa6aed7b3bd-0fb452f158a482-346a7809-1fa400-165fa6aed7c480; unb=2242024317; sg=%E4%BA%BA73; _l_g_=Ug%3D%3D; skt=ed6a0fb4e040c091; cookie1=UR3Wq2iKhDJHTTOd%2FGn4oh0oxwBK8EUqK%2Bm%2Bxv62FEM%3D; csg=ccc38514; uc3=vt3=F8dByRuXIfkv1i93Wzw%3D&id2=UUplY9Ft9xwldQ%3D%3D&nk2=rUtEoY7x%2Bk8Rxyx1ZtN%2FAg%3D%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D; existShop=MTUzNzYwNDUzOA%3D%3D; _cc_=UIHiLt3xSw%3D%3D; dnk=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; _nk_=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; cookie17=UUplY9Ft9xwldQ%3D%3D; mt=ci=67_1; uc1=cookie14=UoTfLJOZvR2Otw%3D%3D&lng=zh_CN&cookie16=U%2BGCWk%2F74Mx5tgzv3dWpnhjPaQ%3D%3D&existShop=false&cookie21=UtASsssmfavW4WY1P7uXzg%3D%3D&tag=8&cookie15=UIHiLt3xD8xYTw%3D%3D&pas=0; _m_h5_tk=accca8abb5cb03e433f7de318df2fcc5_1537615487239; _m_h5_tk_enc=45e3379d30ed556245457e8a1135acc1; isg=BKeni2xOsBs4wDSq3NYUpc24Nt2xhHlotDPN-XkUwzZdaMcqgfwLXuVujijTgFOG' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: zh-CN,zh;q=0.9' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36' -H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' -H 'accept: application/json, text/javascript, */*; q=0.01' -H 'referer: https://headline.taobao.com/feed/feedList.htm?spm=a21bo.2017.226762.2.5af911d91DLSyX' -H 'authority: headline.taobao.com' -H 'x-requested-with: XMLHttpRequest' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)