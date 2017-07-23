# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-23 下午3:39
# @File    : 定制_test.py

# 简单定制
# 目标：需要一个类来保存浮点型,四舍五入,保留2位小数点
# 这个类仅接收一个浮点值
class RoundFloatManual(object):
    def __init__(self, val):
        assert isinstance(val, float),\
            'Value must be a float'
        self.value = round(val, 2)

try:
    rfm = RoundFloatManual(42)
except:
    print('AssertionError: Value must be a float!')

rfm = RoundFloatManual(4.2)
print(rfm)
# 打印的不是我们想要的,我们想要的数值,调用print语句同样没有明显的帮助
# 不幸的是,print(使用str())和真正的字符串对象显示(使用repr())
# 都没能显示过多有关我们对象的信息
# 一个好的方法是:去实现__str__()和__repr__()二者之一,或者两者都实现
# 所以我们在下面的类中添加一个__str()__方法

class RoundFloatManual2(object):
    def __init__(self, val):
        assert isinstance(val, float), \
            'Value must be a float'
        self.value = round(val, 2)

    def __str__(self):
        return str(self.value)
rfm = RoundFloatManual2(5.59064)
print(rfm)
frm = RoundFloatManual2(5.5964)
print(rfm.__repr__)
print('')

# 可以让__repr__()和__str__()一致
# 如果我们想修复它,可以通过重写来覆盖它
# 我们也可以让输出一致
# __repr__ = __str__

# 基本定制
class RoundFloatManual3(object):
    def __init__(self, val):
        assert isinstance(val, float), \
            'Value must be a float'
        self.value = round(val, 2)

    def __str__(self):
        return ('%.2f' % self.value)

    __repr__ = __str__
rfm = RoundFloatManual3(5.59064)
print(rfm)

print('')

# 中级定制
class Time60(object):
    'Time60 - track hours and minutes'

    def __init__(self, hr, min):
        'Time60 construct - takes hours and minutes'
        self.hr = hr
        self.min = min

    def __str__(self):
        'Time - string representation'
        return '%d:%d' % (self.hr, self.min)

    __repr__ = __str__

    def __add__(self, other):
        'Time60 - overloading the addition operator'
        return self.__class__(self.hr + other.hr,
                              self.min + other.min)
    def __iadd__(self, other):
        'Time60 - overloading in-place addition'
        self.hr += other.hr
        self.min += other.min
        return self
wed = Time60(12, 5)
print(wed)

