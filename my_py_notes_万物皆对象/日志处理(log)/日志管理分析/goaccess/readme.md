# goaccess
GoAccess是一个开源的实时网络日志分析器和交互式查看器，可在* nix系统上或通过 浏览器在终端中运行。它为需要动态可视化服务器报告的系统管理员提供快速且有价值的HTTP统计信息。

[github](https://github.com/allinurl/goaccess)

## 安装
```bash
# mac
$ brew install goaccess
```

## simple use
输出 html

```bash
$ goaccess /var/log/nginx/access.log -a > report.html
```
注意：输出报告时，请记得看终端提示，是否提示有 log-format，time-format 等格式错误，如果有，到 /etc/goaccess.conf 里面修改。