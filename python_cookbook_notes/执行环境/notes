# 函数

## 内建函数(BIF)
内建函数属性
bif.__doc__     文档字符串
bif.__name__    字符串类型的文档名
bif.__self__    设置为None(保留给内建方法)
bif.__moudle__  存放bif定义的模块名字(或者None)

## 用户自定义函数(UDF)
用户自定义函数属性
udf.__doc__     文档字符串
udf.__name__    字符串类型的函数名字
udf.func_code   字节编译的代码对象
udf.func_defaults   默认的参数元祖
udf.func_globals    全局名称空间字典：等同于从函数内部调用globals()
udf.func_dict   函数属性的名称空间
udf.func_doc    ...
udf.func_name   ...
udf.func_closure    包含了自由变量的引用的单元对象元祖

# 方法

# 可执行的对象声明和内建函数
callable(obj)       如果obj可调用,return True
compile(string, file, type)     从type类型中创建代码对象;file是代码存放的地方(通常设为"")
eval(obj, globals=globals(), locals=locals())
    对obj进行求值,obj是已编译为代码对象的表达式,或是一个字符串表达式;
    可以给出全局或者/和局部的名称空间       # eval执行的编译代码中,不能进行赋值操作
exec obj
    执行obj,单一的python语句或者语句的集合
    也就是说格式是代码对象或者字符串;
    obj也可以是一个文件对象(已经打开的有效python脚本中)
    eg: exec(str(print('-----------')))
input(prompt='')    等同于eval(raw_input(prompt=""))

exec()和eval() 都可以执行字符串格式的python代码
compile()函数提供了一次性字节代码预编译,以后每次调用时,都不用编译了
compile的三个参数都是必须的
    compile通常用法是动态生成字符串形式的python代码
        然后生成一个代码对象--代码显然没有存放任何文件
    第一个：要编译的python代码
    第二个：虽然是必须的,但通常被置为空串,该参数代表了存放代码对象的文件名字(字符串类型)
    第三个：字符串,表明代码对象的类型

# 手动编译
import compileall
compileall.compile_dir(目录)