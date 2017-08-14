# coding = utf-8

'''
@author = super_fazai
@File    : logging_test.py
@Time    : 2017/8/14 08:36
@connect : superonesfazai@gmail.com
'''

import logging

logs = logging.getLogger('APACHE')      # 先创建一个日志对象
logs.setLevel(logging.INFO)     # 如果此处设置了等级, 则优先级最高, 如果下面对屏幕或者文件单独设置的日志等级, 优先级都低于此处等级

sr_log = logging.StreamHandler()   # 定义一个屏幕输出log
sr_log.setLevel(logging.INFO)

file_log = logging.FileHandler('test.log')  # 定义输出文件的log
file_log.setLevel(logging.INFO)

# 定义输出的日志格式
log_format = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(module)s - %(message)s')

# 将输出格式加到屏幕输出句柄, 文件输出句柄的格式中
sr_log.setFormatter(log_format)
file_log.setFormatter(log_format)

# 将两个句柄放入log日志对象中
logs.addHandler(sr_log)
logs.addHandler(file_log)

# 开始日志输出
logs.debug('DEBUG中文'.encode())
logs.warning('This is a WARNING中文测试'.encode())
logs.info('This is a INFO 中文'.encode())
logs.error('This is a ERROR 中文测试'.encode())

'''
logging的Formatter格式包括如下类型：

%(name)s                   Name of the logger (logging channel)
%(levelno)s                Numeric logging level for the message (DEBUG, INFO,  WARNING, ERROR, CRITICAL)
%(levelname)s          Text logging level for the message ("DEBUG", "INFO",  "WARNING", "ERROR", "CRITICAL")
%(pathname)s           Full pathname of the source file where the logging  call was issued (if available)
%(filename)s             Filename portion of pathname
%(module)s               Module (name portion of filename)
%(lineno)d                 Source line number where the logging call was issued  (if available)
%(funcName)s          Function name
%(created)f                Time when the LogRecord was created (time.time()  return value)
%(asctime)s               Textual time when the LogRecord was created
%(msecs)d                 Millisecond portion of the creation time
%(relativeCreated)d Time in milliseconds when the LogRecord was created, relative to the time the logging module was loaded  (typically at application startup time)
%(thread)d                 Thread ID (if available)
%(threadName)s      Thread name (if available)
%(process)d              Process ID (if available)
%(message)s            The result of record.getMessage(), computed just as       the record is emitted
'''
