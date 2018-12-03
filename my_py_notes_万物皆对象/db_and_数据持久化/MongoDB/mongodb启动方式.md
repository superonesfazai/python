## mongod：
* mongo 是启动MongoDB shell客户端的命令
* mongod 是启动MongoDB数据库服务的命令，主要提供了三种启动方式：

### 1. 命令行方式直接启动
mongodb默认的存储数据目录为/data/db(需要事先创建), 默认端口为27017, 也可修改为不同目录
```shell
# 首先我们创建一个数据库存储目录 /data/db
$ sudo mkdir -p /data/db

# 直接启动mongod(sudo必须)，默认数据存储目在 /data/db
$ sudo mongod

# 启动mongod，并指定数据存储目录（目录必须存在，且有读写权限）
$ sudo mongod --dbpath=/xxxxx/xxxxx
```

### 2. 配置文件方式启动
启动时加上-f参数, 并指向配置文件即可, 默认配置文件为/etc/mongod.cnf， 也可以自行编写配置文件并指定 
```shell
# 启动mongod, 并按指定配置文件执行
$ sudo mongod -f /etc/mongodb.cnf
```

### 3. 守护进程方式启动
- 启动

MongoDB提供了一种后台程序方式启动的选择，只需要加上—fork参数即可。但是注意：如果用到了--fork参数，就必须启用--logpath参数来指定log文件，这是强制的。
```
$ sudo mongod --logpath=/data/db/mongodb.log --fork

about to fork child process, waiting until server is ready for connections.
forked process: xxxxx
child process started successfully, parent exiting
```
- 关闭

如果使用--fork在后台运行mongdb服务，那么就要通过本机admin数据库向服务器发送shutdownServer()消息来关闭。
```
python@ubuntu:~$ mongo
MongoDB shell version: 3.2.8
connecting to: test

> use admin
switched to db admin

> db.shutdownServer()
server should be down...
2017-05-16T22:34:22.923+0800 I NETWORK  [thread1] trying reconnect to 127.0.0.1:27017 (127.0.0.1) failed
2017-05-16T22:34:22.923+0800 W NETWORK  [thread1] Failed to connect to 127.0.0.1:27017, reason: errno:111 Connection refused
2017-05-16T22:34:22.923+0800 I NETWORK  [thread1] reconnect 127.0.0.1:27017 (127.0.0.1) failed failed 
>
```

### 4. 启用用户认证方式启动

