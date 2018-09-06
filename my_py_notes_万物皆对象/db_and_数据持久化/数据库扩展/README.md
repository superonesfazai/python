# 数据库扩展

## 读写分离模式
- [《Mysql主从方案的实现》](https://www.cnblogs.com/houdj/p/6563771.html)

- [《搭建MySQL主从复制经典架构》](https://www.cnblogs.com/edisonchou/p/4133148.html)

- [《Haproxy+多台MySQL从服务器(Slave) 实现负载均衡》](https://blog.csdn.net/nimasike/article/details/48048341)

- [《DRBD+Heartbeat+Mysql高可用读写分离架构》](https://www.cnblogs.com/zhangsubai/p/6801764.html)
    - DRDB 进行磁盘复制，避免单点问题。
- [《MySQL Cluster 方式》](https://coderxing.gitbooks.io/architecture-evolution/di-san-pian-ff1a-bu-luo/62-ke-kuo-zhan-de-shu-ju-ku-jia-gou/621-gao-ke-yong-mysql-de-ji-zhong-fang-an/6214-mysql-cluster-fang-an.html)

## 分片模式
- [《分库分表需要考虑的问题及方案》](https://www.jianshu.com/p/32b3e91aa22c)
    - 中间件： 轻量级：sharding-jdbc、TSharding；重量级：Atlas、MyCAT、Vitess等。
    - 问题：事务、Join、迁移、扩容、ID、分页等。
    - 事务补偿：对数据进行对帐检查;基于日志进行比对;定期同标准数据来源进行同步等。
    - 分库策略：数值范围；取模；日期等。
    - 分库数量：通常 MySQL 单库 5千万条、Oracle 单库一亿条需要分库。
- [《MySql分表和表分区详解》](https://www.2cto.com/database/201503/380348.html)
    - 分区：是MySQL内部机制，对客户端透明，数据存储在不同文件中，表面上看是同一个表。
    - 分表：物理上创建不同的表、客户端需要管理分表路由。
