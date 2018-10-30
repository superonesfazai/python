# coding = utf-8

'''
@author = super_fazai
@File    : tasks.py
@Time    : 2017/8/20 13:56
@connect : superonesfazai@gmail.com
'''

"""
爬取的主要目的是从非结构化源(通常是网页)中提取结构化数据
    scrapy spider能将爬取的数据 作为python的dict来返回

    虽然方便而熟悉，Python却缺乏结构：
    容易造成字段名称中的输入错误或返回不一致的数据，
    特别是在具有许多蜘蛛的较大项目中
    
* scrapy提供了Item类, 来定义常用的输出数据格式
* Item对象是用于收集数据的简单的容器(有点像Python中的dict，但是提供了一些额外的保护减少错误)
    它们提供一个类似字典的API, 具有方便的语法来声名其可用字段
    
* 可以通过创建一个 scrapy.Item 类， 
  并且定义类型为 scrapy.Field的类属性来定义一个Item（可以理解成类似于ORM的映射关系）

* 序列化可以使用Item字段元数据进行自定义，使用 trackref 跟踪Item实例以帮助查找内存泄漏
"""

# 声名创建一个Item
# 这跟Django Models的声名很像, 还简单一点
import scrapy

class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)

'''
Item Field
'''
"""
Field对象用于为每个字段指定元数据。
    1. 您可以为每个字段指定任何种类的元数据。Field对象接受的值没有限制
    2. Field对象中定义的每个键可以被不同的组件使用，只有那些组件知道它
    3. 您还可以根据Field自己的需要定义和使用项目中的其他任何 键
例如，上述last_updated示例中所示的字段的序列化器功能

注意：Field用于声明该项目的对象不会被分配为类属性。
     而是可以通过Item.fields属性访问它们
"""

product = Product(name='Desktop PC', price=1000)
print(product)
print(product['name'], ' ',product.get('name'))
# print(product['last_updated'])      # 会报错 KeyError: 'last_updated', 为了安全都用下面的来
print(product.get('last_updated', 'no set'))

print('name' in product)
print('last_updated' in product)
print('last_updated' in product.fields)

'''
Item objects
class scrapy.item.Item([arg])
    返回一个可以从给定参数初始化的新项目。
    项目复制标准dict API，包括其构造函数。项目提供的唯一附加属性是：

fields
    一个包含此项目的所有声明字段的字典，不仅包含这些填充的字段。
    键是字段名称，值是Item声明中Field使用的 对象
'''

'''
Field objects
class scrapy.item.Field([arg])
    该Field班只是一个别名内置的字典类，并没有提供任何额外功能或属性。
    换句话说， Field对象是古老的Python脚本。
    一个单独的类用于支持 基于类属性的项目声明语法
'''