如果之前未定义过用户，所以mongod将允许本地直接访问操作数据库将使用本地root权限，如果使用--auth参数启动，将启用MongoDB授权认证，即启用不同的用户对不同的数据库的操作权限。
```
也可以在配置文件mongod.conf中加入auth = true按第二种启动方式启动。
```
```
# 启动mongod，并启用用户认证
python@ubuntu:~$ sudo mongod --auth
```
客户端
```
# 启动mongo shell
python@ubuntu:~$ mongo
MongoDB shell version: 3.2.8
connecting to: test

# 1. 切换admin数据库下
> use admin
switched to db admin

# 2. 创建一个拥有root权限的超级用户，拥有所有数据库的所有权限
#      用户名：python，密码：chuanzhi，角色权限：root（最高权限）
> db.createUser({user : "python", pwd : "chuanzhi", roles : ["root"]})
Successfully added user: { "user" : "python", "roles" : [ "root" ] }

# 3. 如果 MongoDB 开启了权限模式，并且某一个数据库没有任何用户时，可以不用认证权限并创建一个用户，但是当继续创建第二个用户时，会返回错误，若想继续创建用户则必须认证登录。
> db.createUser({user : "bigcat", pwd : "bigcat", roles : [{role : "read", db : "db_01"}, {role : "readWrite", db : "db_02"}]})
couldn't add user: not authorized on admin to execute command{ createUser: "bigcat", pwd: "xxx", roles: [ { role: "read", db: "db_01" }, { role: "readWrite", db: "db_02" } ], digestPassword: false, writeConcern: { w: "majority", wtimeout: 30000.0 } } :
_getErrorWithCode@src/mongo/shell/utils.js:25:13
DB.prototype.createUser@src/mongo/shell/db.js:1267:15

# 4. 认证登录到python用户（第一次创建的用户）
> db.auth("python","chuanzhi")
1
>
# 5. 查看当前认证登录的用户信息
> show users
{
    "_id" : "admin.python",
    "user" : "python",
    "db" : "admin",
    "roles" : [
        {
            "role" : "root",
            "db" : "admin"
        }
    ]
}

> 

# 6. 认证登录成功，可以继续创建第二个用户
#      用户名：bigcat，密码：bigcat，角色权限：[对db_01 拥有读权限，对db_02拥有读/写权限]
> db.createUser({user : "bigcat", pwd : "bigcat", roles : [{role : "read", db : "db_01"}, {role : "readWrite", db : "db_02"}]})
Successfully added user: {
    "user" : "bigcat",
    "roles" : [
        {
            "role" : "read",
            "db" : "db_01"
        },
        {
            "role" : "readWrite",
            "db" : "db_02"
        }
    ]
}

# 7. 查看当前数据库下所有的用户信息.
> db.system.users.find()
{ "_id" : "admin.python", "user" : "python", "db" : "admin", "credentials" : { "SCRAM-SHA-1" : { "iterationCount" : 10000, "salt" : "y/3yPLzhDKa7cJ3Zd/8DXg==", "storedKey" : "9XaUqiUteEtFAfof3k+HJjevqCA=", "serverKey" : "YjIoUPl7HTHQZuklSFXXYpZB/U4=" } }, "roles" : [ { "role" : "root", "db" : "admin" } ] }
{ "_id" : "admin.bigcat", "user" : "bigcat", "db" : "admin", "credentials" : { "SCRAM-SHA-1" : { "iterationCount" : 10000, "salt" : "ZcCaT057Gz0WODuSx70Ncg==", "storedKey" : "pNYyLMPisTcYuUHMdR46vndteIo=", "serverKey" : "IOzB2pyBRyCgKTNNSf1wljsVxms=" } }, "roles" : [ { "role" : "read", "db" : "db_01" }, { "role" : "readWrite", "db" : "db_02" } ] }

>
# 8. 认证登录到 bigcat 用户
> db.auth("bigcat", "bigcat")
1
>
# 9. 切换到 数据库db_01，读操作没有问题
> use db_01
switched to db db_01
> show collections
> 
# 10. 切换到 数据库db_02，读操作没有问题
> use db_02
switched to db db_02
> show collections
> 
# 11. 切换到 数据库db_03，读操作出现错误，bigcat用户在db_03数据库下没有相关权限
> use db_03
switched to db db_03
> show collections
2017-05-17T00:26:56.143+0800 E QUERY    [thread1] Error: listCollections failed: {
    "ok" : 0,
    "errmsg" : "not authorized on db_03 to execute command { listCollections: 1.0, filter: {} }",
    "code" : 13
} :
_getErrorWithCode@src/mongo/shell/utils.js:25:13
DB.prototype._getCollectionInfosCommand@src/mongo/shell/db.js:773:1
DB.prototype.getCollectionInfos@src/mongo/shell/db.js:785:19
DB.prototype.getCollectionNames@src/mongo/shell/db.js:796:16
shellHelper.show@src/mongo/shell/utils.js:754:9
shellHelper@src/mongo/shell/utils.js:651:15
@(shellhelp2):1:1

>
# 12. 认证登录到python用户下
> db.auth("python", "chuanzhi")
1
>
# 13. 删除bigcat用户
> db.dropUser("bigcat")
true
>
# 14. 尝试认证登录bigcat失败
> db.auth("bigcat", "bigcat")
Error: Authentication failed.
0
>
# 15. 退出mongo shell
> exit
bye
python@ubuntu:~$
```
[参考阅读](http://docs.mongoing.com/manual-zh/core/authentication.html)

## mongod部分参数说明（了解）：
* dbpath：数据文件存放路径。每个数据库会在其中创建一个子目录，防止同一个实例多次运行的mongod.lock也保存在次目录中。
* logpath：错误日志文件
* auth：用户认证
* logappend：错误日志采用追加模式(默认覆写模式)
* bind_ip：对外服务的绑定ip，一般设置为空，及绑定在本机所有可用ip上。如有需要可以单独绑定。
* port：对外服务端口。Web管理端口在这个port的基础上+1000。
* fork：以后台Daemon形式运行服务。
* journal：开启日志功能，通过保存操作日志来降低单机故障的恢复时间。
* syncdelay：系统同步刷新磁盘的时间，单位为秒，默认时60秒。
* directoryperdb：每个db存放在单独的目录中，建议设置该参数。
* repairpath：执行repair时的临时目录。如果没有开启journal，异常down机后重启，必须执行repair操作。

在源代码中，mongod的参数分为一般参数，windows参数，replication参数，replica set参数以及隐含参数。上面列举的时一般参数。
```
mongod的参数中，没有设置内存大小的相关参数，因为MongoDB使用os mmap机制
来缓存数据文件数据，自身目前不提供缓存机制。mmap在数据量不超过内存时效率很高，
但是数据超过内存后，写入的性能不太稳定。
```
