- 打开test2/settings.py文件，找到DATABASES项，默认使用SQLite3数据库
![](https://i.loli.net/2019/09/24/y6oelcVk94g2Laf.png)

- 修改为使用MySQL数据库，代码如下
- 将引擎改为mysql，提供连接的主机HOST、端口PORT、数据库名Name、用户名USER、密码PASSWORD
```html
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test2',
        'USER': 'root',
        'PASSWORD': 'mysql',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
