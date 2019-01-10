# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

import os
import jnius_config

# jnius_config.add_options('-Xrs', '-Xmx4096')
# jnius_config.set_classpath('.', '/usr/local/fem/plugins/*')

# mac查看JAVA_HOME
# $ /usr/libexec/java_home
os.environ['JAVA_HOME'] = '/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home'
print(os.environ)

from jnius import autoclass

autoclass('java.lang.System').out.println('hello world!')

Stack = autoclass('java.util.Stack')
stack = Stack()
stack.push('hello')
stack.push('world')
print(stack.pop())
print(stack.pop())
System = autoclass('java.lang.System')
System.out.println('Hello World!')

# 调用jar
# 要求导出jar后，需要先在python中设置好os.environ['CLASSPATH']词典，此外，要求放置jar的路径不含中文：
# import os
# os.environ['CLASSPATH'] = "path/to/your.jar"
#
# from jnius import autoclass
# Bla = autoclass('pacakagename.targetClass')

Tea = autoclass('com.mdroid.xxtea.Tea')
arrayOfByte = b'1'
Tea.decryptByDefaultKey(arrayOfByte)