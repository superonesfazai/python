# coding:utf-8

'''
@author = super_fazai
@File    : goods类目.py
@Time    : 2018/8/20 10:24
@connect : superonesfazai@gmail.com
'''

# parent_dir 0: 无 1: 有
_ = {
    '1688': '0',
    '淘宝': '0',
    '天猫': '0',
    '京东': '0',                      # 采集走的不是pc端, 无
    '折800': '1',                     # 常规: 1, 拼团: 1, 秒杀: 1
    '卷皮': '1',                      # 常规: 1, 拼团: 1, 秒杀: 1
    '拼多多': '0',
    '蜜芽': '1',                      # 拼团: 1, 秒杀: 1
    '蘑菇街': '0',
    '楚楚街': '0',
    '唯品会': '0',
    '聚美优品': '',
    '网易考拉': '',
    '网易严选': '',
    '小米有品': '0',
}

# SKUInfo 格式化
'''下面为未格式化数据'''
# site_id=1
_1 = [
    {
        "spec_value":"32GB|黑色【红/蓝 柄】+ 塞尔达传说|单机标配|港版",
        "detail_price":"2810",
        "rest_number":"455",
        'img_url': 'xxx',
    },
]
# site_id=2
_2 = [
    {
        "spec_value":{
            "discountPrice":"215.00",
            "canBookCount":"200"
        },
        "spec_type":"红色"
    },
]
# site_id=3, 4, 6
_3 = [
    {
        "spec_value":"AE-1000WD-1A",
        "rest_number":"3",
        "detail_price":"209",
        'img_url': 'xxxx',
    },
]

# site_id=7, 8, 9, 10
_7 = [
    {
        "spec_value":"i5精英白金版GTX1050Ti 4G|1",
        "detail_price":"6399.00",
        "img":"https://m.360buyimg.com/n12/jfs/t7942/139/3840163775/188824/39be5a8d/59ffd41dN90ac91a2.jpg!q70.jpg",
        "rest_number":""
    }
]

# site_id=11
_11 = [
    {
        "normal_price":"688",
        "rest_number":100,
        "img_url":"http://z11.tuanimg.com/imagev2/trade/800x800.9b729fe5a89220814d278b760e73f747.500x.jpg.webp",
        "detail_price":"278",
        "spec_value":"黑色|20寸"
    },
]
# site_id=12
_12 = [
    {
        "pintuan_price":"109",
        "detail_price":"109",
        "normal_price":"298",
        "img_url":"https://goods8.juancdn.com/goods/171116/e/0/5a0d7a728150a116e552a83d_800x800.jpg?imageMogr2/quality/80!/format/jpg",
        "rest_number":"50",
        "spec_value":"S|深灰色"
    },
]
# site_id=13
_13 = [
    {
        "spec_value":"白底|39",
        "detail_price":"19.9",
        "normal_price":"49",
        "img_url":"//t02img.yangkeduo.com/images/2018-03-23/51d8bde810b166d2b59cd124fd78f695.jpeg",
        "rest_number":6165,
        "is_on_sale":1
    },
]
# site_id=14 折800秒杀
_14 = [
    {
        "spec_value":"黑色|39（标准码）",
        "detail_price":"49",
        "normal_price":"119",
        "img_url":"http://z11.tuanimg.com/imagev2/trade/800x800.14a1268712f7258e82f93f80a1efe5f0.500x.jpg.webp",
        "rest_number":0
    },
]

# site_id=15
_15 = [
    {
        "rest_number":"50",
        "img_url":"https://goods6.juancdn.com/goods/180624/a/9/5b2f29adb6f8ea104e7fbb36_800x800.jpg?imageMogr2/quality/80!/format/jpg",
        "detail_price":"44.9",
        "normal_price":"199",
        "spec_value":"38|红色",
        "pintuan_price":"44.9"
    },
]

# site_id=16
_16 = [
    {
        "spec_value":"置物架Z614",
        "detail_price":"19.5",
        "normal_price":"26.9",
        "img_url":"http://omsproductionimg.yangkeduo.com/images/2018-02-01/bf896c13ac05182166f957f0b2887e29.jpeg",
        "rest_number":6918,
        "is_on_sale":1
    }
]

