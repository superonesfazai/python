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
7. 大白搜题(http://chati.naxuefen.com/#/login)(只返回一个, pass)(结果同wkb)
8. 搜题狗(http://www.etkz.cn/search.php?mod=forum&mobile=2)(多个答案, 但是专业性较强的搜不到(eg: c语言))
9. 安艾希搜题网(https://www.dlsqb.com/question/search.html?word=社会主义)(可以设计为: 先搜索返回问题列表, 再让其点击查看答案, 再去采集对应页的答案)(但是网站极其不稳定, pass)
10. 水桶搜题(https://chati.xuanxiu365.com/index.php)(只返回一个, pass)(结果同wkb)
11. 小马搜题(http://so.xiaomasou.com/static/index.html)(返回2个,)
12. 熊猫题库(http://www.lmcv.cn/)(多个)
13. 菜鸟搜题(http://www.51zhaoti.cn/)(先出问题再根据问题id出答案)
14. soso题库(http://www.sosoti.cn/)(登录才可查看答案)
15. 师兄帮帮(https://sxbb.me/)(搜索大学笔记)
"""

from settings import (
    IP_POOL_TYPE,
    MY_SPIDER_LOGS_PATH,
    PHANTOMJS_DRIVER_PATH,
)
from my_items import AskQuestionsResultItem

from ftfy import fix_text
from fzutils.spider.selector import parse_field
from fzutils.data.list_utils import list_remove_repeat_dict_plus
from fzutils.spider.fz_driver import BaseDriver, PHONE
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
        # 单次请求超时
        self.req_timeout = 8.5

    async def _fck_run(self):
        k = '社会主义核心价值观'
        # k = 'c语言'
        # k = '马克思主义的生命力'
        # k = '科学发展观的根本方法'
        await self._search(k=k)

    async def _search(self, k: str) -> list:
        """
        搜索
        :param k:
        :return:
        """
        # res = await self._search_by_finer(k=k)
        res = await self._search_by_wkb_and_lyoo(k=k)

        res = list_remove_repeat_dict_plus(
            target=res,
            repeat_key='question_desc',)
        pprint(res)
        self.lg.info('本次获取到k: {}, 结果数: {}'.format(
            k,
            len(res),
        ))

        return res

    async def _search_by_wkb_and_lyoo(self, k: str):
        """
        基于某些返回一个答案的搜索, eg: 网课帮, 大学僧搜题
        :param k:
        :return:
        """
        # 用于结果的默认排序值, 使返回结果有序
        default_sort_value = None
        wait_2_exec_list = [
            ['wkb', (k, 0)],
            ['xms', (k, 1)],

            # 暂时无数据
            # ['stg', (k, 1, 2)],
            # ['stg', (k, 2, 3)],
            # 耗时过久, pass
            # ['stg2', (k, 4)],

            # 偶尔会出现非相关数据, 此处不好过滤
            ['xmtk', (k, 5)],

            ['lyoo', (k, 6)],
        ]

        tasks = []
        for item in wait_2_exec_list:
            exec_func_name = item[0]
            exec_params = item[1]
            self.lg.info('create task[where exec_func_name: {}, k: {}] ...'.format(
                exec_func_name,
                k,
            ))
            if exec_func_name == 'wkb':
                func_name = self.get_wkb_search_res

            elif exec_func_name == 'lyoo':
                func_name = self.get_lyoo_search_res

            elif exec_func_name == 'xms':
                func_name = self.get_xms_search_res

            elif exec_func_name == 'stg':
                func_name = self.get_stg_search_res

            elif exec_func_name == 'stg2':
                func_name = self.get_stg_search_res2

            elif exec_func_name == 'xmtk':
                func_name = self.get_xmtk_search_res

            else:
                continue

            tasks.append(self.loop.create_task(unblock_func(
                func_name=func_name,
                func_args=exec_params,
                logger=self.lg,
                default_res={},
            )))

        one_res = await async_wait_tasks_finished(tasks=tasks)
        # pprint(one_res)

        all_res = []
        for i in one_res:
            if i != {}:
                all_res.append(i)

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

        try:
            del tasks
            del one_res
        except:
            pass
        collect()

        return res

    @catch_exceptions_with_class_logger(default_res={})
    def get_xmtk_search_res(self, k: str, default_sort_value: int=None) -> dict:
        """
        熊猫题库
        :param k:
        :param page_num:
        :param default_sort_value:
        :return:
        """
        # 只能获取第一页数据
        headers = get_random_headers(
            connection_status_keep_alive=False,
            cache_control='',
        )
        headers.update({
            'Referer': 'http://www.lmcv.cn/',
        })
        params = (
            ('s', k),
        )
        body = Requests.get_url_body(
            url='http://www.lmcv.cn/',
            headers=headers,
            params=params,
            verify=False,
            ip_pool_type=self.ip_pool_type,
            # proxy_type=PROXY_TYPE_HTTPS,          # 不支持https, 因此偶尔高并发会无数据
            num_retries=self.req_num_retries,
            timeout=self.req_timeout,)
        assert body != ''
        # self.lg.info(body)

        question_item_sel = {
            'method': 'css',
            'selector': 'span.art-main',
        }
        question_desc_div_sel = {
            'method': 're',
            'selector': '问题：(.*?)答案：',
        }
        answer_div_sel = {
            'method': 're',
            'selector': '答案：(.*?)更多相关问题',
        }
        question_item = parse_field(
            parser=question_item_sel,
            target_obj=body,
            is_first=False,
            logger=self.lg,
        )
        assert question_item != []
        # pprint(question_item)

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
                        '<strong>',
                        '</strong>',
                        '<font .*?>',
                        '</font>',
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
                        '<strong>',
                        '</strong>',
                        '<font .*?>',
                        '</font>',
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

        self.lg.info('[{}] xmtk, k: {}'.format(
            '+' if res != [] else '-',
            k,
        ))

        return {
            'k': k,
            'page_num': default_sort_value,
            'res': res,
        }

    @catch_exceptions_with_class_logger(default_res={})
    def get_stg_search_res2(self, k: str, default_sort_value: int=None) -> dict:
        """
        搜题狗2(driver 版)
        :param k:
        :return:
        """
        # 只获取第一页数据
        k = '社会主义核心'
        driver = BaseDriver(
            executable_path=PHANTOMJS_DRIVER_PATH,
            load_images=False,
            logger=self.lg,
            user_agent_type=PHONE,
            ip_pool_type=self.ip_pool_type,
        )
        # 输入框选择器
        input_css_sel = 'input#scform_srchtxt'
        submit_btn_sel = 'button#scform_submit'
        body = driver.get_url_body(
            url='http://www.etkz.cn/search.php?mod=forum',
            css_selector=submit_btn_sel,
            timeout=20,)
        assert body != ''
        # self.lg.info(body)
        driver.find_element(value=input_css_sel).send_keys(k)
        driver.find_element(value=submit_btn_sel).click()
        sleep(5.)
        body = Requests._wash_html(driver.page_source)
        assert body != ''
        self.lg.info(body)

        try:
            del driver
        except:
            pass

        question_item_sel = {
            'method': 'css',
            'selector': 'div#threadlist ul li',
        }
        question_desc_div_sel = {
            'method': 're',
            'selector': '问题：(.*?)答案：',
        }
        answer_div_sel = {
            'method': 're',
            'selector': '答案：(.*?)更多相关问题',
        }
        question_item = parse_field(
            parser=question_item_sel,
            target_obj=body,
            is_first=False,
            logger=self.lg,
        )
        assert question_item != []
        # pprint(question_item)

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
                        '<strong>',
                        '</strong>',
                        '<font .*?>',
                        '</font>',
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
                        '<strong>',
                        '</strong>',
                        '<font .*?>',
                        '</font>',
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

        self.lg.info('[{}] stg2, k: {}'.format(
            '+' if res != [] else '-',
            k,
        ))

        return {
            'k': k,
            'page_num': default_sort_value,
            'res': res,
        }

    @catch_exceptions_with_class_logger(default_res={})
    def get_stg_search_res(self, k: str, page_num: int, default_sort_value: int=None) -> dict:
        """
        搜题狗
        :param k:
        :return:
        """
        headers = get_random_headers(
            user_agent_type=1,
            connection_status_keep_alive=False,)
        headers.update({
            'Proxy-Connection': 'keep-alive',
            # 'Referer': 'http://www.etkz.cn/search.php?mod=forum&searchid=3&orderby=lastpost&ascdesc=desc&searchsubmit=yes&kw={}'.format(k),
        })
        params = [
            ('mod', 'forum'),
            ('searchid', '3'),          # searchid是无规律的, 现在还暂时无解, k 变动, searchid也变动才能搜索
            ('orderby', 'lastpost'),
            ('ascdesc', 'desc'),
            ('searchsubmit', 'yes'),
            ('kw', k),
            ('mobile', '2'),
        ]
        if page_num > 1:
            params.append(('page', page_num),)
        else:
            pass

        body = Requests.get_url_body(
            url='http://www.etkz.cn/search.php',
            headers=headers,
            params=params,
            verify=False,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.req_num_retries,
            proxy_type=PROXY_TYPE_HTTPS,
            timeout=self.req_timeout,
        )
        assert body != ''
        # self.lg.info(body)

        question_item_sel = {
            'method': 'css',
            'selector': 'div#threadlist ul li',
        }
        question_desc_div_sel = {
            'method': 're',
            'selector': '问题：(.*?)答案：',
        }
        answer_div_sel = {
            'method': 're',
            'selector': '答案：(.*?)更多相关问题',
        }
        question_item = parse_field(
            parser=question_item_sel,
            target_obj=body,
            is_first=False,
            logger=self.lg,
        )
        assert question_item != []
        # pprint(question_item)

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
                        '<strong>',
                        '</strong>',
                        '<font .*?>',
                        '</font>',
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
                        '<strong>',
                        '</strong>',
                        '<font .*?>',
                        '</font>',
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
            'page_num': default_sort_value,
            'res': res,
        }

    @catch_exceptions_with_class_logger(default_res={})
    def get_xms_search_res(self, k: str, default_sort_value: int=None) -> dict:
        """
        小马搜题
        :param k:
        :return:
        """
        headers = get_random_headers(
            user_agent_type=1,
            connection_status_keep_alive=False,
            upgrade_insecure_requests=False,
            cache_control='')
        headers.update({
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://so.xiaomasou.com/static/index.html',
        })
        params = (
            ('question', k),
        )
        body = Requests.get_url_body(
            url='http://so.xiaomasou.com/api/question',
            headers=headers,
            params=params,
            verify=False,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.req_num_retries,
            proxy_type=PROXY_TYPE_HTTPS,
            timeout=self.req_timeout)
        assert body != ''
        # self.lg.info(body)

        data = json_2_dict(
            json_str=body,
            default_res={},
            logger=self.lg,).get('data', {}).get('qaList', [])
        assert data != []
        # pprint(data)

        res = []
        for item in data:
            try:
                question = item.get('q', '')
                assert question != ''
                answer = item.get('a', '')
                assert answer != ''
            except AssertionError:
                continue

            ask_questions_result_item = AskQuestionsResultItem()
            ask_questions_result_item['question_desc'] = question
            ask_questions_result_item['answer'] = answer
            res.append(dict(ask_questions_result_item))

        self.lg.info('[{}] xms, k: {}'.format(
            '+' if res != [] else '-',
            k,
        ))

        return {
            'k': k,
            'page_num': default_sort_value,  # 用于单个结果的排序
            'res': res,
        }

    @catch_exceptions_with_class_logger(default_res={})
    def get_lyoo_search_res(self, k: str, default_sort_value: int=None) -> dict:
        """
        大学僧搜题
        :param k:
        :return:
        """
        headers = get_random_headers(
            connection_status_keep_alive=False,
        )
        headers.update({
            'Proxy-Connection': 'keep-alive',
            'Origin': 'http://souti.lyoo.xyz',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://souti.lyoo.xyz/',
        })
        data = {
            'w': k,
        }
        body = Requests.get_url_body(
            method='post',
            url='http://souti.lyoo.xyz/',
            headers=headers,
            data=data,
            verify=False,
            ip_pool_type=self.ip_pool_type,
            proxy_type=PROXY_TYPE_HTTPS,
            num_retries=self.req_num_retries,
            timeout=self.req_timeout)
        assert body != ''
        # self.lg.info(body)
        
        # 他也是基于凡尔搜题, 但是现在凡尔搜题接口不通, 就获取备用题库
        question_desc_div_sel = {
            'method': 're',
            'selector': '<br /> 问题：(.*?)答案：',
        }
        answer_div_sel = {
            'method': 're',
            'selector': '答案：(.*?)</a></span>',
        }
        question_desc_div = parse_field(
            parser=question_desc_div_sel,
            target_obj=body,
            logger=self.lg,
        )
        assert question_desc_div != ''
        answer_div = parse_field(
            parser=answer_div_sel,
            target_obj=body,
            logger=self.lg,
        )
        assert answer_div != ''

        res = []
        ask_questions_result_item = AskQuestionsResultItem()
        ask_questions_result_item['question_desc'] = question_desc_div
        ask_questions_result_item['answer'] = answer_div
        res.append(dict(ask_questions_result_item))

        self.lg.info('[{}] lyoo, k: {}'.format(
            '+' if res != [] else '-',
            k,
        ))

        return {
            'k': k,
            'page_num': default_sort_value,           # 用于单个结果的排序
            'res': res,
        }

    @catch_exceptions_with_class_logger(default_res={})
    def get_wkb_search_res(self, k: str, default_sort_value: int=None) -> dict:
        """
        网课帮搜题
        :param k:
        :return:
        """
        headers = get_random_headers(
            user_agent_type=1,
            connection_status_keep_alive=False,)
        headers.update({
            'Proxy-Connection': 'keep-alive',
            'Origin': 'http://wangkebang.cn',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://wangkebang.cn/m/',
        })

        data = {
            'w': k,
        }
        body = Requests.get_url_body(
            method='post',
            url='http://wangkebang.cn/m/',
            headers=headers,
            # cookies=cookies,
            data=data,
            verify=False,
            ip_pool_type=self.ip_pool_type,
            proxy_type=PROXY_TYPE_HTTPS,
            num_retries=self.req_num_retries,
            timeout=self.req_timeout,)
        assert body != ''
        # self.lg.info(body)

        # 只返回一个答案
        question_item_sel = {
            'method': 'css',
            'selector': 'div.layui-card-body span',
        }
        question_item = parse_field(
            parser=question_item_sel,
            target_obj=body,
            is_first=False,
            logger=self.lg,
        )
        assert question_item != []

        question_desc_div_sel = {
            'method': 'css',
            'selector': 'span strong',
        }
        answer_div_sel = {
            'method': 'css',
            'selector': 'span strong',
        }

        # 存储返回一个答案的问题和结果
        one_res = {}
        for index, item in enumerate(question_item):
            if index == 0:
                try:
                    question_desc_div = parse_field(
                        parser=question_desc_div_sel,
                        target_obj=item,
                        logger=self.lg,
                    )
                    assert question_desc_div != ''
                    # 清洗
                    question_desc = fix_text(wash_sensitive_info(
                        data=question_desc_div,
                        replace_str_list=[],
                        add_sensitive_str_list=[
                            '<span .*?>',
                            '</span>',
                            '<strong>',
                            '</strong>',
                            '题目\:',
                        ],
                        is_default_filter=False,
                        is_lower=False,
                    ))
                except Exception:
                    continue

                one_res['question_desc'] = question_desc

            elif index == 1:
                try:
                    answer_div = parse_field(
                        parser=answer_div_sel,
                        target_obj=item,
                        logger=self.lg,
                    )
                    assert answer_div != ''
                    # 清洗
                    answer = fix_text(wash_sensitive_info(
                        data=answer_div,
                        replace_str_list=[],
                        add_sensitive_str_list=[
                            '<span .*?>',
                            '</span>',
                            '<strong>',
                            '</strong>',
                            '答案\:',
                        ],
                        is_default_filter=False,
                        is_lower=False,
                    ))
                except Exception:
                    continue

                one_res['answer'] = answer

            else:
                continue

        res = []
        ask_questions_result_item = AskQuestionsResultItem()
        ask_questions_result_item['question_desc'] = one_res['question_desc']
        ask_questions_result_item['answer'] = one_res['answer']
        res.append(dict(ask_questions_result_item))

        self.lg.info('[{}] wkb, k: {}'.format(
            '+' if res != [] else '-',
            k,
        ))

        return {
            'k': k,
            'page_num': default_sort_value,           # 用于单个结果的排序
            'res': res,
        }

    async def _search_by_finer(self, k: str) -> list:
        """
        基于凡尔搜索(但是现在接口被封, 不提供搜索服务)
        :param k:
        :return:
        """
        async def get_tasks_params_list():
            tasks_params_list = []
            for page_num in range(0, 3):
                # 默认只返回前两页, 测试发现无限制, 自己设置返回3个避免时间过长
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
            'Referer': 'https://www.finerit.com/',
        })
        params = (
            ('q', k),
            ('p', str(page_num)),
            # ('s_type', 'erya'),
        )
        # todo 他们网站也许也有人在用, 偶尔会无响应
        body = Requests.get_url_body(
            url='https://www.finerit.com/tiku/search/',
            headers=headers,
            params=params,
            # cookies=cookies,
            ip_pool_type=self.ip_pool_type,
            proxy_type=PROXY_TYPE_HTTPS,
            num_retries=self.req_num_retries,
            timeout=self.req_timeout,         #  测试发现10s速度较快, 且成功率可以
        )
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