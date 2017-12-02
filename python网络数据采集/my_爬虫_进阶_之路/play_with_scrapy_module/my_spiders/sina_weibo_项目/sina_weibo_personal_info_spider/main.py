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
    * 并且得先让 sina_weibo_fenlei_spider项目中的爬虫先爬到数据, 这个爬虫才能启动
    * 然后从前面爬虫爬到的数据中获取信息，再进行相应爬取
需要建两个表，我写在最下方：
    分别是 personal_deal_info表 和 company_deal_info表

然后在两个爬虫的 __init__方法里面分别设置自己的mysql相关属性
再在settings里面设置自己登陆新浪后的cookie值, 进行替换下

此外一个重点：
    本程序使用的是动态ip池:
    具体安装详见: https://github.com/qiyeboy/IPProxyPool
    其正确运行时，在浏览器输入http://0.0.0.0:8000时，会出现大量最新的可用代理ip, 本程序的代理ip就是从这获取的(也是本程序运行的基础)
"""

'''
根据自己的需求启动下面的爬虫
'''

from scrapy import cmdline

# 个人私人信息爬取
cmdline.execute("scrapy crawl personal_info_spider".split())
# cmdline.execute("scrapy crawl personal_info_spider --nolog".split())

# 企业私人信息爬取
# cmdline.execute('scrapy crawl company_info_spider'.split())     # 带log调试信息
# cmdline.execute('scrapy crawl company_info_spider --nolog'.split())     # 不带log调试信息


'''
建表的sql语句为下方(请在mysql中执行):

create table personal_deal_info(
	/*昵称*/
	nick_name varchar(50) not null primary key,		
	/*真实姓名*/
	true_name varchar(20),
	/*所在地*/
	live_place varchar(50),
	/*性别*/
	sex varchar(4),
	/*性取向*/
	love_man_or_woman varchar(10),
	/*感情状况*/
	feeling varchar(10),
	/*生日*/
	birthday varchar(15),
	/*血型*/
	blood_type varchar(5),
	/*博客地址*/
	blog_url varchar(200),
	/*简介*/
	simple_desc varchar(800),
	/*个性域名*/
	individuality_url varchar(100),
	/*注册时间*/
	register_time varchar(15),
	/*邮箱*/
	_email varchar(50),
	/*QQ*/
	qq varchar(12),
	/*MSN*/
	msn varchar(25),
	/*公司*/
	company varchar(800),
	/*大学*/
	edu varchar(500),
	/*标签*/
	_label varchar(1000),

	/*勋章信息*/
	medal_info varchar(1000),
	/*等级信息*/
	/*微博等级*/
	sina_level int not null,
	/*当前微博经验值*/
	sina_level_exp int not null,

	/*会员信息*/
	/*会员图标*/
	vip_icon varchar(200),
	/*会员成长速度*/
	vip_group_speed int,
	/*会员成长值*/
	vip_group_value int,

	/*阳光信用*/
	credit_value varchar(10)
);

create table company_deal_info(
	/*昵称*/
	nick_name varchar(50) not null primary key,	
	/*简介*/
	simple_desc varchar(800),
	/*联系人*/
	company_contact_name varchar(100),
	/*电话*/
	company_phone varchar(200),
	/*友情链接*/
	friend_url varchar(1000),

	/*勋章信息*/
	medal_info varchar(800),
	/*等级信息*/
	/*微博等级*/
	sina_level int not null,
	/*当前微博经验值*/
	sina_level_exp int not null,

	/*会员信息*/
	/*会员图标*/
	vip_icon varchar(200),
	/*会员成长速度*/
	vip_group_speed int,
	/*会员成长值*/
	vip_group_value int
);
'''