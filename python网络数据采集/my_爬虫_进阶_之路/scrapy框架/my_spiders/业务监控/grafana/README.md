# grafana
Grafana 是一款采用 go 语言编写的开源应用

- grafana是用于可视化大型测量数据的开源程序，他提供了强大和优雅的方式去创建、共享、浏览数据。dashboard中显示了你不同metric数据源中的数据。
- grafana最常用于因特网基础设施和应用分析，但在其他领域也有机会用到，比如：工业传感器、家庭自动化、过程控制等等。
- grafana有热插拔控制面板和可扩展的数据源，目前已经支持Graphite、InfluxDB、OpenTSDB、Elasticsearch。

## 安装
```bash
$ brew install grafana
```

## 启动
要使用自制服务启动Grafana，请首先确保已安装homebrew / services。

`brew tap homebrew/services`

然后使用以下方式启动Grafana
```bash
# 启动
brew services start grafana
# 停止
brew services stop grafana
```

用户名与密码都是admin

## 配置
配置文件应位于
```
/usr/local/etc/grafana/grafana.ini
```

## 插件
如果你想手动安装一个插件，请点击此处
```bash
/usr/local/var/lib/grafana/plugins
```

## 浏览器
```bash
$ open http://localhost:3000
```