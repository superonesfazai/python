# coding:utf-8

'''
@author = super_fazai
@File    : kandian_youth_spider.py
@connect : superonesfazai@gmail.com
'''

"""
中青看点
"""

from gc import collect
from fzutils.ip_pools import tri_ip_pool
from fzutils.data.list_utils import list_remove_repeat_dict_plus
from fzutils.spider.fz_requests import PROXY_TYPE_HTTPS
from fzutils.spider.async_always import *

class KanDianYouth(AsyncCrawler):
    """
    中青看点m站: https://focus.youth.cn/html/articleTop/mobile.html
    """
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            ip_pool_type=tri_ip_pool,)
        self.num_retries = 5
        self.max_page_num = 20

    async def _fck_run(self):
        # cate_id_list = await self._get_m_site_cate_id_list()
        # pprint(cate_id_list)

        # 获取某个cate_id的所有信息
        data = await self._get_all_one_api_info_by_cate_id(
            # type='m',
            _type='pc',
            cate_id=3,)

    async def _get_all_one_api_info_by_cate_id(self, _type='m', cate_id: int=3) -> list:
        """
        获取m站/pc站某个cate_id的所有信息
        :param cate_id:
        :return:
        """
        tasks = []

        if _type == 'm':
            for page_num in range(1, self.max_page_num + 1):
                print('create task[where cate_id: {}, page_num: {}] ...'.format(cate_id, page_num))
                func_args = [
                    cate_id,
                    page_num,
                ]
                tasks.append(self.loop.create_task(unblock_func(
                    func_name=self._get_m_site_one_api_info_by_cate_id,
                    func_args=func_args,
                    default_res=[])))

        elif _type == 'pc':
            for o in range(372, 401):
                print('create task[where cate_id: {}, o: {}] ...'.format(cate_id, o))
                func_args = [
                    cate_id,
                    o,
                ]
                tasks.append(self.loop.create_task(unblock_func(
                    func_name=self._get_pc_site_one_api_info_by_cate_id,
                    func_args=func_args,
                    default_res=[])))

        else:
            raise NotImplemented

        _ = await async_wait_tasks_finished(tasks=tasks)
        all_res = []
        for i in _:
            for j in i:
                all_res.append(j)
        try:
            del _
        except:
            pass

        res = self._parse_someone_cate_id_api_info(
            _type=_type,
            target_list=all_res,)
        pprint(res)
        print('res_len: {}'.format(len(res)))

        return all_res

    def _parse_someone_cate_id_api_info(self, target_list: list, _type='m',) -> list:
        """
        解析m站, pc站接口的信息
        :param target_list:
        :return:
        """
        # pprint(target_list)
        res = []
        for item in target_list:
            try:
                title = item.get('title', '')
                assert title != '', 'title != ""'
                share_num = item.get('share_num', '0')
                assert share_num != '0', "share_num != '0'"
                id = item.get('id', )
                assert id is not None, 'id is not None'

                if _type == 'm':
                    read_num = item.get('read_num', '0')
                elif _type == 'pc':
                    read_num = item.get('read_sum', '0')
                else:
                    raise NotImplemented
                assert read_num != '0', "read_num != '0'"

            except (AssertionError, Exception) as e:
                # print('遇到错误:', e)
                continue

            res.append({
                'id': id,
                'title': title,
                'read_num': read_num,
                'share_num': share_num,
                'url': 'https://focus.youth.cn/mobile/detail/id/{}#'.format(id)
            })

        res = list_remove_repeat_dict_plus(
            target=res,
            repeat_key='title', )
        # 按阅读数正序排列
        # res = sorted(res, key=lambda item: int(item.get('read_num', '0')), reverse=True)

        return res

    def _get_pc_site_one_api_info_by_cate_id(self, cate_id: int=3, o: int='372') -> list:
        """
        获取pc站某个cate_id的单个接口信息
        :param cate_id:
        :return:
        """
        headers = self._get_random_pc_headers()
        headers.update({
            # 'Referer': 'http://kandian.youth.cn/index/lists?type=3',
        })
        _t = get_now_13_bit_timestamp()
        # print(_t)
        # _ 从372开始, 后面累加1
        _ = _t[:10] + str(o)
        params = (
            # ('jsonpcallback', 'jQuery20304605245637579367_1559269153366'),
            ('recgid', '15592081818956551'),
            ('type', str(cate_id)),
            ('_', _),
        )
        url = 'http://kandian.youth.cn/index/getContent'
        body = Requests.get_url_body(
            url=url,
            headers=headers,
            params=params,
            ip_pool_type=self.ip_pool_type,
            proxy_type=PROXY_TYPE_HTTPS,
            num_retries=self.num_retries,)
        # print(body)

        data = []
        try:
            data = json_2_dict(
                json_str=re.compile('\((.*)\)').findall(body)[0],
                default_res={}, ).get('data', [])
            # pprint(data)
        except IndexError as e:
            print(e)

        print('[{}] cate_id: {}, _: {}'.format(
            '+' if data != [] else '-',
            cate_id,
            _,
        ))

        return data

    def _get_m_site_one_api_info_by_cate_id(self, cate_id: int=3, page_num: int=1) -> list:
        """
        获取m站某个cate_id的单个接口信息
        :param cate_id: '3' 是健康
        :param page_num:
        :return:
        """
        data = dumps({
            'type': '1',
            'page': str(page_num),
            'catid': str(cate_id),
        })
        url = 'https://focus.youth.cn/WebApi/Article/top'
        body = Requests.get_url_body(
            method='post',
            url=url,
            headers=self._get_random_phone_headers(),
            data=data,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.num_retries,)
        # print(body)
        data = json_2_dict(
            json_str=body,
            default_res={},).get('data', {}).get('items', [])
        # pprint(data)
        print('[{}] cate_id: {}, page_num: {}'.format(
            '+' if data != [] else '-',
            cate_id,
            page_num,
        ))

        return data

    async def _get_m_site_cate_id_list(self) -> list:
        """
        获取m站 cate id list(比如健康的id是3)
        :return:
        """
        url = 'https://focus.youth.cn/WebApi/Article/Category'
        data = dumps({
            'type': '1',
            'page': '1',
            'catid': '0',
        })
        body = await unblock_request(
            method='post',
            url=url,
            headers=self._get_random_phone_headers(),
            data=data,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.num_retries,)
        # print(body)
        data = json_2_dict(
            json_str=body,
            default_res={},).get('data', {}).get('items', [])

        return data

    @staticmethod
    def _get_random_phone_headers() -> dict:
        return {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'https://focus.youth.cn',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': get_random_phone_ua(),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

    @staticmethod
    def _get_random_pc_headers() -> dict:
        return {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'User-Agent': get_random_pc_ua(),
            'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }

    def __del__(self):
        try:
            del self.loop
        except:
            pass
        collect()

if __name__ == '__main__':
    loop = get_event_loop()
    _ = KanDianYouth()
    res = loop.run_until_complete(_._fck_run())