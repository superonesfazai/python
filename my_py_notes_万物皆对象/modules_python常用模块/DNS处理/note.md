# dnspython模块
dnspython模块提供了大量的DNS处理方法, 最常用的方法是域名查询

dnspython提供了一个DNS解析器类-resolver, 使用它的query方法来实现域名的查询功能

安装: pip3 install dnspython

```python
query(self, qname, rdtype=1, rdclass=1, tcp=False, source=None, raise_on_no_answer=True, source_port=0)

# 其中qname参数为查询的域名
# rdtype参数用来指定RR资源的类型, 常用的一下几种:
'''
A记录, 将主机名转换为IP地址
MX记录, 邮件交换记录, 定义邮件服务器的域名
CNAME记录, 指别名记录, 实现域名间的映射
NS记录, 标记区域的域名服务器及授权子域
PTR记录, 反向解析, 与A记录相反, 将IP转换为主机名
SOA记录, SOA标记, 一个起始授权区的定义
'''
# rdclass参数用于指定网络类型, 可选值有IN, CH和HS, 其中IN是默认，使用最广泛
# tcp参数用于指定查询是否启用tcp协议
# source与source_port参数作为指定查询源地址与端口, 默认值为查询设备的ip地址和0
# raise_on_no_answer参数用于指定当查询无应答是否触发异常, 默认为True
```
