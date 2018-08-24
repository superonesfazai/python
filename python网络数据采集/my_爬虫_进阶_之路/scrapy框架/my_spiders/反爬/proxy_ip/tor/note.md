# Tor

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
- 生成passwd
```bash
$ tor --hash-password haguagaugugxa
```

```
## mac 设置方式
$ cd /usr/local/etc/tor/
$ cp torrc.sample torrc
$ vi torrc

## linux 设置方式
# 之后编辑/etc/tor/torrc加上

ControlPort 9051

HashedControlPassword
16:872860B76453A77D60CA2BB8C1A7042072093276A3D701AD684053EC4C

让ControlPort监听9051端口，后边那个16:开头的hash就是上一步得到的。

# 重启下tor
```
