# coding:utf-8

'''
@author = super_fazai
@File    : main.py
@Time    : 2017/9/26 14:37
@connect : superonesfazai@gmail.com
'''

"""
这个文件是程序开始运行的地方:
    1. 记住意外报错, 优先考虑是否是自己的微博号被封, 先解封再重新运行

注意：存储使用的是mysql数据库
    需要先建一个表：我写在最下方
    
然后在 pipeline.py文件里 的 __init__方法里面设置自己的mysql数据库相关属性
再在settings里面设置自己登陆新浪后的cookie值, 进行替换下

此外一个重点：
    本程序使用的是动态ip池:
    具体安装详见: https://github.com/qiyeboy/IPProxyPool
    其正确运行时，在浏览器输入http://0.0.0.0:8000时，会出现大量最新的可用代理ip, 本程序的代理ip就是从这获取的(也是本程序运行的基础)

还有一个注意每个热门分类里面微博号重复率很高，值筛选出不重复的插入~~

"""
from scrapy import cmdline

cmdline.execute("scrapy crawl sina_species_spider_new".split())

# cmdline.execute("scrapy crawl sina_species_spider_new --nolog".split())


'''
建表的sql语句在下方(请在mysql中运行):

create table bozhu_user(
	nick_name varchar(50) not null primary key,
	sina_type varchar(50) not null,
	nick_name_url varchar(200) not null, 
	care_number int default 0,
	fans_number int default 0,
	weibo_number int default 0,
	verify_type varchar(50),
	sine_level int default 0,
	verify_desc varchar(300),
	personal__deal_info_url varchar(200)
);
'''