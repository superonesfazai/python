# better_exceptions

## 安装
```shell
$ pip3 install better_exceptions
```

并将Better_Exceptions环境变量设置为以下值：
```shell
$ export BETTER_EXCEPTIONS=1  # Linux / OSX
$ source ~/.zshrc 

$ setx BETTER_EXCEPTIONS 1    # Windows
```

如果要允许输出整个值而不是截断为一定数量的字符：
```python
import better_exceptions
better_exceptions.MAX_LENGTH = None
```