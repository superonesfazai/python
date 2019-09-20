# pytest
成熟且功能强大的单元测试框架(三方)

[github](https://github.com/pytest-dev/pytest)

[doc](http://pytest.org/en/latest/)

## install
```bash
$ pip3 install pytest
# 更新
$ pip3 install -U pytest
```

## 测试

### 在类中组合多个测试
一旦开发了多个测试，您可能希望将它们分组到一个类中。pytest可以很容易地创建一个包含多个测试的类.

pytest发现遵循其[Python测试发现约定](Python测试发现约定的)的所有测试，因此它找到两个test_前缀函数。没有必要继承任何东西

```python
# content of test_class.py
class TestClass:
    def test_one(self):
        x = "this"
        assert "h" in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, "check")
```
```bash
$ pytest -q test_class.py
.F                                                                   [100%]
================================= FAILURES =================================
____________________________ TestClass.test_two ____________________________

self = <test_class.TestClass object at 0xdeadbeef>

    def test_two(self):
        x = "hello"
>       assert hasattr(x, "check")
E       AssertionError: assert False
E        +  where False = hasattr('hello', 'check')

test_class.py:8: AssertionError
1 failed, 1 passed in 0.02s
```