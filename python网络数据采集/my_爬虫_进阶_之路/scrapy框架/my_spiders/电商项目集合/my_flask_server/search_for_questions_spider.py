# coding:utf-8

'''
@author = super_fazai
@File    : search_for_questions_spider.py
@connect : superonesfazai@gmail.com
'''

"""
搜题spider
"""

"""
1. 网课帮m站(http://wangkebang.cn/m/)(只返回一个, pass)
2. 凡尔搜题(https://www.finerit.com)
3. 大学僧搜题(http://souti.lyoo.xyz/)(只返回一个, pass)
4. 上学吧(https://m.shangxueba.com)(充值会员, 且登录存在加减验证码, 一个账号一天只可在3个ip登录, 否则封, pass)(小程序要求看视频才能搜索一次, pass)
5. 作业在线(https://m.yourbin.com/)(大学题经常搜不到, pass)
6. 小猿搜题(拍照搜题, 签名认证)
"""

from settings import (
    IP_POOL_TYPE,
    MY_SPIDER_LOGS_PATH,
)
from my_items import AskQuestionsResultItem

from ftfy import fix_text
from fzutils.spider.selector import parse_field
from fzutils.data.list_utils import list_remove_repeat_dict_plus
from fzutils.spider.async_always import *

class SearchForQuestionsSpider(AsyncCrawler):
    def __init__(self, logger=None):
        """
        搜题爬虫
        """
        AsyncCrawler.__init__(
            self,
            ip_pool_type=IP_POOL_TYPE,
            log_print=True,
            logger=logger,
            log_save_path=MY_SPIDER_LOGS_PATH + '/搜题/_/',
        )
        self.req_num_retries = 3

    async def _fck_run(self):
        k = '社会主义核心价值观'
        await self._search(k=k)

    async def _search(self, k: str) -> list:
        """
        搜索
        :param k:
        :return:
        """
        async def get_tasks_params_list():
            tasks_params_list = []
            for page_num in range(0, 5):
                # 默认只返回前两页, 测试发现无限制
                tasks_params_list.append({
                    'k': k,
                    'page_num': page_num
                })

            return tasks_params_list

        def get_create_task_msg(k) -> str:
            return 'create task[k: {}, page_num: {}]'.format(
                k['k'],
                k['page_num'],
            )

        def get_now_args(k) -> list:
            return [
                k['k'],
                k['page_num'],
            ]

        all_res = await get_or_handle_target_data_by_task_params_list(
            loop=self.loop,
            tasks_params_list=await get_tasks_params_list(),
            func_name_where_get_create_task_msg=get_create_task_msg,
            func_name=self.get_finer_search_res,
            func_name_where_get_now_args=get_now_args,
            func_name_where_add_one_res_2_all_res=default_add_one_res_2_all_res2,
            one_default_res={},
            step=5,
            logger=self.lg,
            concurrent_type=0,
        )
        # pprint(all_res)

        # 根据页码生成最后的结果, 有序
        try:
            all_res.sort(key=lambda item: item.get('page_num', ''))
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)
            return []

        # pprint(all_res)
        res = []
        for item in all_res:
            for i in item.get('res', []):
                res.append(i)

        res = list_remove_repeat_dict_plus(
            target=res,
            repeat_key='question_desc',)
        # pprint(res)
        self.lg.info('本次获取到k: {}, 结果数: {}'.format(
            k,
            len(res),
        ))

        return res

    @catch_exceptions_with_class_logger(default_res={})
    def get_finer_search_res(self, k: str, page_num: int) -> dict:
        """
        凡尔搜题
        :param k: 关键字
        :param page_num: 0开始
        :return:
        """
        headers = get_random_headers(cache_control='')
        headers.update({
            # 'Referer': 'https://www.finerit.com/tiku/search/?q=%E7%A4%BE%E4%BC%9A%E4%B8%BB%E4%B9%89&p=0',
        })
        params = (
            ('q', k),
            ('p', str(page_num)),
        )
        body = Requests.get_url_body(
            url='https://www.finerit.com/tiku/search/',
            headers=headers,
            params=params,
            # cookies=cookies,
            ip_pool_type=self.ip_pool_type,
            proxy_type=PROXY_TYPE_HTTPS,
            num_retries=self.req_num_retries,
            timeout=12,)
        assert body != ''
        # self.lg.info(body)

        question_item_sel = {
            'method': 'css',
            'selector': 'div.resultItem',
        }
        question_desc_div_sel = {
            'method': 'css',
            'selector': 'div.itemHead a',
        }
        answer_div_sel = {
            'method': 'css',
            'selector': 'div.itemBody',
        }
        question_item = parse_field(
            parser=question_item_sel,
            target_obj=body,
            is_first=False,
            logger=self.lg,
        )
        assert question_item != []

        res = []
        for item in question_item:
            # 有序的
            try:
                question_desc_div = parse_field(
                    parser=question_desc_div_sel,
                    target_obj=item,
                    logger=self.lg,
                )
                assert question_desc_div != ''
                answer_div = parse_field(
                    parser=answer_div_sel,
                    target_obj=item,
                    logger=self.lg,
                )
                assert answer_div != ''
                # 清洗
                question_desc = fix_text(wash_sensitive_info(
                    data=question_desc_div,
                    replace_str_list=[],
                    add_sensitive_str_list=[
                        '<div class=\"itemHead\">',
                        '</div>',
                        '<a .*?>',
                        '</a>',
                        '<span .*?>',
                        '</span>',
                    ],
                    is_default_filter=False,
                    is_lower=False,
                ))
                answer = fix_text(wash_sensitive_info(
                    data=answer_div,
                    replace_str_list=[],
                    add_sensitive_str_list=[
                        '<div class=\"itemBody\">',
                        '</div>',
                        '<p .*?>',
                        '</p>',
                        '答案：',
                    ],
                    is_default_filter=False,
                    is_lower=False,
                ))
            except Exception:
                continue

            ask_questions_result_item = AskQuestionsResultItem()
            ask_questions_result_item['question_desc'] = question_desc
            ask_questions_result_item['answer'] = answer
            res.append(dict(ask_questions_result_item))

        self.lg.info('[{}] k: {}, page_num: {}'.format(
            '+' if res != [] else '-',
            k,
            page_num,
        ))

        return {
            'k': k,
            'page_num': page_num,
            'res': res,
        }

    def __del__(self):
        try:
            del self.loop
            del self.lg
        except:
            pass
        collect()

if __name__ == '__main__':
    ask_spider = SearchForQuestionsSpider()
    loop = get_event_loop()
    loop.run_until_complete(ask_spider._fck_run())