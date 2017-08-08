#!/usr/bin/python3.5
#coding: utf-8

#通过getattr获取对象的引用
#你已经知道 Python 函数是对象 。你不知道的是,使用 getattr 函数,可以得到
#一个直到运行时才知道名称的函数的引用

#getattr 介绍
li = ["Larry", "Curly"]
print(li.pop)
print(getattr(li, 'pop'))
print(li)
print(getattr(li, 'append')('MOE'))
print(li)
print(getattr({}, 'clear'))
#print(getattr((), 'pop'))  #报错：tuple没有属性pop
'''
(1) 该语句获取列表的 pop 方法的引用。注意该语句并不是调用 pop 方法;调
用 pop 方法的应该是 li.pop() 。这里指的是方法对象本身。
(2) 该语句也是返回 pop 方法的引用,但是此时,方法名称是作为一个字符串
参数传递给 getattr 函数的。 getattr 是一个有用到令人无法致信的内置函数,
可以返回任何对象的任何属性。在这个例子中,对象是一个 list,属性是
pop
方法。
(3) 如果不确信它是多么的有用,试试这个: getattr 的返回值 是 方法,然后你
就可以调用它,就像直接使用 li.append("Moe") 一样。但是实际上你没有直
接调用函数;只是以字符串形式指定了函数名称。
(4) getattr 也可以作用于字典。
(5) 理论上, getattr 可以作用于元组,但是由于元组没有方法,所以不管你指
定什么属性名称 getattr 都会引发一个异常
'''

#getattr 作为一 个分发者
'''
getattr 常见的使用模式是作为一个分发者。举个例子,如果你有一个程序可以
以不同的格式输出数据,你可以为每种输出格式定义各自的格式输出函数,
然后使用唯一的分发函数调用所需的格式输出函数。
例如,让我们假设有一个以 HTML、XML 和普通文本格式打印站点统计的程序。
输出格式在命令行中指定,或者保存在配置文件中。 statsout 模块定义了三个
函数: output_html 、 output_xml 和 output_text 。然后主程序定义了唯一的输出函数,
如下:
'''
#使用 getattr 创建 分发者
# import statsout
# def output(data, format="text"):
#     output_function = getattr(statsout, "output_%s" % format)
#     return output_function(data)
'''
(1) output 函数接收一个必备参数 data ,和一个可选参数 format 。如果没有指定format
参数,其缺省值是 text 并完成普通文本输出函数的调用。
(2) 你可以连接 format 参数值和 "output_" 来创建一个函数名称作为参数值,
然后从 statsout 模块中取得该函数。这种方式允许今后很容易地扩展程序
以支持其它的输出格式,而且无需修改分发函数。所要做的仅仅是向
statsout
中添加一个函数,比如 output_pdf ,之后只要将 “pdf” 作为 format 的
参数值传递给 output 函数即可。
(3) 现在你可以简单地调用输出函数,就像调用其它函数一样。 output_function
变量是指向 statsout 模块中相应函数的引用
'''

#getattr 缺省值
# import statsout
# def output(data, format="text"):
#     output_function = getattr(statsout, "output_%s" % format, statsout.output_text)
#     return output_function(data)
'''
(1) 这个函数调用一定可以工作,因为你在调用 getattr 时添加了第三个参数。
第三个参数是一个缺省返回值,如果第二个参数指定的属性或者方法没能
找到,则将返回这个缺省返回值。
正如你所看到, getattr 是相当强大的。它是自省的核心,在后面的章节中你将
看到它更强大的示例。
'''

