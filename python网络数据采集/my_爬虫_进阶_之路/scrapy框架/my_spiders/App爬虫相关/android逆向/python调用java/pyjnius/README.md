# pyjnius
使用JNI以Python类访问Java类的Python模块。

[github](https://github.com/kivy/pyjnius)

[docs](https://pyjnius.readthedocs.io/en/latest/api.html#jvm-options-and-the-class-path)

## 安装
```bash
pip3 install Cython
pip3 install pyjnius
```

## 使用
你需要安装一个java JDK（OpenJDK会这样做），Cython和make来构建它。请确保您的JDK_HOME或JAVA_HOME环境变量指向已安装的JDK根目录，并且您的环境变量中可以使用JVM库（jvm.so或 jvm.dll）PATH。如果不这样做可能会导致安装失败或安装成功但无法使用pyjnius库。

### 使用python-for-android
- 获取 http://github.com/kivy/python-for-android
    - pip3 install python-for-android 
- 使用kivy编译分布（将自动添加pyjnius）
- Then, you can do this kind of thing:
```python
from time import sleep
from jnius import autoclass

Hardware = autoclass('org.renpy.android.Hardware')
print('DPI is', Hardware.getDPI())

Hardware.accelerometerEnable(True)
for x in range(20):
    print(Hardware.accelerometerReading())
    sleep(.1)
```