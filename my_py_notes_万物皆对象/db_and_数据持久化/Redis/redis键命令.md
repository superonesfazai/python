## redis键命令
#### 1.keys *: 查看所有键
```html
keys *
```
#### 2. 使用通配符 *：查看名称中包含a的键
```
keys '*a*'
```
#### 3. exists 判断键是否存在：如果存在返回1，不存在返回0
```
exists key1 keys2 ...
```
#### 4. type 查看键对应的value的类型
```
type key
```
#### 5. del 删除键及对应的值
```
del key1 key2 ...
```
#### 6. expire 设置过期时间
* 以秒为单位，如果没有指定过期时间则一直存在，直到使用DEL移除
```
expire key 60
```
#### 7. ttl 查看有效时间，以秒为单位
```
ttl key
```

#### 8. persist (立刻执行persist命令，该存在超时的键变成持久化的键，即将该Key的超时去掉)
```html
redis 127.0.0.1:6379> persist mykey
(integer) 1
# ttl的返回值告诉我们，该键已经没有超时了。
redis 127.0.0.1:6379> ttl mykey
(integer) -1
```

#### 9. 删除所有Key
* 删除所有Key，可以使用Redis的flushdb和flushall命令
//删除当前数据库中的所有Key  
```
flushdb  
```
* //删除所有数据库中的key  
```
flushall  
```

#### 10. 查看所有配置信息
```bash
config get *
```

#### 11. 切换db
```bash
select 2
```