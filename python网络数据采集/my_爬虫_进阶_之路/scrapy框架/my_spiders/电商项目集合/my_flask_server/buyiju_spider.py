# coding:utf-8

'''
@author = super_fazai
@File    : buyiju_spider.py
@connect : superonesfazai@gmail.com
'''

"""
卜易居 spider(https://m.buyiju.com)
"""

from gc import collect
from settings import (
    MY_SPIDER_LOGS_PATH,
    IP_POOL_TYPE,)
from article_spider import (
    modify_body_p_typesetting,
    modify_body_img_centering,)
from fzutils.spider.selector import async_parse_field
from fzutils.exceptions import catch_exceptions_with_class_logger
from fzutils.spider.async_always import *

class BuYiJuSpider(AsyncCrawler):
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            ip_pool_type=IP_POOL_TYPE,
            log_print=True,
            log_save_path=MY_SPIDER_LOGS_PATH + '/buyiju/_/',)
        self.num_retries = 6
        self.parser_obj_dict = self.get_parser_obj_dict()

    async def _fck_run(self):
        """
        main
        :return:
        """
        # ** 姓名打分
        # res = await self.name_scoring(surname='吕', name='布')

        # ** 测字算命
        # res = await self.word_and_fortune_telling(two_words='你好')

        # ** 生日算命
        # res = await self.birthday_fortune_telling(month=12, day=25)

        # ** 手机号码测吉凶
        # res = await self.phone_number_for_good_or_bad_luck(phone_num=18796571279)

        # ** 车牌号码测吉凶
        # res = await self.license_plate_num_for_good_or_bad(
        #     province='京',
        #     city_num='A',
        #     num='66666')

        # ** 姓名缘分配对
        # res = await self.distribution_pairs_of_names(name1='吕布', name2='貂蝉')

        # ** 星座配对
        res = await self.constellation_pairing(constellation_name1='处女座', constellation_name2='摩羯座')

        # ** 抽签算命
        # 观音灵签
        # res = await self.fortune_telling_by_lot(lot_type='gy')
        # 佛祖灵签
        # res = await self.fortune_telling_by_lot(lot_type='fz')
        # 月老灵签
        # res = await self.fortune_telling_by_lot(lot_type='yl')
        # 关帝灵签
        # res = await self.fortune_telling_by_lot(lot_type='gd')
        # 黄大仙灵签
        # res = await self.fortune_telling_by_lot(lot_type='hdx')
        # 吕祖灵签
        # res = await self.fortune_telling_by_lot(lot_type='lz')
        # 天后妈祖灵签
        # res = await self.fortune_telling_by_lot(lot_type='mz')
        # 财神灵签
        # res = await self.fortune_telling_by_lot(lot_type='cs')
        # 地藏王灵签
        # res = await self.fortune_telling_by_lot(lot_type='dzw')
        # 易经64卦灵签
        # res = await self.fortune_telling_by_lot(lot_type='yj')
        # 太上老君灵签
        # res = await self.fortune_telling_by_lot(lot_type='tslj')

        pprint(res)

    async def constellation_pairing(self, constellation_name1: str, constellation_name2: str) -> dict:
        """
        星座配对
        :param constellation_name1:
        :param constellation_name2:
        :return:
        """
        headers = await self.get_random_phone_headers()
        headers.update({
            'Origin': 'https://m.buyiju.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://m.buyiju.com/peidui/xzpd.php',
        })
        data = {
            'xz1': constellation_name1,
            'xz2': constellation_name2,
            'submit': '开始测试',
        }
        body = await unblock_request(
            method='post',
            url='https://m.buyiju.com/peidui/xzpd.php',
            headers=headers,
            data=data,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.num_retries,
            logger=self.lg, )
        # self.lg.info(body)

        try:
            assert body != ''
            content = await async_parse_field(
                parser=self.parser_obj_dict['byj']['constellation_pairing']['content'],
                target_obj=body,
                logger=self.lg, )
            assert content != '', 'content != ""'
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)
            return {}

        content = await self._wash_constellation_pairing_content(content=content)
        print(content)

        return {
            'res': content,
        }

    async def distribution_pairs_of_names(self, name1: str, name2: str) -> dict:
        """
        姓名缘分配对
        :param name1:
        :param name2:
        :return:
        """
        headers = await self.get_random_phone_headers()
        headers.update({
            'Origin': 'https://m.buyiju.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://m.buyiju.com/peidui/xmyf.php',
        })
        data = {
            'cname1': name1,
            'cname2': name2,
            'submit': '开始测试',
        }
        body = await unblock_request(
            method='post',
            url='https://m.buyiju.com/peidui/xmyf.php',
            headers=headers,
            data=data,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.num_retries,
            logger=self.lg, )
        # self.lg.info(body)

        try:
            assert body != ''
            content = await async_parse_field(
                parser=self.parser_obj_dict['byj']['distribution_pairs_of_names']['content'],
                target_obj=body,
                logger=self.lg, )
            assert content != '', 'content != ""'
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)
            return {}

        content = await self._wash_distribution_pairs_of_names_content(content=content)
        print(content)

        return {
            'res': content,
        }

    async def license_plate_num_for_good_or_bad(self, province: str, city_num: str, num :str):
        """
        车牌测吉凶
        :param province:
        :param city_num:
        :param num:
        :return:
        """
        headers = await self.get_random_phone_headers()
        headers.update({
            'Origin': 'https://m.buyiju.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://m.buyiju.com/cm/chepai/',
        })
        data = {
            'sheng': province,
            'shi': city_num,
            'czsm': num,
            'action': 'test'
        }
        body = await unblock_request(
            method='post',
            url='https://m.buyiju.com/cm/chepai/',
            headers=headers,
            data=data,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.num_retries,
            logger=self.lg, )
        # self.lg.info(body)

        try:
            assert body != ''
            content = await async_parse_field(
                parser=self.parser_obj_dict['byj']['license_plate_num_for_good_or_bad']['content'],
                target_obj=body,
                logger=self.lg, )
            assert content != '', 'content != ""'
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)
            return {}

        content = await self._wash_license_plate_num_for_good_or_bad_content(content=content)
        print(content)

        return {
            'res': content,
        }

    async def phone_number_for_good_or_bad_luck(self, phone_num: int):
        """
        手机号码测吉凶
        :param phone_num:
        :return:
        """
        headers = await self.get_random_phone_headers()
        headers.update({
            'Origin': 'https://m.buyiju.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://m.buyiju.com/shouji/',
        })
        data = {
            'sjhao': str(phone_num),
            'action': 'test'
        }
        body = await unblock_request(
            method='post',
            url='https://m.buyiju.com/shouji/',
            headers=headers,
            data=data,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.num_retries,
            logger=self.lg, )
        # self.lg.info(body)

        try:
            assert body != ''
            content = await async_parse_field(
                parser=self.parser_obj_dict['byj']['phone_number_for_good_or_bad_luck']['content'],
                target_obj=body,
                logger=self.lg, )
            assert content != '', 'content != ""'
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)
            return {}

        content = await self._wash_phone_number_for_good_or_bad_luck_content(content=content)
        print(content)

        return {
            'res': content,
        }

    async def birthday_fortune_telling(self, month: int, day: int) -> dict:
        """
        生日算命
        :return:
        """
        headers = await self.get_random_phone_headers()
        headers.update({
            'Referer': 'https://m.buyiju.com/birth/shu/',
        })
        body = await unblock_request(
            url='https://m.buyiju.com/birth/shu/{month}-{day}.html'.format(month=month, day=day),
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.num_retries,
            logger=self.lg, )
        # self.lg.info(body)

        try:
            assert body != ''
            content = await async_parse_field(
                parser=self.parser_obj_dict['byj']['birthday_fortune_telling']['content'],
                target_obj=body,
                logger=self.lg, )
            assert content != '', 'content != ""'
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)
            return {}

        content = await self._wash_birthday_fortune_telling_content(content=content)
        print(content)

        return {
            'res': content,
        }

    async def get_lot_some_params(self, lot_type: str) -> tuple:
        """
        得到抽签动态参数
        :param lot_type:
        :return:
        """
        base_referer = 'https://m.buyiju.com/{}/'
        base_url = 'https://m.buyiju.com/{}/'
        base_referer2 = 'https://m.buyiju.com/chouqian/{}/'
        base_url2 = 'https://m.buyiju.com/chouqian/{}/'
        if lot_type == 'gy':
            # 观音灵签, 共100签
            referer = base_referer.format('guanyin')
            qid = str(get_random_int_number(1, 100))
            url = base_url.format('guanyin')

        elif lot_type == 'fz':
            # 佛祖灵签, 共51签
            referer = base_referer2.format('fozu')
            qid = str(get_random_int_number(1, 51))
            url = base_url2.format('fozu')

        elif lot_type == 'yl':
            # 月老灵签, 共101签
            referer = base_referer.format('yuelao')
            qid = str(get_random_int_number(1, 101))
            url = base_url.format('yuelao')

        elif lot_type == 'gd':
            # 关帝灵签, 共100签
            referer = base_referer.format('guandi')
            qid = str(get_random_int_number(1, 100))
            url = base_url.format('guandi')

        elif lot_type == 'hdx':
            # 黄大仙灵签, 共100签
            referer = base_referer.format('hdx')
            qid = str(get_random_int_number(1, 100))
            url = base_url.format('hdx')

        elif lot_type == 'lz':
            # 吕祖灵签, 共100签
            referer = base_referer.format('lvzu')
            qid = str(get_random_int_number(1, 100))
            url = base_url.format('lvzu')

        elif lot_type == 'mz':
            # 天后妈祖灵签, 共101签
            referer = base_referer2.format('mazu')
            qid = str(get_random_int_number(1, 101))
            url = base_url2.format('mazu')

        elif lot_type == 'cs':
            # 财神灵签, 共61签
            referer = base_referer2.format('caishen')
            qid = str(get_random_int_number(1, 61))
            url = base_url2.format('caishen')

        elif lot_type == 'dzw':
            # 地藏王灵签, 共60签
            referer = base_referer2.format('dizangwang')
            qid = str(get_random_int_number(1, 60))
            url = base_url2.format('dizangwang')

        elif lot_type == 'yj':
            # 易经64卦灵签, 共64签
            referer = base_referer2.format('yijing')
            qid = str(get_random_int_number(1, 64))
            url = base_url2.format('yijing')

        elif lot_type == 'tslj':
            # 太上老君灵签, 共28签
            referer = base_referer2.format('taishanglaojun')
            qid = str(get_random_int_number(1, 28))
            url = base_url2.format('taishanglaojun')

        else:
            raise NotImplemented('lot_type value异常!')

        return referer, qid, url

    async def fortune_telling_by_lot(self, lot_type: str) -> dict:
        """
        根据抽签类别进行抽签
        :param lot_type:
        :return:
        """
        referer, qid, url = await self.get_lot_some_params(lot_type=lot_type)
        headers = await self.get_random_phone_headers()
        headers.update({
            'Origin': 'https://m.buyiju.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': referer,
        })
        data = {
            'qian': 'ok',
            'qid': qid,
        }
        body = await unblock_request(
            method='post',
            url=url,
            headers=headers,
            data=data,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.num_retries,
            logger=self.lg, )
        # self.lg.info(body)
        try:
            assert body != ''
            content = await async_parse_field(
                parser=self.parser_obj_dict['byj']['fortune_telling_by_lot']['content'],
                target_obj=body,
                logger=self.lg, )
            assert content != '', 'content != ""'
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)
            return {}

        content = await self._wash_fortune_telling_by_lot_content(content=content)
        print(content)

        return {
            'res': content,
        }

    async def word_and_fortune_telling(self, two_words: str) -> dict:
        """
        测字算命
        :param two_words: 2字
        :return:
        """
        headers = await self.get_random_phone_headers()
        headers.update({
            'Origin': 'https://m.buyiju.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://m.buyiju.com/cm/cezi/',

        })
        data = {
            'czsm': two_words,
            'action': 'test',
        }
        body = await unblock_request(
            url='https://m.buyiju.com/cm/cezi/',
            headers=headers,
            data=data,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.num_retries,
            logger=self.lg,)
        # self.lg.info(body)

        try:
            assert body != ''
            content = await async_parse_field(
                parser=self.parser_obj_dict['byj']['word_and_fortune_telling']['content'],
                target_obj=body,
                logger=self.lg,)
            assert content != '', 'content != ""'
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)
            return {}

        content = await self._wash_word_and_fortune_telling_content(content=content)
        print(content)

        return {
            'res': content,
        }

    async def name_scoring(self, surname: str, name: str) -> dict:
        """
        姓名打分
        :param surname: 姓
        :param name: 名字
        :return:
        """
        headers = await self.get_random_phone_headers()
        headers.update({
            'Origin': 'https://m.buyiju.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Referer': 'https://m.buyiju.com/cm/',
        })
        data = {
            'xs': surname,
            'mz': name,
            'action': 'test'
        }
        body = await unblock_request(
            method='post',
            url='https://m.buyiju.com/cm/',
            headers=headers,
            data=data,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.num_retries,
            logger=self.lg,)
        # self.lg.info(body)

        try:
            assert body != ''
            content = await async_parse_field(
                parser=self.parser_obj_dict['byj']['name_scoring']['content'],
                target_obj=body,
                logger=self.lg,)
            assert content != '', 'content != ""'
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)
            return {}

        content = await self._wash_name_scoring_content(content=content)
        print(content)

        return {
            'res': content,
        }

    @staticmethod
    async def _wash_constellation_pairing_content(content) -> str:
        """
        清洗星座配对
        :param content:
        :return:
        """
        content = wash_sensitive_info(
            data=content,
            replace_str_list=[
                ('卜易居士|卜易居', '优秀网'),
                # 避免过度清洗
                ('<div class=\"yunshi\">.*</div>', '</div>'),
            ],
            add_sensitive_str_list=None,
            is_default_filter=False, )

        content = modify_body_p_typesetting(content=content)

        return content

    @staticmethod
    async def _wash_distribution_pairs_of_names_content(content) -> str:
        """
        姓名缘分测试
        :param content:
        :return:
        """
        content = wash_sensitive_info(
            data=content,
            replace_str_list=[
                ('卜易居士|卜易居', '优秀网'),
                # 避免过度清洗
                ('<div class=\"yunshi\">.*</div>', '</div>'),
            ],
            add_sensitive_str_list=None,
            is_default_filter=False, )

        content = modify_body_p_typesetting(content=content)

        return content

    @staticmethod
    async def _wash_license_plate_num_for_good_or_bad_content(content) -> str:
        """
        清洗车牌测吉凶
        :param content:
        :return:
        """
        content = wash_sensitive_info(
            data=content,
            replace_str_list=[
                ('卜易居士|卜易居', '优秀网'),
                ('<div class=\"inform\">.*</div>', '</div>')
            ],
            add_sensitive_str_list=[
                '<p><strong>优秀网车牌祥批</strong></p>',
                '<p>以上结果为通用数理分析，如需全面掌握车牌号 <span class=\"red\">.*?</span> 带给你的机缘，可请优秀网结合 <strong>生辰八字</strong>进行测算，让你全面掌握车牌号带给你的机缘！可以为选车牌号提供参考。</p>'
            ],
            is_default_filter=False,)

        content = modify_body_p_typesetting(content=content)
        if content != '':
            # 牌照底纹蓝色
            content = '<style>.cp{width:180px;margin:auto;}  .cp ul{color:white;font-weight:bold;letter-spacing:2px;background-color:blue;padding:2px;}  .cp ul li{border:2px solid #fff;text-transform:uppercase;font:normal normal 26px/30px Arial, Helvetica, sans-serif;list-style-type: none;padding-top:2px;}  .zmdx{text-transform:uppercase;}</style>' + \
                content
        else:
            pass

        return content

    @staticmethod
    async def _wash_phone_number_for_good_or_bad_luck_content(content) -> str:
        """
        清洗手机号码测吉凶
        :param content:
        :return:
        """
        content = wash_sensitive_info(
            data=content,
            replace_str_list=[
                ('卜易居士|卜易居', '优秀网'),
                ('<div class=\"inform\">.*</div>', '</div>')
            ],
            add_sensitive_str_list=[
                '<p><strong>优秀网手机号吉凶祥批</strong></p>',
                '<p>以上结果为通用数理分析，如需全面掌握手机号码 <span class=\"red\">\d+</span> 带给您的机缘，可请优秀网结合您的 <strong>生辰八字</strong> 进行测算，可以为选手机号提供参考。</p>'
            ],
            is_default_filter=False, )

        content = modify_body_p_typesetting(content=content)

        return content

    @staticmethod
    async def _wash_birthday_fortune_telling_content(content) -> str:
        """
        清洗生日算命
        :param content:
        :return:
        """
        content = wash_sensitive_info(
            data=content,
            replace_str_list=[
                ('卜易居士|卜易居', '优秀网'),
                # 避免过度清洗
                ('<div class=\"yunshi\">.*</div>', '</div>')
            ],
            add_sensitive_str_list=[
                '<a href=\"/sm/cx.php\">点此进行精确的星座查询</a>',
                '如果您的生日刚好处于起止点日期前后，您可能需要进行精确的星座查询，。',
            ],
            is_default_filter=False,)

        return content

    @staticmethod
    async def _wash_fortune_telling_by_lot_content(content) -> str:
        """
        清洗抽签算命
        :param content:
        :return:
        """
        content = wash_sensitive_info(
            data=content,
            replace_str_list=[
                ('卜易居士|卜易居', '优秀网'),
                ('<div class=\"inform\">.*</div>', '</div>')
            ],
            add_sensitive_str_list=[
                '<p><strong>大师解签</strong></p>',
                '<p>以上解签为通用解释，如需知晓具体事宜，可请大师结合您的生辰八字解签：</p>',
            ],
            is_default_filter=False, )

        return content

    @staticmethod
    async def _wash_word_and_fortune_telling_content(content) -> str:
        """
        清洗测字算命
        :param content:
        :return:
        """
        content = wash_sensitive_info(
            data=content,
            replace_str_list=[
                # 避免过度清洗
                ('<div class=\"yunshi\">.*</div>', '</div>')
            ],
        )

        content = modify_body_p_typesetting(content=content)

        return content

    @staticmethod
    async def _wash_name_scoring_content(content) -> str:
        """
        清洗姓名打分
        :param content:
        :return:
        """
        content = wash_sensitive_info(
            data=content,
            replace_str_list=[
                ('卜易居士|卜易居', '优秀网'),
                ('<div class=\"inform\">.*</div>', '</div>'),
                ('<table>', '<table border=\"1\" width=\"100%\" bgcolor=\"white\" cellpadding=\"2\">')
            ],
            add_sensitive_str_list=None,
            is_default_filter=False,)

        if content != '':
            content = '<link href="//i.buyiju.com/css/mobile.css?v0616" rel="stylesheet" media="screen" type="text/css" />' \
                      + content
        else:
            pass

        return content

    @catch_exceptions_with_class_logger(default_res='aa')
    def test(self) -> str:
        assert '' != ''

        return ''

    @staticmethod
    def get_parser_obj_dict() -> dict:
        return {
            'byj': {
                'name_scoring': {
                    'content': {
                        'method': 'css',
                        'selector': 'div.content',
                    }
                },
                'word_and_fortune_telling': {
                    'content': {
                        'method': 'css',
                        'selector': 'div.content',
                    }
                },
                'fortune_telling_by_lot': {
                    'content': {
                        'method': 'css',
                        'selector': 'div.content',
                    }
                },
                'birthday_fortune_telling': {
                    'content': {
                        'method': 'css',
                        'selector': 'div.content',
                    }
                },
                'phone_number_for_good_or_bad_luck': {
                    'content': {
                        'method': 'css',
                        'selector': 'div.content',
                    }
                },
                'license_plate_num_for_good_or_bad': {
                    'content': {
                        'method': 'css',
                        'selector': 'div.content',
                    }
                },
                'distribution_pairs_of_names': {
                    'content': {
                        'method': 'css',
                        'selector': 'div.content',
                    }
                },
                'constellation_pairing': {
                    'content': {
                        'method': 'css',
                        'selector': 'div.content',
                    }
                },
            },
        }

    @staticmethod
    async def get_random_phone_headers() -> dict:
        return {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_phone_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

    def __del__(self):
        try:
            del self.loop
        except:
            pass
        collect()

if __name__ == '__main__':
    byj_spider = BuYiJuSpider()
    loop = get_event_loop()
    loop.run_until_complete(byj_spider._fck_run())