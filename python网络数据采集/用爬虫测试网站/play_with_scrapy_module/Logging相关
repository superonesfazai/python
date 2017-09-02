## Logging
Scrapy提供了log功能，可以通过 logging 模块使用。
```html
可以修改配置文件settings.py，任意位置添加下面两行，效果会清爽很多。
```
```python
LOG_FILE = "TencentSpider.log"
LOG_LEVEL = "INFO"
```
#### Log levels
```html
* Scrapy提供5层logging级别:

* CRITICAL - 严重错误(critical)

* ERROR - 一般错误(regular errors)
* WARNING - 警告信息(warning messages)
* INFO - 一般信息(informational messages)
* DEBUG - 调试信息(debugging messages)
```
#### logging设置
通过在setting.py中进行以下设置可以被用来配置logging:
```
1. LOG_ENABLED 默认: True，启用logging
2. LOG_ENCODING 默认: 'utf-8'，logging使用的编码
3. LOG_FILE 默认: None，在当前目录里创建logging输出文件的文件名
4. LOG_LEVEL 默认: 'DEBUG'，log的最低级别
5. LOG_STDOUT 默认: False 如果为 True，进程所有的标准输出(及错误)将会被重定向到log中。例如，执行 print "hello" ，其将会在Scrapy log中显示。
```

