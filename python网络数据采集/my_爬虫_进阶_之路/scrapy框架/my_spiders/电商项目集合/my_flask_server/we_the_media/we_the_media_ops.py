# coding:utf-8

'''
@author = super_fazai
@File    : we_the_media_ops.py
@connect : superonesfazai@gmail.com
'''

"""
自媒体ops
"""

import sys
sys.path.append('..')

from settings import IP_POOL_TYPE
from article_spider import ArticleParser

from gc import collect
from fzutils.spider.async_always import *

class WeTheMediaOps(AsyncCrawler):
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            ip_pool_type=IP_POOL_TYPE,)
        self.ht_we_the_media_x_auth_token_file_path = '/Users/afa/myFiles/pwd/ht_we_the_media_x_auth_token.txt'

    async def _publish_article(self, publish_article_type: str, title='', content=''):
        """
        发布article
        :return:
        """
        if publish_article_type == 'ht':
            await self._ht_publish_article(
                title=title,
                content=content,)

        else:
            raise NotImplemented

    async def _ht_publish_article(self, title='', content=''):
        """
        ht
        :param article_url:
        :param title:
        :param content:
        :return:
        """
        self.ht_x_auth_token = await self._get_ht_we_the_media_x_auth_token()
        print('ht:x_auth_token: {}'.format(self.ht_x_auth_token))
        assert title !='', 'title != ""'
        assert content != '', 'content != ""'

        # 惠头条自动发文
        headers = await self._get_random_pc_headers()
        headers.update({
            'Origin': 'null',
            'Referer': 'http://mp.cashtoutiao.com/content/add',
            'X-Auth-Token': self.ht_x_auth_token,
            'Content-Type': 'application/json',
        })
        # eg: 官方标准html
        # article_content = '<p>5月20日，港交所发布公告称，自5月21日起，上海证券交易所上市的康美药业将从中华通证券名单中移除并加入到中华通特别证券名单，即只可经沪股通卖出。<br></p><p><img src="https://res.youth.cn/article_201905_21_21i_5ce2e066409f9.jpg"><br></p><p>这是5月份港交所唯一调动的沪股通股票名单。明天，康美药业也将被“ST”。</p><p><strong>康美药业危机重重</strong></p><p>有香港市场人士称，港交所公告意味着，自5月21日起，北向资金只能卖出康美药业，不能买入。同时，康美药业因被实施其他风险警示，上交所将于5月21日将其调出融资融券标的证券名单。</p><p>5月21日将是康美药业戴上“ST”帽子的第一天，公司28万户的股东20日晚上又将彻夜难眠。明天公司股票开盘后大概率跌停，而这仅仅是噩梦的开始，不知道要多少个跌停才能止血。</p><p><img src="https://res.youth.cn/article_201905_21_21y_5ce2e067a5ee4.jpg"><br></p><p>噩梦其实并不突然。证监会5月17日通报了康美药业调查进展。公司披露的2016-2018年财务报告存在重大虚假，涉嫌违反《证券法》第63条等相关规定。一是使用虚假银行单据虚增存款，二是通过伪造业务凭证进行收入造假，三是部分资金转入关联方账户买卖本公司股票。<br></p><p><strong>沪深股通什么情形只出不进？</strong></p><p>对于康美药业在沪股通中只能卖出，港交所方面人士表示，这只是一个常规操作，因为康美药业被ST了。</p><p>上述人士提供的一份《沪深港股票市场交易互联互通机制常问问题》显示，沪股通股票在发生下列3种情形时，将被暂停买入（但允许卖出）：</p><p><img src="https://res.youth.cn/article_201905_21_21v_5ce2e06d61729.jpg"><br></p><p>康美药业属于上述3种情形的第二种——被实施风险警示。</p><p>事实上，由于这种原因被暂停买入的沪股通标的也不止康美药业一只。港交所5月20日公布的最新《沪股通股票名单更改》显示，2019年4月以来已有4家公司被移至沪股通特别证券、中华通特别证券名单，即只可卖出不能买入。</p><p><img src="https://res.youth.cn/article_201905_21_21v_5ce2e06ee2c3d.jpg"><br></p><p>深股通被暂停买入（但允许卖出）额外增加了一种情形：<br></p><p><img src="https://res.youth.cn/article_201905_21_21g_5ce2e06f8264e.jpg"><br></p><p>深股通增加的这一种情形是：如果该股的市值按任何其后进行的定期审核低于人民币60亿元，也将会被暂停买入。</p><p><strong>什么时候可以恢复买入？</strong></p><p>中证君注意到，被“ST”之后，沪股通、深股通标的被暂停买入，但也不是不可以恢复买入。</p><p>在前述的《沪股通股票名单更改》中，2019年4月2日，石化油服就由“沪股通特别证券/中华通特别证券名单(只可卖出)”中加入到了沪股通名单，其调整原因正是“该股票已被调出风险警示板”，即取消“ST”。</p><p><img src="https://res.youth.cn/article_201905_21_21z_5ce2e06fd8f67.jpg"><br></p><p>而这一调整，正是基于2019年4月2日，石化油服发布关于公司A股股票撤销退市风险警示的公告：<br></p><p><img src="https://res.youth.cn/article_201905_21_21d_5ce2e0702332b.jpg"><br></p><p>康美药业时间线</p><p>5月20日：上交所将康美药业调出融资融券标的；港交所发布公告，康美药业只可经沪股通卖出不能买入；</p><p>5月17日：证监会通报康美药业案进展，其存在收入造假，部分资金转出炒股</p><p>康美药业公告于2019年5月21日起实施其他风险警示；</p><p>5月9日：作为康美药业的审计机构，广东正中珠江会计事务所被证监会立案调查；</p><p>4月30日：康美药业发布了一份《关于前期会计差错更正》的公告，对2017年财报做出重大调整；</p><p>另外，上交所分别于5月12日、5月5日和4月30日，对康美药业进行了3次问询。</p>'
        data = dumps({
            'campaignId': None,
            'channel': 2,               # 健康
            'content': content,
            'cover': '',
            'coverType': 5,
            'fixedReleaseTime': '',
            'tagIds': '财经',
            'title': title,
            'weMediaState': 1,
        })
        url = 'http://content.wemedia.cashtoutiao.com/wemedia/article/addRelease'
        body = await unblock_request(
            method='post',
            use_proxy=False,
            url=url,
            headers=headers,
            data=data,
            ip_pool_type=self.ip_pool_type,)
        print(body)

        return

    async def _get_ht_we_the_media_x_auth_token(self):
        """
        获取ht x_auth_token
        :return:
        """
        with open(self.ht_we_the_media_x_auth_token_file_path, 'r') as f:
            x_auth_token = f.read().replace('\n', '')

        assert x_auth_token != '', 'x_auth_token != ""'

        return x_auth_token

    @staticmethod
    async def _get_random_pc_headers():
        return {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_pc_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

    def __del__(self):
        try:
            del self.loop
        except:
            pass
        collect()

if __name__ == '__main__':
    loop = get_event_loop()
    we_the_media_ops_obj = WeTheMediaOps()

    article_url = 'https://focus.youth.cn/mobile/detail/id/15562764#'
    article_parser = ArticleParser()
    article_res = loop.run_until_complete(article_parser._parse_article(
        article_url=article_url))

    # 待发布内容
    title = article_res['title']
    content = article_res['div_body']
    # 发布文章
    res = loop.run_until_complete(we_the_media_ops_obj._publish_article(
        publish_article_type='ht',
        title=title,
        content=content,))
