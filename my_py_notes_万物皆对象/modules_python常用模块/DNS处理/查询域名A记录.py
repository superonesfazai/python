# coding:utf-8

'''
@author = super_fazai
@File    : 查询域名A记录.py
@Time    : 2018/5/18 14:18
@connect : superonesfazai@gmail.com
'''

import dns.resolver

domain = input('请输入域名地址:')
A = dns.resolver.query(domain, 'A')
for i in A.response.answer:     # 获取查询响应信息
    for j in i.items():         # 遍历响应信息
        print(j.address)