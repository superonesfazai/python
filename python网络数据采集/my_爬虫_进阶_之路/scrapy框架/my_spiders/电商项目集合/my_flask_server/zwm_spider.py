# coding:utf-8

'''
@author = super_fazai
@File    : zwm_spider.py
@connect : superonesfazai@gmail.com
'''

from gc import collect
from settings import MY_SPIDER_LOGS_PATH
from decimal import Decimal

from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from my_items import ZWMBusinessSettlementRecordItem
from sql_str_controller import (
    zwm_select_str_1,
    zwm_insert_str_1,
)
from requests import session
from datetime import datetime
from requests_toolbelt import MultipartEncoder
from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.async_always import *

ZWM_PWD_PATH = '/Users/afa/myFiles/pwd/zwm_pwd.json'

class ZWMSpider(AsyncCrawler):
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            ip_pool_type=tri_ip_pool,
            log_print=True,
            log_save_path=MY_SPIDER_LOGS_PATH + '/zwm/_/',
        )
        self.init_zwm_pwd()
        self.concurrency = 10
        self.num_retries = 6
        self.max_transaction_details_page_num = 20              # 交易截止抓取页
        self.max_business_settlement_records_page_num = 20      # 商户结算记录截止抓取页
        self.login_cookies_dict = {}
        self.sleep_time = 5

    def init_zwm_pwd(self):
        ori_data = ''
        with open(ZWM_PWD_PATH, 'r') as f:
            for line in f:
                ori_data += line.replace('\n', '').replace('  ', '')
        data = json_2_dict(
            json_str=ori_data,
            logger=self.lg,
            default_res={},)
        self.zwm_username, self.zwm_pwd = data['username'], data['pwd']
        assert self.zwm_username != '' and self.zwm_pwd != ''

    async def _fck_run(self) -> None:
        while True:
            try:
                login_res = await self._login()
                assert login_res is True, '登录失败, 退出后续同步操作!'

                # 获取所有交易明细(自己有接口, 不需要了)
                # all_transaction_details = await self._get_all_transaction_details()
                # pprint(all_transaction_details)
                # self.lg.info('len_all_transaction_details: {}'.format(len(all_transaction_details)))
                # await self._wash_and_save_all_transaction_details(target_list=all_transaction_details)

                # 获取所有商户结算记录
                all_business_settlement_records = await self._get_all_business_settlement_records_by_something()
                # pprint(all_business_settlement_records)
                self.lg.info('len_all_business_settlement_records: {}'.format(len(all_business_settlement_records)))
                await self._wash_save_all_business_settlement_records(target_list=all_business_settlement_records)

            except Exception:
                self.lg.error('遇到错误:', exc_info=True)

            self.lg.info('## 同步完成 ##')
            self.lg.info('休眠 {} minutes ...'.format(self.sleep_time))

            # 定时
            await async_sleep(60 * self.sleep_time)

    async def _login(self) -> bool:
        """
        登录
        :return:
        """
        headers = await self._get_random_pc_headers()
        headers.update({
            'Referer': 'https://agent.yrmpay.com/JHAdminConsole/loginNew.jsp',
        })
        file_load = {
            'loginName': self.zwm_username,
            'userPassword': self.zwm_pwd,
        }
        m = MultipartEncoder(fields=file_load)
        # self.lg.info(m)
        headers.update({
            'Content-Type': m.content_type
        })
        login_url = 'https://agent.yrmpay.com/JHAdminConsole/foreigncard/permissionsLogin.do'

        with session() as _session:
            try:
                response = _session.post(
                    url=login_url,
                    headers=headers,
                    data=m,
                    proxies=self._get_proxies(),)
                login_res = json_2_dict(
                    json_str=response.text,
                    default_res={},
                    logger=self.lg, ).get('message', '')
                assert login_res == '登录成功', '登录失败!'
                self.lg.info(login_res)
                self.login_cookies_dict = response.cookies.get_dict()
                assert self.login_cookies_dict != {}, 'self.login_cookies_dict != 空dict!'
                # pprint(self.login_cookies_dict)
            except Exception:
                self.lg.error('遇到错误:', exc_info=True)
                return False

        return True

    async def _wash_save_all_business_settlement_records(self, target_list):
        """
        清洗并存储 未被存储的所有商户结算记录
        :param target_list:
        :return:
        """
        self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        try:
            db_data = self.sql_cli._select_table(
                sql_str=zwm_select_str_1,
                params=None,
                logger=self.lg,)
            # pprint(db_data)
            db_unique_id_list = [item[0] for item in db_data]
            assert db_unique_id_list != [], 'db_unique_id_list != []'
            self.lg.info('len_db_unique_id_list: {}'.format(len(db_unique_id_list)))
        except Exception:
            self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
            self.lg.error('遇到错误:', exc_info=True)
            return None

        all_res = []
        for item in target_list:
            try:
                create_time = get_shanghai_time()
                shop_name = item.get('merName', '')
                assert shop_name != ''
                shop_id = item.get('mid', '')
                assert shop_id != ''
                agent_name = item['agentName']
                top_agent_name = item['topAgentName']
                date_settle_type = item['settleType']
                trans_amount = item.get('transAmt', '')
                assert trans_amount != ''
                trans_amount = Decimal(trans_amount).__round__(2)
                service_charge = Decimal(item['mda']).__round__(2)
                accounting_amount = Decimal(item['mnamt']).__round__(2)
                trans_date = date_parse(item['txnDay'])
                trans_status = item['status']
                if trans_status == '已结算':
                    trans_status = 0
                else:
                    raise ValueError('trans_status 未知交易状态!')
                settle_type = item['type']
                settle_date = date_parse(item['minDay'])
                # 生成唯一标识码
                unique_id = get_uuid3(
                    target_str=shop_id + str(date_settle_type) + str(trans_amount) + \
                               str(service_charge) + str(trans_date) + \
                               str(settle_type) + str(settle_date),)
            except Exception:
                self.lg.error('遇到错误:', exc_info=True)
                continue

            if unique_id in db_unique_id_list:
                # self.lg.info('该record[unique_id: {}]已存在!'.format(unique_id))
                continue

            settle_record_item = ZWMBusinessSettlementRecordItem()
            settle_record_item['unique_id'] = unique_id
            settle_record_item['create_time'] = create_time
            settle_record_item['shop_name'] = shop_name
            settle_record_item['shop_id'] = shop_id
            settle_record_item['agent_name'] = agent_name
            settle_record_item['top_agent_name'] = top_agent_name
            settle_record_item['date_settle_type'] = date_settle_type
            settle_record_item['trans_amount'] = trans_amount
            settle_record_item['service_charge'] = service_charge
            settle_record_item['accounting_amount'] = accounting_amount
            settle_record_item['trans_date'] = trans_date
            settle_record_item['trans_status'] = trans_status
            settle_record_item['settle_type'] = settle_type
            settle_record_item['settle_date'] = settle_date
            all_res.append(dict(settle_record_item))

        # pprint(all_res)
        self.lg.info('未存储个数: {}'.format(len(all_res)))
        await self._save_all_business_settlement_records(all_res=all_res)

        try:
            del all_res
        except:
            pass

        return None

    async def _save_all_business_settlement_records(self, all_res) -> None:
        """
        存储新增的商家提现记录
        :param all_res:
        :return:
        """
        new_add_count = 0
        for item in all_res:
            # 处理未存储的新数据
            unique_id = item['unique_id']
            self.lg.info('saving unique_id: {} ...'.format(unique_id))
            params = await self._get_insert_item_params(item=item)
            try:
                res = self.sql_cli._insert_into_table_2(
                    sql_str=zwm_insert_str_1,
                    params=params,
                    logger=self.lg)
                if res:
                    new_add_count += 1
            except Exception:
                self.lg.error('遇到错误:', exc_info=True)
                continue

        if not self.sql_cli.is_connect_success:
            self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        else:
            pass

        self.lg.info('新增个数: {}'.format(new_add_count))

        return None

    async def _get_insert_item_params(self, item) -> tuple:
        """
        待插入对象
        :param item:
        :return:
        """
        return tuple([
            item['unique_id'],
            item['create_time'],
            item['shop_name'],
            item['shop_id'],
            item['agent_name'],
            item['top_agent_name'],
            item['date_settle_type'],
            item['trans_amount'],
            item['service_charge'],
            item['accounting_amount'],
            item['trans_date'],
            item['trans_status'],
            item['settle_type'],
            item['settle_date'],
        ])

    async def _wash_and_save_all_transaction_details(self, target_list: list):
        """
        清洗并存储所有交易明细
        :param target_list:
        :return:
        """
        pass

    async def _get_all_business_settlement_records_by_something(self):
        """
        获取所有商户结算记录
        :return:
        """
        async def _get_tasks_params_list() -> list:
            """获取tasks_params_list"""
            tasks_params_list = []
            for page_num in range(1, self.max_business_settlement_records_page_num):
                tasks_params_list.append({
                    'page_num': page_num,
                })

            return tasks_params_list

        tasks_params_list = await _get_tasks_params_list()
        tasks_params_list_obj = TasksParamsListObj(
            tasks_params_list=tasks_params_list,
            step=self.concurrency,)

        all_res = []
        while True:
            try:
                slice_params_list = tasks_params_list_obj.__next__()
            except AssertionError:
                break

            tasks = []
            for k in slice_params_list:
                page_num = k['page_num']
                self.lg.info('create task[where page_num: {}]...'.format(page_num))
                func_args = [
                    page_num,
                ]
                tasks.append(self.loop.create_task(
                    unblock_func(
                        func_name=self._get_one_page_business_settlement_records_by_something,
                        func_args=func_args,
                        logger=self.lg,)))

            one_res = await async_wait_tasks_finished(tasks=tasks)
            try:
                del tasks
            except:
                pass
            for i in one_res:
                for j in i:
                    all_res.append(j)

        return all_res

    def _get_one_page_business_settlement_records_by_something(self,
                                                               page_num :int,
                                                               start_date: str=None,
                                                               end_date: str=None,
                                                               mid: str='',
                                                               agent_name: str='') -> list:
        """
        得到单页商户结算记录
        :param page_num:
        :param start_date:              默认设置当月第一天, eg: '2019-07-01'
        :param end_date:                eg: '2019-07-16'
        :param mid:                     商户编号
        :param agent_name:              顶级机构名称
        :return:
        """
        res = []

        try:
            start_date = str(self.get_1_on_the_month() if start_date is None else start_date).split(' ')[0]
            # start_date = '2018-01-01'
            end_date = (str(get_shanghai_time()) if end_date is None else end_date).split(' ')[0]
            self.lg.info('start_date: {}, end_date: {}'.format(start_date, end_date))
        except IndexError:
            self.lg.error('遇到错误:', exc_info=True)
            return res

        headers = self.get_random_pc_headers()
        headers.update({
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://agent.yrmpay.com/JHAdminConsole/merSettle/querySettleJsp.do',
            'X-Requested-With': 'XMLHttpRequest',
        })
        params = (
            ('_dc', get_now_13_bit_timestamp()),
        )
        data = {
            'startDate': start_date,
            'endDate': end_date,
            'mid': mid,
            'agentName': agent_name,
            'loginAgentId': self.zwm_username[0:8],                   # 前8位
            'page': str(page_num),
            'start': str((page_num - 1) * 100),                       # 开始位置, 0, 100, 200
            'limit': '100',
        }
        url = 'https://agent.yrmpay.com/JHAdminConsole/merSettle/queryMerSettleList.do'
        try:
            body = Requests.get_url_body(
                method='post',
                url=url,
                headers=headers,
                params=params,
                cookies=self.login_cookies_dict,
                data=data,
                ip_pool_type=self.ip_pool_type,
                num_retries=self.num_retries,)
            # self.lg.info(body)
            assert body != '', 'body不为空值!'
            res = json_2_dict(
                json_str=body,
                logger=self.lg,
                default_res={}).get('data', [])
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)
            return res

        self.lg.info('[{}] page_num: {}'.format(
            '+' if res != [] else '-',
            page_num,
        ))

        return res

    async def _get_all_transaction_details(self) -> list:
        """
        获取所有交易流水
        :return:
        """
        async def _get_tasks_params_list() -> list:
            """获取tasks_params_list"""
            tasks_params_list = []
            for page_num in range(1, self.max_transaction_details_page_num):
                tasks_params_list.append({
                    'page_num': page_num,
                })

            return tasks_params_list

        tasks_params_list = await _get_tasks_params_list()
        tasks_params_list_obj = TasksParamsListObj(
            tasks_params_list=tasks_params_list,
            step=self.concurrency,)

        all_res = []
        while True:
            try:
                slice_params_list = tasks_params_list_obj.__next__()
            except AssertionError:
                break

            tasks = []
            for k in slice_params_list:
                page_num = k['page_num']
                self.lg.info('create task[where page_num: {}]...'.format(page_num))
                func_args = [
                    page_num,
                ]
                tasks.append(self.loop.create_task(
                    unblock_func(
                        func_name=self._get_one_page_transaction_details_by_something,
                        func_args=func_args,
                        logger=self.lg,)))

            one_res = await async_wait_tasks_finished(tasks=tasks)
            try:
                del tasks
            except:
                pass
            for i in one_res:
                for j in i:
                    all_res.append(j)

        return all_res

    def _get_one_page_transaction_details_by_something(self,
                                                      page_num: int,
                                                      start_date: str=None,
                                                      end_date: str=None,
                                                      transaction_status: str='',
                                                      mer_name: str='',
                                                      order_no: str='',
                                                      mid: str='',
                                                      agent_name: str='',
                                                      pay_channel: str ='',
                                                      sale_name: str='',) -> list:
        """
        获取单页交易流水
        :param page_num:                开始页面, eg: 1, 2, 3
        :param start_date:              eg: '2019-07-16 00:00'
        :param end_data:                eg: '2019-07-16 10:02'
        :param transaction_status:      交易状态 | 选择全部: '' or 交易成功: '1' or 退款成功: '3'
        :param mer_name:                待查询的商户名称
        :param order_no:                订单号
        :param mid:                     商户编号
        :param agent_name:              顶级机构名称
        :param pay_channel:             支付渠道 | 请选择: '' or 微信: '50' or 支付宝: '51' or 微信条码: '55' or 支付宝条码: '56' or 微信小程序: '67'
        :param sale_name:               销售名称
        :return:
        """
        res = []
        start_date = self.get_0_00_on_the_day() if start_date is None else start_date
        end_date = str(get_shanghai_time()) if end_date is None else end_date

        headers = self.get_random_pc_headers()
        headers.update({
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'Referer': 'https://agent.yrmpay.com/JHAdminConsole/limafuReport/transflow.do',
            'X-Requested-With': 'XMLHttpRequest',
        })
        params = (
            ('_dc', get_now_13_bit_timestamp()),
        )
        data = {
            'startDate': start_date,
            'endDate': end_date,
            'type': '2',
            'status': transaction_status,
            'payChannel': pay_channel,
            'orderNo': order_no,
            'merName': mer_name,
            'mid': mid,
            'agentName': agent_name,
            'saleName': sale_name,
            'page': str(page_num),
            'start': str((page_num - 1) * 20),          # 开始位置, 0, 20, 40
            'limit': '20',
        }
        url = 'https://agent.yrmpay.com/JHAdminConsole/limafuReport/querylimafuTransFlow.do'

        try:
            body = Requests.get_url_body(
                method='post',
                url=url,
                headers=headers,
                params=params,
                cookies=self.login_cookies_dict,
                data=data,
                ip_pool_type=self.ip_pool_type,
                num_retries=self.num_retries,)
            assert body != '', 'body不为空值!'
            res = json_2_dict(
                json_str=body,
                logger=self.lg,
                default_res={}).get('data', [])
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)
            return res

        self.lg.info('[{}] page_num: {}'.format(
            '+' if res != [] else '-',
            page_num,
        ))

        return res

    def get_0_00_on_the_day(self) -> str:
        """
        获取当天的0点
        :return:
        """
        now_time = get_shanghai_time()

        return str(datetime(
                year=now_time.year,
                month=now_time.month,
                day=now_time.day))

    def get_1_on_the_month(self) -> str:
        """
        获取当月的第一天
        :return:
        """
        now_time = get_shanghai_time()

        return str(datetime(
            year=now_time.year,
            month=now_time.month,
            day=1,))

    def _get_proxies(self) -> dict:
        """
        获取代理
        :return:
        """
        proxies = Requests._get_proxies(ip_pool_type=self.ip_pool_type, )
        assert proxies != {}, 'proxies不为空dict!'

        return proxies

    async def _get_random_pc_headers(self) -> dict:
        """
        :return:
        """
        return self.get_random_pc_headers()

    @staticmethod
    def get_random_pc_headers() -> dict:
        return {
            'Origin': 'https://agent.yrmpay.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'User-Agent': get_random_pc_ua(),
            # 'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundarytSJCAoaErjNY4IbM',
            'Accept': 'text/plain, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }

    def __del__(self):
        try:
            del self.lg
            del self.login_cookies_dict
        except:
            pass
        try:
            del self.loop
        except:
            pass
        collect()

if __name__ == '__main__':
    zwm = ZWMSpider()
    loop = get_event_loop()
    loop.run_until_complete(zwm._fck_run())