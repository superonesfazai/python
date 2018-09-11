# charles

## 添加SSL Proxying
证书安装完毕后，还需要对SSL做以下处理：

1. 进入"Proxy" -> "SSL Proxying Settings"
2. 勾选"Enable SSL Proxying"，并点击下方的Add
3. 在弹出的"Edit Location"中，输入Host和Port都为"＊"（看提示这样配置可以抓到所有https的包），然后进行添加

以上设置完毕后就可以正常抓取数据了。

## NOTICE
一些app会设置主流抓包软件无法抓取其关键接口

eg: 检测到中间人即返回403

解决方案: 
1. wireshark(可抓udp, tcp)
2. 非主流抓包软件如stream(IOS)
