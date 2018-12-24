# Tor

[python-stem官网](https://stem.torproject.org/index.html)

## install
```bash
$ brew install tor
```

## 启动
启动后socks监听9050端口。
- 非后台启动
```bash
$ tor
```
- 生成HashedControlPassword
```bash
$ tor --hash-password haguagaugugxa
16:AF830A619779489260BE020F3F571B1AEEBD1FF0B2FA8A32508D4ADE23
```

```
## mac 设置方式
$ cd /usr/local/etc/tor/
$ cp torrc.sample torrc
$ vi torrc

## linux 设置方式
# 之后编辑/etc/tor/torrc加上
# 开启ControlPort，这是其它应用(python-stem)和Tor沟通的端口
ControlPort 9051

HashedControlPassword 16:872860B76453A77D60CA2BB8C1A7042072093276A3D701AD684053EC4C

# 开启cookie认证
CookieAuthentication 1

让ControlPort监听9051端口，后边那个16:开头的hash就是上一步得到的。

# 重启下tor
$ tor Socks5Proxy 127.0.0.1:1080
```

## 安装其他

### 安装python-stem
操作tor
```bash
$ pip3 install stem
```

### 安装privoxy
```bash
# Tor本身并不是HTTP代理，为了能让爬虫访问Tor网络，需要使用privoxy做为Tor的http代理。
$ brew install privoxy
# linux
$ sudo vim /etc/privoxy/config
# mac
$ vim /usr/local/etc/privoxy/config
# 添加forward-socks5(privoxy默认监听8118端口，它把http请求转向到Tor的9050端口)
forward-socks5 / 127.0.0.1:9050 .
# 重启privoxy linux
$ sudo systemctl restart privoxy
# mac
$ /usr/local/sbin/privoxy /usr/local/etc/privoxy/config
```

[note](http://blog.topspeedsnail.com/archives/7258)
