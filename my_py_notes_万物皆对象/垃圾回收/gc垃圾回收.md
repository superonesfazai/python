python⾥也同java⼀样采⽤了垃圾收集机制

不过不⼀样的是: python采⽤的是引⽤计数机制为主, 分代收集机制为辅的策略

引⽤计数机制：

python⾥每⼀个东⻄都是对象， 它们的核⼼就是⼀个结构体： PyObject
```bash
typedef struct_object {
    int ob_refcnt;
    struct_typeobject *ob_type;
} PyObject;
```

PyObject是每个对象必有的内容, 其中ob_refcnt就是做为引⽤计数.

当⼀个对象有新的引⽤时, 它的ob_refcnt就会增加, 当引⽤它的对象被删除, 它的ob_refcnt就会减少
```c
#define Py_INCREF(op) ((op)->ob_refcnt++) //增加计数
#define Py_DECREF(op) \ //减少计数
if (--(op)->ob_refcnt != 0) \
    ; \
else \
    __Py_Dealloc((PyObject *)(op))
```
当引⽤计数为0时， 该对象⽣命就结束了

- 应⽤程序那颗跃动的⼼:
    - GC系统所承担的⼯作远⽐"垃圾回收"多得多, 实际上， 它们负责三个重要任务。 它们
        1. 为新⽣成的对象分配内存
        2. 识别那些垃圾对象， 并且
        3. 从垃圾对象那回收内存。