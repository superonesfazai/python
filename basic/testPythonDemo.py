#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
#使unicode编码能识别中文

#python是对大小写敏感的
print "hello, Python!";

name = raw_input('please enter your name: ');
#Integer a = (Integer)raw_input('please enter the number: ');
#This variable itself is not a fixed type of language, called a dynamic language, and corresponds to a static language.
b = 123;
c = 'abc';
print b,c;

#下面是java中静态变量的赋值
#aaa is an integer type variable
#int aaa = 123; 
#aaa = "ABC";  #Error: string cannot be assigned to an integer variable

print ord('A'), chr(65);
#输出中文
print u'中文';  
print '\xe4\xb8\xad\xe6\x96\x87'.decode('utf-8');
print u'ABC'.encode('utf-8'), ',', u'中文'.encode('utf-8');

print 'Hello,', name, '!';
print '''line1
line2
lline3''';

#输出格式化的字符串
#在Python中，采用的格式化方式和C语言是一致的，用%实现
#%d	整数 %f	浮点数 %s	字符串 %x	十六进制整数
#格式化整数和浮点数还可以指定是否补0和整数与小数的位数
print 'Hello, %s' % 'world';
print 'Hi, %s, you have $%d.' % ('Michael', 1000000);
print '%2d-%02d' % (3, 1), '%.2f' % 3.1415926;
#如果你不太确定应该用什么，%s永远起作用，它会把任何数据类型转换为字符串
print 'Age: %s. Gender: %s' % (25, True);
#用%来转义字符
print 'growth rate: %d %%' % 7;

#list
#list是一种有序的集合，可以随时添加和删除其中的元素
classmates = ['afa', 'axing','ahua'];
print classmates,',', len(classmates),',', classmates[0], classmates[1], classmates[2];
print classmates[-1], classmates[-2], classmates[-3];
classmates.append('Adam');
print classmates;
classmates.pop();
print classmates;