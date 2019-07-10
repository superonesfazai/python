# pychrome
适用于Google Chrome开发协议的Python包，[更多文档](https://fate0.github.io/pychrome/)

[github](https://github.com/fate0/pychrome)

## 安装
```shell
$ pip3 install pychrome
# 更新
$ pip3 install pychrome -U
```

## 设置Chrome
只是：
```shell
$ google-chrome --remote-debugging-port=9222
```

或无头模式（chrome版本> = 59）：
```shell
$ google-chrome --headless --disable-gpu --remote-debugging-port=9222
```
或使用docker(推荐)：
```shell
$ docker pull fate0/headless-chrome
$ docker run -it --rm --name fate0-chrome --cap-add=SYS_ADMIN -p 9222:9222 fate0/headless-chrome
```

## 标签管理
运行pychrome -h更多信息


## 更多例子
[更多例子](https://github.com/fate0/pychrome/tree/master/examples)