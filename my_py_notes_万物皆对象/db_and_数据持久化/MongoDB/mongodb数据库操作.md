MongoDB 将数据存储为一个文档，数据结构由键值(key=>value)对组成。MongoDB 文档类似于 JSON 对象。字段值可以包含其他文档，数组及文档数组。
![](https://i.loli.net/2019/09/24/db2h8cw1vsYBV4o.png)

#### 集合
文档组，类似于关系数据库中的表格。

集合存在于数据库中，一个数据库可以包含很多个集合。集合没有固定的结构，这意味着你在对集合可以插入不同格式和类型的数据，但通常情况下我们插入集合的数据都会有一定的关联性。

比如，我们可以将以下不同数据结构的文档插入到集合中：
```html
{"site":"www.baidu.com"}
{"site":"www.google.com","name":"Google"}
{"site":"www.xxx.cn","name":"xxx","num":100}
```
当第一个文档插入时, 集合就会被创建

#### 文档
文档是一组键-值对
![](https://i.loli.net/2019/09/24/8zBisFW7IT1LNxZ.jpg)

## RDBMS VS MongoDB
下面给出的表显示RDBMS(关系型数据库)术语与MongoDB的关系

![](https://i.loli.net/2019/09/24/6mDU9VsM5IYjbdp.png)

通过下图实例, 我们也可以更直观的了解Mongo中的一些概念

![](https://i.loli.net/2019/09/24/aSGhQpnCeEOHL4B.png)

#### 示例文档
下面给出的示例显示了一个博客网站, 这是一个类似于json对象键值对文档结构
```html
{
   _id: ObjectId("57146ec5de7375577083d127")
   title: 'MongoDB Overview', 
   description: 'MongoDB is no sql database',
   by: 'itcast.cn',
   url: 'http://www.itcast.cn',
   tags: ['mongodb', 'database', 'NoSQL'],
   likes: 100, 
   comments: [  
      {
         user:'user1',
         message: 'My first comment',
         dateCreated: new Date(2017,4,20,2,15),
         like: 0 
      },
      {
         user:'user2',
         message: 'My second comments',
         dateCreated: new Date(2017,4,25,7,45),
         like: 5
      }
   ]
}
```

### 数据库命令
* 连接成功后, 默认使用test数据库
* 查看当前数据库名称
```html
> db
```
* 查看所有数据库名称, 列出所有在物理上存在的数据库
```html
> show dbs
```
* 切换数据库, 如果数据库不存在也并不创建, 直接插入数据或创建集合时数据库才被创建
```html
> use 数据库名称
```
* 删除当前指向的数据库, 如果数据库不存在, 则什么也不做
```html
> db.dropDatabase()
```
