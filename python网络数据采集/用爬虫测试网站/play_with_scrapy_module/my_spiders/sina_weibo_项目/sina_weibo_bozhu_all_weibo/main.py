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

另外得到每个用的数据库的文件中把数据库改成自己的数据库
    像我的是：
    self.conn = connect(
                host='localhost',
                port=3306,
                db='python',
                user='root',
                passwd='lrf654321',
                # charset='utf-8',
    )
    请改成你自己的...

爬取的月份去settings.py文件中更改截止月份即可

然后自己如果要指定要爬取的表的话，得从bozhu_user表中获取信息
去get_nick_name_and_and_nick_name_url_and_personal_deal_info_url这个函数中改sql语句, 改成你需要爬取的表
(注意：给定的字段必须一一对应)

此外一个重点：
    本程序使用的是动态ip池:
    具体安装详见: https://github.com/qiyeboy/IPProxyPool
    其正确运行时，在浏览器输入http://0.0.0.0:8000时，会出现大量最新的可用代理ip, 本程序的代理ip就是从这获取的(也是本程序运行的基础)
    (让他先出现至少150个代理ip才可进行爬取)
"""

from scrapy import cmdline

# 打印debug信息版
cmdline.execute("scrapy crawl simple_bozhu_all_weibo_spider".split())

# 不打印debug信息版
# cmdline.execute("scrapy crawl simple_bozhu_all_weibo_spider --nolog".split())


'''
建表的sql语句在下方(请在mysql中运行):

微博内容表设计:
create table sina_wb_article(
	/*微博文章的id*/
	id varchar(40) not null primary key,
	/*博主的名字*/
	nick_name varchar(40) not null,
	/*微博文章的创建时间*/
	created_at varchar(30) not null,
	/*该微博的内容*/
	text varchar(2500),
	/*原创微博的图片链接*/
	image_url_list varchar(1000),
	/*原创微博的视频链接*/
	m_media_url varchar(400),
	/*该微博的转发内容*/
	retweeted_text varchar(1200),
	/*转发内容的图片链接*/
	retweeted_image_url_list varchar(1000),
	/*转发内容的视频链接*/
	media_url varchar(400),
	/*转载数*/
	reposts_count int,
	/*评论数*/
	comments_count int,
	/*点赞数*/
	attitudes_count int
);

评论表设计:
create table sina_review(
	/*评论的id*/
	review_id varchar(40) not null primary key,
	/*微博文章的id*/
	wb_id varchar(40) not null,	/*算是一个外键, 用于查找某条微博所有的评论信息*/
	/*评论者的微博名*/
	username varchar(100),
	/*评论的内容*/
	comment varchar(2500),
	/*评论的图片链接*/
	review_pics varchar(1200),
	/*评论创建时间*/
	review_created_at varchar(30),
	/*是否为博主回复内容*/
	is_reply_comment varchar(6),
	/*评论点赞数*/
	like_counts int
);
'''