## sina_weibo_fenlei_spider
* 这个是抓取分类的爬虫

具体使用方法：
* 环境是python3
* 进入这个目录下的main.py文件
* 在main.py文件里面进行相关配置
* 在settings.py里面进行相关设置
* 运行python3 main.py即可

## sina_weibo_home_info_spider
* 这个是抓取主页里面个人信息的(如微博认证, 认证种类)
* 用法同上

## sina_weibo_personal_info_spider
* 这个是抓取个人私人信息页和企业信息页的
* 用法同上

## sina_weibo_bozhu_all_weibo
* 这个是抓取个人近半年所有微博, 和对应微博所有评论的
* 打开main.py文件进行相关设置和配置
* 遇到异常的微博号，可以用在做筛选的sql语句是不选择异常微博号即可

## 注意

* 以上爬虫每个都是单独运行的
* 运行顺序，必须先运行第一个爬虫(sina_weibo_fenlei_spider)，让里面有数据才行
* 才可运行其他几个
* 必须进入main.py和settings.py进行相关设置才能运行每个爬虫
* 在mysql, 动态ip池和驱动配置都没问题的情况下，爬虫跑死, 优先考虑登录的账户异常, 重新赋值cookies