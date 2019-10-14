# coding:utf-8

'''
@author = super_fazai
@File    : my_client.py
@connect : superonesfazai@gmail.com
'''

"""
测试server端的接口签名
"""

import sys
sys.path.append('..')

import hashlib
from base64 import b64encode
from requests import get

from settings import IP_POOL_TYPE

from fzutils.spider.async_always import *

class RequestClient(AsyncCrawler):
    """ 接口签名client示例 """
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            ip_pool_type=IP_POOL_TYPE,
        )
        # 并发数
        self.concurrency = 6
        # 最大请求数
        self.max_req_num = 6
        self._version = "v1"
        self._access_key_id = "yiuxiu"
        self._access_key_secret = "22879be192793e9d80289b58a451f857"
        self.md5 = lambda pwd: hashlib.md5(pwd).hexdigest()
        self.get_current_timestamp = lambda: datetime_to_timestamp(get_shanghai_time())

    def _sign(self, parameters:dict) -> str:
        '''
        签名
        :param parameters: url请求参数(包含除signature外的公共参数)
        :return:
        '''
        if "sign" in parameters:
            parameters.pop("sign")

        # NO.1 参数排序(正序)
        _my_sorted = sorted(parameters.items(), key=lambda parameters: parameters[0])

        # NO.2 排序后拼接字符串
        canonicalized_query_string = ''
        for (k, v) in _my_sorted:
            canonicalized_query_string += '{}={}&'.format(k, v)

        # eg: access_key_id=yiuxiu&goods_link=aHR0cHM6Ly9oNS5tLnRhb2Jhby5jb20vYXdwL2NvcmUvZGV0YWlsLmh0bT9pZD01NTEwNDc0NTQxOTg=&t=1536802300&v=v1&22879be192793e9d80289b58a451f857
        canonicalized_query_string += self._access_key_secret

        # NO.3 加密返回签名: sign(小写, md5加密)
        sign = self.md5(canonicalized_query_string.encode('utf-8')).lower()
        # print('sign:{}'.format(sign))

        return sign

    async def _fck_run(self):
        await self.concurrent_test()

    async def concurrent_test(self):
        """
        并发测试
        :return:
        """
        def get_tasks_params_list(url):
            tasks_params_list = []
            for index in range(0, self.max_req_num):
                tasks_params_list.append({
                    'url': url,
                })

            return tasks_params_list

        def get_create_task_msg(k) -> str:
            return 'create task[where url: {}] ...'.format(
                k['url'],
            )

        def get_now_args(k) -> list:
            return [
                k['url'],
            ]

        url = self.get_target_url()
        all_res = await get_or_handle_target_data_by_task_params_list(
            loop=self.loop,
            tasks_params_list=get_tasks_params_list(url=url),
            func_name_where_get_create_task_msg=get_create_task_msg,
            func_name=self._request,
            func_name_where_get_now_args=get_now_args,
            func_name_where_add_one_res_2_all_res=default_add_one_res_2_all_res2,
            one_default_res={},
            step=self.concurrency,
            get_all_res=True,)
        pprint(all_res)

    def get_target_url(self) -> str:
        """
        获取目标url
        :return:
        """
        # NOTICE:
        # goods_link = 'https://h5.m.taobao.com/awp/core/detail.htm?id=551047454198&umpChannel=libra-A9F9140EBD8F9031B980FBDD4B9038F4&u_channel=libra-A9F9140EBD8F9031B980FBDD4B9038F4&spm=a2141.8147851.1.1'
        # 由于: link中不能带&否则会被编码在sign中加密, 因此先进行b64encode格式化再decode

        # tb
        # goods_link = 'https://item.taobao.com/item.htm?spm=a219r.lmn002.14.1.3b7e12d56SCJjf&id=575507061506&ns=1&abbucket=16'
        # tm
        # goods_link = 'https://detail.tmall.hk/hk/item.htm?spm=a1z10.5-b-s.w4011-16816054130.101.3e6227dfLIwIrR&id=555709593338&rn=2563b85d76e776e4dd26a13103df62bd&abbucket=6'
        # jd
        # goods_link = 'https://item.m.jd.com/ware/view.action?wareId=3713001'
        # goods_link = 'https://item.jd.com/5025518.html'

        # article_link = 'https://www.toutiao.com/a6623270159790375438/'
        # article_link = 'https://www.jianshu.com/p/1a60bdc3098b'

        # qq看点
        # article_link = 'https://post.mp.qq.com/kan/article/2184322959-232584629.html?_wv=2147483777&sig=24532a42429f095b9487a2754e6c6f95&article_id=232584629&time=1542933534&_pflag=1&x5PreFetch=1&web_ch_id=0&s_id=gnelfa_3uh3g5&share_source=0'
        # todo 含视频(本地可以, server失败[原因selenium 与firefox和geckodriver不兼容启动geckodriver失败, 即使firefox和geckodriver皆为最新版本])
        # article_link = 'http://post.mp.qq.com/kan/video/200553568-1375d3f1b48697ah-j0906gh4g62.html?_wv=2281701505&sig=e1dfb38fc2d5eaa0fd4400b05c94d17c&time=1564417414&iid=Mjc3Mzg2MDk1OQ==&sourcefrom=6'

        # 微信
        # article_link = 'https://mp.weixin.qq.com/s?src=11&timestamp=1557111601&ver=1589&signature=ALBo1FMtv3X*yJa8CzViSYK*FV-Cr7rHblhsr-96NCZDD5jK8ra2daIg2QWCSVnnqJ4H4KJG*n820P0PULQ6PIQblWXUf*7R69P8ObOCR7UJmpRlKU8s2FgRFiUMrR7N&new=1'
        # article_link = 'https://mp.weixin.qq.com/s?src=11&timestamp=1563850802&ver=1745&signature=kF7BFCtTqr9OlfBzqLSgUfnD413Ig9JfMVKCc1ew8YQ8maPdhL8zFXgrctDdl5Z3HfI0ZOb7yThhKR1QHrtuUjVQE*gTTPBvBOTagAA5wN*bylpMTtwBqwv7ctFh-j5P&new=1'
        # article_link = 'https://mp.weixin.qq.com/s?src=11&timestamp=1563850802&ver=1745&signature=kF7BFCtTqr9OlfBzqLSgUfnD413Ig9JfMVKCc1ew8YQ8maPdhL8zFXgrctDdl5Z3HfI0ZOb7yThhKR1QHrtuUjVQE*gTTPBvBOTagAA5wN*bylpMTtwBqwv7ctFh-j5P&new=1'
        # article_link = ' https://mp.weixin.qq.com/s?src=11&timestamp=1568253601&ver=1847&signature=g3Udtoe0dc75qCfQ6nVgjOsV2m0ipYDEjWAJ-IpyYbVqBQsHT6vU739bYLf90jkKwocVVJM5k5O3ELWGKsGYwCleIUee7YlXN0oyvLcMPfnQqXbXJmihMY0KBR2EKfk*&new=1'

        # kb
        # 图文
        # article_link = 'https://kuaibao.qq.com/s/20190723A0IRBX00?refer=kb_news&amp;titleFlag=2&amp;coral_uin=ec30afdb64e74038ca7991e4e282153af308670081f17d0ee4fc3e473b0b5dda2f&amp;omgid=22c4ac23307a6a33267184cafd2df8b6&from=groupmessage&isappinstalled=0'
        # 视频(有一定失败率多尝试)
        # 第一种类型
        # article_link = 'https://kuaibao.qq.com/s/20190322V0DCSY00?refer=kb_news&amp;coral_uin=ec2fef55983f2b0f322a43dc540c8dda94190bf70c60ca0d998400a23f576204fb&amp;omgid=7a157262f3d303c6f2d089446406d22e&amp;chlid=daily_timeline&amp;atype=4&from=groupmessage&isappinstalled=0'
        # 第二种类型
        # article_link = 'https://kuaibao.qq.com/s/20190221V170RM00?refer=kb_news&amp;titleFlag=2&amp;coral_uin=ec2fef55983f2b0f322a43dc540c8dda94190bf70c60ca0d998400a23f576204fb&amp;omgid=7a157262f3d303c6f2d089446406d22e&from=groupmessage&isappinstalled=0'
        # article_link = 'https://kuaibao.qq.com/s/20190509V0JOTG00?refer=kb_news&amp;titleFlag=2&amp;coral_uin=ec2fef55983f2b0f322a43dc540c8dda94190bf70c60ca0d998400a23f576204fb&amp;omgid=7a157262f3d303c6f2d089446406d22e&from=groupmessage&isappinstalled=0'

        # 搜狗头条
        # article_link = 'https://sa.sogou.com/sgsearch/sgs_tc_news.php?req=xtgTQEURkeIQnw4p57aSHd9gihe6nAvIBk6JzKMSwdJ_9aBUCJivLpPO9-B-sc3i&user_type=wappage'
        # article_link = 'http://sa.sogou.com/sgsearch/sgs_video.php?mat=11&docid=sf_307868465556099072&vl=http%3A%2F%2Fsofa.resource.shida.sogoucdn.com%2F114ecd2b-b876-46a1-a817-e3af5a4728ca2_1_0.mp4'
        # article_link = 'http://sa.sogou.com/sgsearch/sgs_video.php?mat=11&docid=286635193e7a63a24629a1956b3dde76&vl=http%3A%2F%2Fresource.yaokan.sogoucdn.com%2Fvideodown%2F4506%2F557%2Fd55cd7caceb1e60a11c8d3fff71f3c45.mp4'

        # 东方头条
        # article_link = 'https://mini.eastday.com/mobile/190505214138491.html?qid=null&idx=1&recommendtype=crb_a579c9a168dd382c_1_1_0_&ishot=1&fr=toutiao&pgnum=1&suptop=0'
        # article_link = 'https://mini.eastday.com/video/vgaoxiao/20190506/190506045241686142077.html?qid=null&idx=6&recommendtype=-1_a579c9a168dd382c_1_6_0_&ishot=1&fr=toutiao&pgnum=1&suptop=0'
        # 百度m站
        # article_link = 'https://mbd.baidu.com/newspage/data/landingpage?s_type=news&dsp=wise&context=%7B%22nid%22%3A%22news_9512351987809643964%22%7D&pageType=1&n_type=1&p_from=-1'

        # bd好看视频
        # article_link = 'https://m.baidu.com/#iact=wiseindex%2Ftabs%2Fnews%2Factivity%2Fnewsdetail%3D%257B%2522linkData%2522%253A%257B%2522name%2522%253A%2522iframe%252Fmib-iframe%2522%252C%2522id%2522%253A%2522feed%2522%252C%2522index%2522%253A0%252C%2522url%2522%253A%2522https%253A%252F%252Fhaokan.baidu.com%252Fvideoui%252Fpage%252Fsearchresult%253Fpd%253Dwise%2526vid%253D8197562812859491736%2526innerIframe%253D1%2522%252C%2522isThird%2522%253Afalse%252C%2522title%2522%253Anull%257D%257D'
        # 推荐栏上边点击视频进入的tab, 所得的到视频地址
        # article_link = 'https://sv.baidu.com/videoui/page/videoland?context=%7B%22nid%22%3A%22sv_7865563634675285012%22%7D&pd=feedtab_h5&pagepdSid='

        # 阳光宽频
        # article_link = 'https://www.365yg.com/a6690781947519566350/#mid=1622709093855239'

        # 凤凰网
        # article_link = 'https://news.ifeng.com/c/7nDvcZ4NtW1'
        # 含视频的
        # article_link = 'https://v.ifeng.com/c/7nE1XJY8fL6'

        # 51健康养生网
        # article_link = 'http://www.51jkst.com/article/275325/index.html'

        # 彩牛养生网
        # 视频
        # article_link = 'http://m.cnys.com/yiliao/1784.html'
        # 文章
        # article_link = 'http://m.cnys.com/yangshengzixun/2158.html'

        # 爱范儿
        # 视频
        # article_link = 'https://www.ifanr.com/video/1195120'
        # 图文
        # article_link = 'https://www.ifanr.com/1227137'
        # article_link = 'https://www.ifanr.com/app/1257907'

        # 科学松鼠会
        # article_link = 'https://songshuhui.net/archives/101270'

        # 界面新闻
        # article_link = 'https://www.jiemian.com/article/3265195.html'
        # 视频
        # article_link = 'https://www.jiemian.com/video/AGQCNwhhB24BP1Vh.html'

        # 澎湃网
        # article_link = 'https://m.thepaper.cn/newsDetail_forward_3839854'

        # 虎嗅网
        # article_link = 'https://m.huxiu.com/article/308402.html'

        # 南方周末
        # article_link = 'http://www.infzm.com/wap/#/content/153854'
        # article_link = 'http://www.infzm.com/wap/#/content/158165'

        # 好奇心日报
        # article_link = 'http://m.qdaily.com/mobile/articles/63484.html'

        # 西瓜视频
        # article_link = 'https://www.ixigua.com/i6623552886510977540/'

        # 梨视频
        # article_link = 'https://www.pearvideo.com/video_1584404'

        # 艾墨镇
        # article_link = 'https://aimozhen.com/view/15960/'

        # 美拍
        # article_link = 'https://www.meipai.com/media/1131644923'

        # 好看视频
        # article_link = 'https://haokan.baidu.com/v?vid=17448170737812377575&tab=shishang'

        # 七丽女性网
        # article_link = 'https://i.7y7.com/jiaju/97/386197.html'

        # 亲亲宝贝
        # article_link = 'https://m.qbaobei.com/v/video_25.html'

        # 发条网
        # article_link = 'https://mqtwj.fatiao.pro/detail/8937.html'

        # 觅糖
        # 视频
        # article_link = 'https://www.91mitang.com/pages/91022'
        # 图文
        # article_link = 'https://www.91mitang.com/pages/2106106'

        # 梨视频
        # article_link = 'https://www.pearvideo.com/video_1584072'
        # article_link = 'https://www.pearvideo.com/video_1598014'

        # 七丽女性网
        # article_link = 'https://i.7y7.com/hufu/84/385784.html'
        # article_link = 'https://i.7y7.com/hufu/37/385737.html'

        # 亲亲宝贝网
        # article_link = 'https://m.qbaobei.com/a/1372711.html'

        # 雪球
        # article_link = 'https://xueqiu.com/5157574024/130400677'

        # 5号女性网
        # article_link = 'http://m.5h.com/yl/148912.html'

        # 百思不得姐
        # article_link = 'http://www.budejie.com/detail-29752617.html'

        # 发条网
        # article_link = 'https://mart.fatiao.pro/detail/1522.html'

        # 来福爆笑娱乐网
        # article_link = 'http://www.laifudao.com/tupian/87109.htm?xid=tupian87109'

        # bilibili(firefox可正常打开, 但是cp server无法下载)
        article_link = 'https://www.bilibili.com/video/av60965559?spm_id_from=333.334.b_62696c695f67756f636875616e67.42'

        url = article_link

        return url

    def _request(self, target_url) -> str:
        '''
        测试用例
        :return:
        '''
        article_link = target_url

        now_timestamp = self.get_current_timestamp() - 5
        print('请求时间戳为: {}[{}]'.format(now_timestamp, str(timestamp_to_regulartime(now_timestamp))))
        new_url = b64encode(s=article_link.encode('utf-8')).decode('utf-8')
        print('b64编码后的article_link: {}'.format(new_url))
        params = {
            'access_key_id': self._access_key_id,
            'v': self._version,
            't': now_timestamp,                                                         # 10位
            # 'goods_link': b64encode(s=goods_link.encode('utf-8')).decode('utf-8'),  # 传str, 不传byte, server会识别
            'article_link': new_url,
        }
        # params.update({
        #     'sign': self._sign(params)
        # })
        # print('params如下:')
        # pprint(params)

        # url = 'http://127.0.0.1:5000/api/goods'

        # rpc 远程过程调用
        # 淘宝天猫调这个
        # url = 'http://spider.taobao_tmall.k85u.com/api/goods'
        # 京东调这个
        # url = 'http://spider.other.k85u.com/api/goods'

        # article
        # url = 'http://127.0.0.1:5000/api/article'
        url = 'http://118.31.39.97/api/article'
        # url = 'http://192.168.2.112/api/article'
        # url = 'http://23.239.0.250/api/article'

        with get(url, params=params) as response:
            res = response.text
            # print(res)
            data = json_2_dict(
                json_str=res,
                default_res={})
            # pprint(data)

            # article
            # print(data.get('data', {}).get('div_body', ''))

        return res

    def __del__(self):
        try:
            del self.loop
        except:
            pass
        collect()

# 单次请求
client = RequestClient()

# print(RequestClient()._request(target_url=client.get_target_url()))

loop = get_event_loop()
loop.run_until_complete(client._fck_run())
