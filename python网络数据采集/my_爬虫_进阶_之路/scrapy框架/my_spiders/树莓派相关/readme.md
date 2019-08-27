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

### 使用VNC Viewer连接树莓派(vnc 除非设置内网穿透，固定公网IP或者花生壳动态域名解析，才可外网访问)
推荐使用：VNC Viewer，免费易用。[下载地址](https://www.realvnc.com/en/connect/download/viewer/)

(vnc账户 已存在Chrome vnc书签)

1. 打开VNC Viewer
2. 在地址栏上面输入树莓派的IP地址(eg: 192.168.2.114)，按回车, 即可登录进入树莓派ui页

## teamviewer
teamviewer 则可实现内网穿透 让外网访问

而teamviewer则登陆账户设置连接密码则可被世界上任意一台主机访问

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
$ sudo apt-get install wget make gcc build-essential curl zlib* bzip2-devel openssl openssl-devel libssl-dev ncurses-devel git vim python-cffi python3-cffi libffi-dev libxml2 libxslt1.1 libxml2-dev libxslt1-dev python-libxml2 python-libxslt1 freetds-dev tmux sqlite3 libsqlite3-dev -y --fix-missing
$ wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz
$ tar -zxvf Python-3.6.3.tgz
$ cd Python-3.6.3
$ ./configure --prefix=/usr/local/python3 --enable-loadable-sqlite-extensions
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
$ pip3 install -i http://pypi.douban.com/simple/ pillow wheel pysocks requests requests_oauthlib requests_toolbelt selenium==3.8.0 uvloop asyncio nest_asyncio psutil pyexecjs setuptools numpy pprint chardet scrapy greenlet==0.4.14 gevent aiohttp celery flower pyexcel pyexcel-xlsx fabric jieba appium-python-client elasticsearch elasticsearch_dsl salt baidu-aip fonttools xmltodict ftfy tenacity pyzbar termcolor pypinyin bitarray click websockets==7.0 pyppeteer bunch better_exceptions scapy scapy-http demjson jsonpath pytz python-dateutil sqlalchemy pymongo redis mongoengine prettytable pika pymssql --trusted-host pypi.douban.com
$ pip3 install -i http://pypi.douban.com/simple/ flask flask_login --trusted-host pypi.douban.com
$ pip3 install -i http://pypi.douban.com/simple/ fzutils --trusted-host pypi.douban.com
```

### 常用shell
```bash
# 查看cpu温度
$ watch -n 0.1 echo CPU: $[$(cat /sys/class/thermal/thermal_zone0/temp)/1000]°
or 
$ vcgencmd measure_temp

# 查看某文件最后几行
$ tail -n 200 xx.log
```

### man (查看某个命令用法)
```bash
$ man unzip
```

#### fzf (超快的命令行模糊查找器)(强烈推荐, 相见恨晚!!)
```bash
# github: https://github.com/junegunn/fzf
$ apt-get install fzf
# 用法
$ fzf 

# 切换当前工作目录
# 通过下面方式进入fzf, 选中目标目录回车即可进入
$ cd $(find * -type d | fzf)
```

#### cloc
```bash
# 代码统计工具
$ apt-get install cloc
# use
$ cloc xxx.py
```

#### thefuck (纠正您控制台命令错误)(强烈推荐, 详见恨晚!!)
```bash
# github: https://github.com/nvbn/thefuck
$ pip3 install thefuck
$ vi ~/.zshrc 
# 加入这行
eval $(thefuck --alias)
$ source ~/.zshrc

# 用法
root@raspberrypi:~|⇒  aptget update
zsh: command not found: aptget
root@raspberrypi:~|⇒  fuck
apt-get update [enter/↑/↓/ctrl+c]
```

#### nload (查看主机网络流量)
```bash
$ apt-get install nload
# use
$ nload
```

### git 加速
[blog](https://blog.csdn.net/w958660278/article/details/81161224)

打开https://www.ipaddress.com/

查询以下三个链接的DNS解析地址 (修改下方的ip, 再存入)
1. github.com 
2. assets-cdn.github.com 
3. github.global.ssl.fastly.net

```bash
$ vi /etc/hosts
# 加入下方
192.30.253.112     github.com
185.199.108.153    assets-cdn.github.com
151.101.185.194    github.global.ssl.fastly.net
# 刷新dns
$ sudo /etc/init.d/networking restart
```

然后速度起飞!

### 驱动
```bash
# 否则无法启动chromedriver
$ apt-get install chromium-browser && apt-get install libnss3 libgconf-2-4

# 否则无法启动firefoxdriver
# 树莓派安装firefox
$ sudo apt-get install firefox-esr

# 树莓派安装phantomjs(我已下载到本地直接运行即可)
# 下面是原先的, 但是动态切换代理失败!! pass
$ apt-get install chrpath git-core libfontconfig1-dev libxft-dev 
$ cd ~/myFiles/linux_drivers
$ wget https://github.com/aeberhardo/phantomjs-linux-armv6l/archive/master.zip && unzip master.zip
$ rm -rf master.zip
# 即可得到在树莓派上能运行的phantomjs
$ cd phantomjs-linux-armv6l-master && tar -jxvf phantomjs-1.9.0-linux-armv6l.tar.bz2 
# 更改路径至(文件名得一致) '/root/myFiles/linux_drivers/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'

# 装2.1.1 gitHub: https://github.com/ApioLab/phantomjs-2.1.1-linux-arm
$ apt-get install chrpath git-core libfontconfig1-dev libxft-dev 
$ cd ~/myFiles/linux_drivers
$ wget https://raw.githubusercontent.com/ApioLab/phantomjs-2.1.1-linux-arm/master/phantomjs-2.1.1-linux-arm.tar.bz2
# 解压即可得到在树莓派上能运行的phantomjs
$ tar -jxvf phantomjs-2.1.1-linux-arm.tar.bz2
# 更改路径至(文件名得一致) '/root/myFiles/linux_drivers/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'
# 运行./phantomjs 报错:
# ./phantomjs: error while loading shared libraries: libssl.so.1.0.0: cannot open shared object file: No such file or directory
# blog: https://blog.csdn.net/uniom/article/details/54092570
```

### 禁用wifi
```bash
$ vi /etc/modprobe.d/raspi-blacklist.conf
# 加上
# wifi
blacklist brcmfmac
blacklist brcmutil
# 蓝牙
# blacklist btbcm
# blacklist hci_uart
$ reboot
```

### 解决树莓派使用HDMI-VGA转换器黑屏的方案(如果外接显示器的话, 一般不设置已cli模式)
设置树莓派默认启动页(desktop/shell)
```bash
$ sudo raspi-config
# 1. 选择Boot Options
# 2. 选择Desktop/cli
# 3. 选择B3 Desktop
# 4. 回车, 保存更改并reboot即可
```

### vim 变成IDE
代码自动补全神器

[YouCompleteMe](https://github.com/ycm-core/YouCompleteMe)

## 外网访问树莓派

### cpolar(推荐)
如果你曾尝试将树莓派（Raspberry Pi）设置成为物联网设备，你就会知道，除非你跳过一大堆恼人的内网穿透问题，否则你就无法在本地网络上提供网页和数据。从家庭或本地网络外部访问树莓派可能是一项挑战。

cpolar是一种安全的隧道服务，可以在任何地方在线提供您的设备。 隧道是一种在两台计算机之间通过互联网等公共网络建立专线的方法。 当您在两台计算机之间设置隧道时，它应该是安全且私有的，并且能够通过网络障碍，如端口阻塞路由器和防火墙。 这是一个方便的服务，允许您在安全的无线网络或防火墙后面将请求从公共互联网连接到本地计算机。 使用此平台，您可以通过非常简单的方式从家庭或本地网络外部访问Raspberry Pi。

[开始页](https://dashboard.cpolar.com/get-started)

### 安装
```bash
$ sudo wget https://www.cpolar.com/static/downloads/cpolar-stable-linux-arm.zip
$ sudo unzip cpolar-stable-linux-arm.zip && rm -rf cpolar-stable-linux-arm.zip
```

### 注册
免费版的cpolar允许您一次访问一个终端，并在每次启动cpolar时分配随机网址。 使用免费版本，您每次希望建立远程连接并与远程用户共享地址时，都必须从Pi生成主机地址。

要创建cpolar帐户，请单击此处，然后单击注册以获取authtoken密钥。 如果您希望自己的自定义域执行联机SSH，则此令牌是必需的。

登录到cpolar网站后，您将获得一个authtoken密钥，其中包含许多字符的组合。 您需要保密此令牌：拥有此令牌的任何人都可以访问您的Raspberry Pi。

[获取自己账户的认证代码](https://dashboard.cpolar.com/get-started)

使用您从cpolar网站获得的令牌更改yourauthtoken字符串。 您只需要为Raspberry pi执行一次认证，它就会存储在配置文件中。

```bash
$ ./cpolar authtoken xxxxx[你的账号的认证代码]
Authtoken saved to configuration file: /root/.cpolar/cpolar.yml
```

### 远程连接

#### 使用ssh从远程网络访问Pi
在Raspberry Pi终端中键入以下命令以启用从远程访问Putty终端。
```bash
$ ./cpolar tcp 22
```

![](https://i.loli.net/2019/08/27/dn8XS5BmUPjuC2s.png)

如果你的隧道状态为“online”，你可以在任何地方使用Putty打开你的Raspberry Pi终端。 注意下图所示的主机地址和端口号; 你将使用它们来访问Raspberry Pi。

远程ssh
```bash
$ ssh <树莓派用户名@1.tcp.cpolar.io> -p <cpolar公网端口号>  

# 本例子
$ ssh root@1.tcp.cpolar.io -p 10012
参数说明：
-p 参数 指定服务器端口号
10012 是上图cpolar分配给你的服务器端口号，每次会变化
1.tcp.cpolar.io 是服务器分配给你的服务器主机地址，每次会变化
root 是树莓派默认用户名
```

### http访问pi
要在端口80上启动HTTP隧道
```bash
$ ./cpolar http 80
```
![](https://i.loli.net/2019/08/27/ipgJnWKuZfFT7vk.png)

如果你的隧道状态为“online”，你可以在任何地方使用浏览器连接Raspberry Pi终端

浏览器访问
```bash
# 例子
http://4e9c5588.cpolar.io
https://4e9c5588.cpolar.io
```