# 17
_17 = [
    {
        "spec_value":"7216款粉色|35",
        "pintuan_price":"80.8",
        "detail_price":"82.80",
        "normal_price":"",
        "img_url":"https://z11.tuanimg.com/imagev2/trade/800x800.37510389820c16c4ef3bceb3d47d0809.300x.jpg",
        "rest_number":98
    },
]

_18 = [
    {
        "pintuan_price":"17.9",
        "img_url":"https://goods3.juancdn.com/goods/171018/5/a/59e7549ba9fcf87d752d2733_800x800.jpg?iopcmd=convert&Q=80&dst=jpg",
        "detail_price":"19.9",
        "rest_number":"50",
        "normal_price":"56",
        "spec_value":"500克白莲子有心"
    }
]

_19 = [
    {
        "spec_value":"160/M|吊带军绿",
        "detail_price":"12.9",
        "rest_number":"437"
    },
]

_20 = [
    {
        "spec_value":"蓝柄|380ml",
        "detail_price":"99.0",
        "rest_number":50,
        "img_url":"https://img05.miyabaobei.com/d1/p5/2018/03/07/94/be/94beb9db01d7763a8a675990c3d7b070215528188.jpg@base@tag=imgScale&w=447",
        "normal_price":"169.0"
    },
]

_21 = [
    {
        "pintuan_price":"50.0",
        "detail_price":"59.0",
        "img_url":"https://img05.miyabaobei.com/d1/p5/2018/02/05/ea/1c/ea1cb5c7148726c20dcf5163d8403929124463915.jpg@base@tag=imgScale&w=447",
        "spec_value":"浅绿色",
        "normal_price":"119.0",
        "rest_number":50
    },
]

_22 = [
    {
        "rest_number":5,
        "spec_value":"黑色|S",
        "detail_price":"45.00",
        "normal_price":"84.29",
        "img_url":"https://s5.mogucdn.com/mlcdn/c45406/180730_242k41h54b2hl1753976a8a3g0ci3_640x960.jpg"
    },
]

_23 = [
    {
        "img_url":"https://s11.mogucdn.com/mlcdn/c45406/180324_7e0j9b553hgd5l5lbadj96817kb23_640x960.jpg",
        "rest_number":8822,
        "pintuan_price":"7.50",
        "spec_value":"干脆面|混合味10包",
        "detail_price":"",
        "normal_price":"11.29"
    },
]

_24 = [
    {
        "spec_value":"M|白色",
        "detail_price":"9.90",
        "rest_number":0,
        "img_url":"",
        "normal_price":"25.80"
    },
]

# site_id=25
_25 = [
    {
        'spec_value': '',
        'detail_price': '',
        'normal_price': '',
        'rest_number': 2313,  # 设置默认的值
        'img_url': '',  # 设置默认为空值
    },
]

_26 = [
    {
        "spec_value":"粉色|M（详细尺码请看详情）",
        "img_url":"http://mp5.jmstatic.com/product/197/423/df4429858197423110_std/s_df4429858197423110_800_800.jpg?imageView2/2/w/320/q/90",
        "normal_price":"199",
        "rest_number":20,
        "detail_price":"29"
    },
]

_27 = [
    {
        "spec_value":"浅绿色|均码",
        "pintuan_price":"25.8",
        "rest_number":20,
        "normal_price":"",
        "img_url":"http://mp5.jmstatic.com/product/003/636/3636278_std/3636278_800_800.jpg?_ut=1495450728&imageView2/2/w/320/q/90",
        "detail_price":"单价模式无法购买"
    },
]

_28 = [
    {
        "spec_value":"AE-1000WD-1A",
        "rest_number":"3",
        "detail_price":"209"
    },
]

