Scrapy 生成的调试信息非常有用,但是通常太罗嗦。你可以在 Scrapy 项目中
的 setting.py 文件中设置日志显示层级:
    LOG_LEVEL = 'ERROR'
Scrapy 日志有五种层级,按照范围递增顺序排列如下:
    • CRITICAL
    • ERROR
    • WARNING
    • DEBUG
    • INFO
如果日志层级设置为 ERROR ,那么只有 CRITICAL 和 ERROR 日志会显示出来。
如果日志层级设置为 INFO ,那么所有信息都会显示出来,其他同理。

日志不仅可以显示在终端,也可以通过下面命令输出到一个独立的文件中:
    $ scrapy crawl article -s LOG_FILE=wiki.log
如果目录中没有 wiki.log,那么运行程序会创建一个新文件,然后把所有的
日志都保存到里面。如果已经存在,会在原文后面加入新的日志内容。