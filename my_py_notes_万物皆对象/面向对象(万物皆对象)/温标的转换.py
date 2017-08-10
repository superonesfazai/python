#coding:utf-8

class Temperature():
    coefficients = {'c':(1.0, 0.0, -273.15),
                    'f':(1.8, -273.15, 32.0),
                    'r':(1.8, 0.0, 0.0)}
    def __init__(self, **kwargs):
        # 默认是绝对(开氏)温度0,但可接受一个命名的参数
        # 名字可以是k,c,f或r,分别对应不同的温标
        try:
            name, value = kwargs.popitem()
        except KeyError:
            # 无参数 默认k = 0
            name, value = 'k', 0
        # 若参数过多或者参数不能识别,报错
        if kwargs or name not in 'kcfr':
            kwargs[name] = value
            raise(TypeError, 'invalid argument %r' % kwargs)
        setattr(self, name, float(value))

    def __getattr__(self, name):
        # 将c,f,r的获取映射到k的计算
        try:
            eq = self.coefficients[name]
        except KeyError:
            # 未知名字,提示错误
            raise(AttributeError, name)
        return (self.k + eq[1]) * eq[0] + eq[2]

    def __setattr__(self, name, value):
        # 将k,c,f,r的设置映射到对k的设置;并禁止其他选项
        if name in self.coefficients:
            # 名字c,f或r, 计算并设置k
            eq = self.coefficients[name]
            self.k = (value - eq[2]) / eq[0] - eq[1]
        elif name == 'k':
            # 名字是k,设置之
            object.__setattr__(self, name, value)
        else:
            # 未命名,给出错误信息
            raise(AttributeError, name)

    def __str__(self):
        # 以易读和简洁的格式打印
        return '%s K' % self.k

    def __repr__(self):
        # 以详细和准确的格式打印
        return 'Temperture(k=%r)' % self.k


t = Temperature(f = 70)
print(t.c)
t.c = 23
print(t.f)
