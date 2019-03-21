# python-adb
该存储库(google开发)包含ADB和Fastboot协议的纯python实现，使用libusb1进行USB通信。

这是Android项目的ADB和fastboot代码的完整替代和重新架构

此代码主要针对需要以自动方式与Android设备通信的用户，例如自动化测试。它在客户端和设备之间没有守护进程，因此不支持同一设备的多个同时命令。与Android项目的ADB不同，它确实支持任意数量的设备，并且从不与不想要的设备通信。

[github](https://github.com/google/python-adb)

## 安装
```bash
$ pip3 install adb
```