# 树莓派
[树莓派官网](https://www.raspberrypi.org/)

## sd卡系统刻录相关
[balenaEtcher下载](https://www.balena.io/etcher/)

![](https://i.loli.net/2019/08/24/ZeGpJaqwzThXS4m.gif)

## 树莓派Raspbian系统启用ROOT用户
树莓派的Raspbian系统root用户默认是禁用状态，且没有密码，所以要先设置个密码，然后开启才能正常使用。

```
使用pi账户进行登陆命令行，执行命令
$ sudo passwd root
新的 密码：
重新输入新的 密码：
passwd：已成功更新密码

设置root用户密码，然后在执行
$ sudo passwd --unlock root
passwd：密码过期信息已更改。

pi账户下测试是否生效root账户
$ sudo su root
```

## enable ssh
```bash
$ ssh pi@192.168.2.114
```

### 开启远程root登录(必须先在上面设置root密码)
```bash
$ sudo vi /etc/ssh/sshd_config
# 再将配置项PermitRootLoginwithout-password修改为PermitRootLogin yes，重启系统之后就可以登录
$ sudo reboot
```

```bash
$ ssh root@192.168.2.114
```

## enable vnc

## 更改密码
用户名是: pi
```bash
$ passwd
```

## vnc远程桌面连接
VNC就是一款可以让你通过手机或者电脑远程控制另一台主机的软件，在我们操作树莓派的时候，就可以通过VNC远程控制，而不再需要另外配置显示器和键盘。

现在的树莓派都默认安装VNC服务的，所以我们很简单就能通过命令行开启VNC。

首先进入系统，打开终端，或者通过远程SSH登陆树莓派。

### 开启vnc
1. 进入树莓派配置界面
```bash
$ sudo raspi-config
```
![](https://i.loli.net/2019/08/22/OE1FyNjiPzcxQvq.png)

2. 选择「5 Interfacing Options」，按回车
![](https://i.loli.net/2019/08/22/ceXR6n8mOdl2Psq.png)

3. 选择「P3 VNC」，按回车
![](https://i.loli.net/2019/08/22/ygAMwUex6JNTPiB.png)

4. 这里问你是否开启VNC服务，选择「Yes」，按回车
![](https://i.loli.net/2019/08/22/L4mzj7g29vZbAF8.png)

5. 提示已经开启VNC服务，按回车确认，之后退出树莓派配置界面
![](https://i.loli.net/2019/08/22/uty6QkzrpneObXL.png)

至此我们已经打开了树莓派的VNC服务，接下来，是通过软件进行VNC远程桌面控制。

### 使用VNC Viewer连接树莓派
推荐使用：VNC Viewer，免费易用。[下载地址](https://www.realvnc.com/en/connect/download/viewer/)

(vnc账户 已存在Chrome vnc书签)

1. 打开VNC Viewer
2. 在地址栏上面输入树莓派的IP地址(eg: 192.168.2.114)，按回车, 即可登录进入树莓派ui页

## 树莓派 Raspberry Pi 更换清华大学源更新源方法
```bash
$ sudo vim /etc/apt/sources.list
# 进入编辑界面，注释原有的内容，粘贴如下内容：
deb http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ buster main non-free contrib
deb-src http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ buster main non-free contrib

$ sudo vim /etc/apt/sources.list.d/raspi.list
# 注释原文件所有内容，用以下内容取代：
deb http://mirrors.tuna.tsinghua.edu.cn/raspberrypi/ buster main ui

$ sudo apt-get update && sudo apt-get upgrade
```

## 树莓派python开发环境搭建(下面权限都是root基础上: 先切换至root)
```bash
$ sudo su root
```

其python3版本默认是最新版

## oh-my-zsh
地址: https://github.com/robbyrussell/oh-my-zsh
```
$ sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
# 当前用户设置为zsh
chsh -s /bin/zsh

# 改变主题
vi ~/.zshrc
# 修改为pygmalion
```

### 安装python3.6.3
```bash
# 依赖安装(必须)
$ sudo apt-get install wget make gcc build-essential curl zlib* bzip2-devel openssl openssl-devel libssl-dev ncurses-devel git vim python-cffi python3-cffi libffi-dev libxml2 libxslt1.1 libxml2-dev libxslt1-dev python-libxml2 python-libxslt1 freetds-dev tmux -y --fix-missing
$ wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz
$ tar -zxvf Python-3.6.3.tgz
$ cd Python-3.6.3
$ ./configure --prefix=/usr/local/python3
$ make && make install

# 并将/usr/local/python3/bin加入PATH
$ vim ~/.zshrc
# 加入PATH=$PATH:$HOME/bin:/usr/local/python3/bin
$ source ~/.zshrc

$ pip3 install --upgrade pip
```

### python3安装opencv(非编译方式)
```
$ sudo apt-get install python-opencv libopencv-dev
```

### 安装fzutils
```bash
$ cd ~ && mkdir myFiles && cd myFiles && mkdir python

# 速度较快
$ pip3 install -i http://pypi.douban.com/simple/ numpy --trusted-host pypi.douban.com
# 安装pymssql必备
$ pip3 install -i http://pypi.douban.com/simple/ Cython --trusted-host pypi.douban.com
$ pip3 install -i http://pypi.douban.com/simple/ wheel pysocks requests requests_oauthlib selenium==3.8.0 uvloop asyncio nest_asyncio psutil pyexecjs setuptools numpy pprint chardet scrapy greenlet==0.4.14 gevent aiohttp celery flower pyexcel pyexcel-xlsx fabric jieba appium-python-client elasticsearch elasticsearch_dsl salt baidu-aip fonttools xmltodict ftfy tenacity pyzbar termcolor pypinyin bitarray click websockets==7.0 pyppeteer bunch better_exceptions scapy scapy-http demjson jsonpath pytz python-dateutil sqlalchemy pymongo redis mongoengine prettytable pika pymssql --trusted-host pypi.douban.com
$ pip3 install -i http://pypi.douban.com/simple/ flask flask_login --trusted-host pypi.douban.com
$ pip3 install -i http://pypi.douban.com/simple/ fzutils --trusted-host pypi.douban.com
```

### vim 变成IDE
代码自动补全神器

[YouCompleteMe](https://github.com/ycm-core/YouCompleteMe)
