# 关闭docker中的jenkins
因为是自启动
```bash
$ docker ps
CONTAINER ID        IMAGE                 COMMAND                  CREATED             STATUS              PORTS                                              NAMES
40e282de8083        jenkins/jenkins:lts   "/sbin/tini -- /usr/…"   2 weeks ago         Up 10 minutes       0.0.0.0:8080->8080/tcp, 0.0.0.0:50000->50000/tcp   docker_jenkins
# 关闭该容器
$ docker stop 40e282de8083
# docker 设置开机自启动
$ systemctl enable docker.service
# 关闭开机自启动
$ systemctl disable docker.service 
```