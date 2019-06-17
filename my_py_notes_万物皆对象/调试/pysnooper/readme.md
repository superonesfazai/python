# PySnooper
超级火的调试器

[github](https://github.com/cool-RR/PySnooper)

## 安装
```bash
$ pip3 install pysnooper
```

## simple use
```python
import pysnooper

@pysnooper.snoop()
def test():
    index = 0
    while index < 6:
        print(index)
        
test()
```