# site_id=29
_29 = [
    {
        "spec_value":"66厘米|白-大心",
        "img_url":"http://pop.nosdn.127.net/be968f91-bdc3-42cc-bd10-78058183a73c?imageView&thumbnail=800x0&quality=85",
        "detail_price":"56",
        "normal_price":"80",
        "account_limit_buy_count":5,
        "rest_number":16
    },
]
# site_id=30
_30 = [
    {
        "spec_value":"自然色",
        "img_url":"",
        "detail_price":"239",
        "normal_price":"239",
        "account_limit_buy_count":5,
        "rest_number":4268
    },
]
# site_id=31
_31 = [
    {
        "spec_value":"绿色|适合1.2m床",
        "img_url":"http://img.youpin.mi-img.com/800_pic/101616_9393_61njskgsw3sm.png@base@tag=imgScale&h=350&w=350&et=1ð=480&etw=480&etc=FFFFFF",
        "detail_price":"89.0",
        "normal_price":"99.0",
        "account_limit_buy_count":5,
        "rest_number":2457
    },
]

# p_info格式化(已完成)

# 相关参数添加情况 [0: 无 1:有], sku_name为是否已加img_here字段
_ = {
    '1688': {
        'sku_name': 1,          # [{"spec_name": "颜色", "img_here": 1}, {"spec_name": "尺寸", "img_here": 0}]
        'normal_price': 0,      # 无, 只有批发价
        'img_url': 1,
    },
    '淘宝': {
        'sku_name': 1,
        'normal_price': 1,
        'img_url': 1,
    },
    '天猫': {
        'sku_name': 1,
        'normal_price': 1,
        'img_url': 1,
    },
    '京东': {
        'sku_name': 1,
        'normal_price': 0,      # 无, 只有当前售价
        'img_url': 1,
    },
    '折800': {
        'sku_name': 1,
        'normal_price': 1,      # 折800拼团商品normal_price为'', detail_price即为单购价, pintuan_price即为拼团价
        'img_url': 1,
    },
    '卷皮': {
        'sku_name': 1,
        'normal_price': 1,
        'img_url': 1,
    },
    '拼多多': {
        'sku_name': 1,
        'normal_price': 1,
        'img_url': 1,
    },
    '蜜芽': {
        'sku_name': 1,
        'normal_price': 1,
        'img_url': 1,
    },
    '蘑菇街': {
        'sku_name': 1,
        'normal_price': 1,      # 蘑菇街拼团商品detail_price为''
        'img_url': 1,
    },
    '楚楚街': {
        'sku_name': 1,
        'normal_price': 1,
        'img_url': 0,           # 无
    },
    '唯品会': {
        'sku_name': 1,
        'normal_price': 1,
        'img_url': 1,
    },
    '聚美优品': {
        'sku_name': 1,
        'normal_price': 1,      # 聚美拼团商品detail_price可能='单价模式无法购买', 表示拼团情况下如语义, normal_price为''
        'img_url': 1,
    },
    '网易考拉': {
        'sku_name': 1,
        'normal_price': 1,
        'img_url': 1,
    },
    '网易严选': {
        'sku_name': 1,
        'normal_price': 1,
        'img_url': 1,
    },
    '小米有品': {
        'sku_name': 1,
        'normal_price': 1,
        'img_url': 1,
    },
}

# 相关参数添加情况 [0: 无 1:有], sku_name为是否已加img_here字段, img_here为1表示示例图显示在spec_name, 全为0则不显示规格示例图
_ = {
    '1688': {
        'sku_name': 1,          # [{"spec_name": "颜色", "img_here": 1}, {"spec_name": "尺寸", "img_here": 0}]
    },
    '淘宝': {
        'sku_name': 1,
    },
    '天猫': {
        'sku_name': 1,
    },
    '京东': {
        'sku_name': 1,
    },
    '折800': {
        'sku_name': 1,
    },
    '卷皮': {
        'sku_name': 1,
    },
    '拼多多': {
        'sku_name': 1,
    },
    '蜜芽': {
        'sku_name': 1,
    },
    '蘑菇街': {
        'sku_name': 1,
    },
    '楚楚街': {
        'sku_name': 1,
    },
    '唯品会': {
        'sku_name': 1,
    },
    '聚美优品': {
        'sku_name': 1,
    },
    '网易考拉': {
        'sku_name': 1,
    },
    '网易严选': {
        'sku_name': 1,
    },
    '小米有品': {
        'sku_name': 1,
    },
}