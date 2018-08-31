# fz_proxy_pool
fz的分布式代理ip池

## 架构
celery + redis + spiders6770934mmm

## 启动
#### 1. redis
- 安装redis
```bash
# mac
$ brew install redis
```
- 启动redis
```bash
# server
$ redis-server

# cli客户端
$ redis-cli 
```

#### 2. 运行proxy_spiders_tasks worker
```bash
$ celery -A proxy_tasks worker -l info
```

#### 3. python3 main.py

