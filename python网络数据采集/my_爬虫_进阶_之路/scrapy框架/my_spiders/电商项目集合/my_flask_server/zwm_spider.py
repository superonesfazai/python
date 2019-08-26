# coding:utf-8

'''
@author = super_fazai
@File    : zwm_spider.py
@connect : superonesfazai@gmail.com
'''

"""
zwm spider
"""

from decimal import Decimal

from settings import (
    MY_SPIDER_LOGS_PATH,
    IP_POOL_TYPE,
    IS_BACKGROUND_RUNNING,
    ZWM_PWD_PATH,)
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from my_items import (
    ZWMBusinessSettlementRecordItem,
    ZWMBusinessManageRecordItem,
)
from sql_str_controller import (
    zwm_select_str_1,
    zwm_insert_str_1,
    zwm_select_str_2,
    zwm_insert_str_2,
    zwm_update_str_1,
)
from requests import session
from datetime import datetime
from requests_toolbelt import MultipartEncoder
from fzutils.exceptions import catch_exceptions_with_class_logger
from fzutils.spider.async_always import *

class ZWMSpider(AsyncCrawler):
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            ip_pool_type=IP_POOL_TYPE,
            log_print=True,
            log_save_path=MY_SPIDER_LOGS_PATH + '/zwm/_/',
        )
        self.init_zwm_pwd()
        self.concurrency = 20
        self.num_retries = 6
        self.max_transaction_details_page_num = 20              # 交易截止抓取页
        self.max_business_settlement_records_page_num = 20      # 商户结算记录截止抓取页
        self.max_business_manage_page_num = 80                  # 商户及门店管理截止抓取页(单数据也超过此数量就得进行修改)
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
                self.lg.info('获取所有商户结算记录...')
                all_business_settlement_records = await self._get_all_business_settlement_records_by_something()
                # pprint(all_business_settlement_records)
                self.lg.info('len_now_business_settlement_records: {}'.format(len(all_business_settlement_records)))
                await self._wash_save_all_business_settlement_records(target_list=all_business_settlement_records)
                self.lg.info('\n')

                # 获取所有商户及门店管理记录
                self.lg.info('获取所有商户及门店管理记录 ...')
                all_business_manage_records = await self._get_all_business_manage_records_by_something()
                # pprint(all_business_manage_records)
                self.lg.info('len_all_business_manage_records: {}'.format(len(all_business_manage_records)))
                await self._wash_save_all_business_manage_records(target_list=all_business_manage_records)
                self.lg.info('\n')

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

    async def _wash_save_all_business_manage_records(self, target_list: list):
        """
        清洗并存储所有未存储的 or 更新所有已存储的business manage records
        :param target_list:
        :return:
        """
        all_res = []
        for item in target_list:
            try:
                now_time = get_shanghai_time()
                create_time, modify_time, approval_status_change_time = now_time, now_time, now_time
                agent_name = item['agentName']
                top_agent_name = item['topAgentName']
                shop_type = item['merType']

                is_high_quality_shop = item['isHighQualityMer']
                if is_high_quality_shop == '否':
                    is_high_quality_shop = 0
                elif is_high_quality_shop == '是':
                    is_high_quality_shop = 1
                else:
                    raise ValueError('is_high_quality_shop value: {} 异常!'.format(is_high_quality_shop))

                shop_id = item.get('jhmid', '')
                assert shop_id != ''
                shop_chat_name = item.get('merchantName', '')
                assert shop_chat_name != ''
                phone_num = item.get('phone', '')
                assert phone_num != ''
                shop_chant_num = int(item['merchantNum'])
                sale = item['sale']
                is_real_time = 0 if item['isRealTime'] == '未开通' else 1
                approve_date = date_parse(item['approveDate'])
                rate = Decimal(item['rate']).__round__(4)
                account_type = item['accType']
                apply_time = date_parse(item['applyTime'])
                # 可为空值
                process_context = item.get('processContext', '')
                is_non_contact = 0 if item['isNonContact'] == '未开通' else 1

                approval_status = item['approvalStatus']
                if approval_status == '待审核':
                    approval_status = 1
                elif approval_status == '审核通过':
                    approval_status = 0
                elif approval_status == '退回':
                    approval_status = 2
                else:
                    raise ValueError('approval_status value: {} 异常'.format(approval_status))

                # 用其原值为定值不变, 且唯一
                unique_id = item['id']

            except Exception:
                self.lg.error('遇到错误:', exc_info=True)
                continue

            zwm_item = ZWMBusinessManageRecordItem()
            zwm_item['unique_id'] = unique_id
            zwm_item['create_time'] = create_time
            zwm_item['modify_time'] = modify_time
            zwm_item['agent_name'] = agent_name
            zwm_item['top_agent_name'] = top_agent_name
            zwm_item['shop_type'] = shop_type
            zwm_item['is_high_quality_shop'] = is_high_quality_shop
            zwm_item['shop_id'] = shop_id
            zwm_item['shop_chat_name'] = shop_chat_name
            zwm_item['phone_num'] = phone_num
            zwm_item['shop_chant_num'] = shop_chant_num
            zwm_item['sale'] = sale
            zwm_item['is_real_time'] = is_real_time
            zwm_item['approve_date'] = approve_date
            zwm_item['rate'] = rate
            zwm_item['account_type'] = account_type
            zwm_item['apply_time'] = apply_time
            zwm_item['process_context'] = process_context
            zwm_item['is_non_contact'] = is_non_contact
            zwm_item['approval_status'] = approval_status
            zwm_item['approval_status_change_time'] = approval_status_change_time
            all_res.append(dict(zwm_item))

            # 查看
            # if shop_id == 'YRMPAY100038574':
            # if phone_num == '18192242001':
            # if shop_chat_name == '哇哇叫':
            #     pprint(dict(zwm_item))

        # pprint(all_res)
        await self._insert_or_update_shop_manage_records_table(all_res=all_res)
        try:
            del all_res
        except:
            pass

        return None

    async def _insert_or_update_shop_manage_records_table(self, all_res: list):
        """
        插入or update原数据
        :param all_res:
        :return:
        """
        self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        try:
            db_data = self.sql_cli._select_table(
                sql_str=zwm_select_str_2,
                params=None,
                logger=self.lg, )
            # pprint(db_data)
            db_unique_id_list = [item[0] for item in db_data]
            assert db_unique_id_list != [], 'db_unique_id_list != []'
            self.lg.info('len_db_unique_id_list: {}'.format(len(db_unique_id_list)))
        except Exception:
            self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
            self.lg.error('遇到错误:', exc_info=True)
            return None

        new_add_count = 0
        for item in all_res:
            unique_id = item['unique_id']
            if unique_id not in db_unique_id_list:
                # 插入
                self.lg.info('inserting unique_id: {} ...'.format(unique_id))
                params = await self._get_insert_item_params2(item=item)
                try:
                    res = self.sql_cli._insert_into_table_2(
                        sql_str=zwm_insert_str_2,
                        params=params,
                        logger=self.lg)
                    if res:
                        new_add_count += 1
                except Exception:
                    self.lg.error('遇到错误:', exc_info=True)
                    continue
            else:
                db_old_approval_status, db_old_approval_status_change_time = await self._get_dd_old_approval_status_and_approval_status_change_time(
                    db_data=db_data,
                    unique_id=unique_id,)
                item['approval_status_change_time'] = await self._get_new_approval_status_change_time(
                    db_old_approval_status=db_old_approval_status,
                    db_old_approval_status_change_time=db_old_approval_status_change_time,
                    new_approval_status=item['approval_status'],
                    new_approval_status_change_time=item['approval_status_change_time'])
                # 更新
                self.lg.info('updating unique_id: {} ...'.format(unique_id))
                params = await self._get_update_item_params(item=item)
                try:
                    res = self.sql_cli._update_table_2(
                        sql_str=zwm_update_str_1,
                        params=params,
                        logger=self.lg)
                except Exception:
                    self.lg.error('遇到错误:', exc_info=True)
                    continue

        if not self.sql_cli.is_connect_success:
            self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        else:
            pass

        try:
            del db_data
            del db_unique_id_list
        except:
            pass

        self.lg.info('table.zwm_buss_manage_records新增个数: {}'.format(new_add_count))

    async def _get_new_approval_status_change_time(self,
                                                   db_old_approval_status,
                                                   db_old_approval_status_change_time,
                                                   new_approval_status,
                                                   new_approval_status_change_time):
        """
        获取新的approval_status_change_time
        :return:
        """
        if db_old_approval_status_change_time is not None:
            new_approval_status_change_time = db_old_approval_status_change_time \
                if db_old_approval_status == new_approval_status \
                else get_shanghai_time()
        else:
            pass

        return new_approval_status_change_time

    async def _get_dd_old_approval_status_and_approval_status_change_time(self, db_data: list, unique_id: str) -> tuple:
        """
        获取db 原先的approval_status
        :param db_data:
        :param unique_id:
        :return:
        """
        for item in db_data:
            if unique_id == item[0]:
                return item[1], item[2]
            else:
                continue

    async def _get_all_business_manage_records_by_something(self,):
        """
        获取所有商户及门店管理记录
        :return:
        """
        async def get_tasks_params_list(max_business_manage_page_num) -> list:
            """获取tasks_params_list"""
            tasks_params_list = []
            for page_num in range(1, max_business_manage_page_num):
                tasks_params_list.append({
                    'page_num': page_num,
                })

            return tasks_params_list

        def get_create_task_msg(k) -> str:
            return 'create task[where page_num: {}]...'.format(k['page_num'])

        def get_now_args(k) -> list:
            return [
                k['page_num'],
            ]

        res = await get_or_handle_target_data_by_task_params_list(
            loop=self.loop,
            tasks_params_list=await get_tasks_params_list(
                max_business_manage_page_num=self.max_business_manage_page_num),
            func_name_where_get_create_task_msg=get_create_task_msg,
            func_name=self._get_one_page_business_manage_records_by_something,
            func_name_where_get_now_args=get_now_args,
            func_name_where_handle_one_res=None,
            func_name_where_add_one_res_2_all_res=default_add_one_res_2_all_res,
            one_default_res=[],
            step=self.concurrency,
            logger=self.lg,
            get_all_res=True,)

        return res

    @catch_exceptions_with_class_logger(default_res=[])
    def _get_one_page_business_manage_records_by_something(self,
                                                           page_num: int,
                                                           start_date: str = None,
                                                           end_date: str = None,):
        """
        获取单页商户及门店管理记录
        :param page_num:
        :param start_date:      默认设置前一个月27号, eg: '2019-01-27 00:00'
        :param end_date:        eg: '2019-07-20 09:39'
        :return:
        """
        # todo 获取最开始->至今的, 即采集所有, 避免老店铺的审核状态变动, 而后台无法同步状态, 审核时间
        # start_date = str(self.get_1_on_the_month() if start_date is None else start_date).split(' ')[0] + ' 00:00'
        start_date = '2018-01-01 00:00'
        end_date = (str(get_shanghai_time()) if end_date is None else end_date)[0:16]
        self.lg.info('start_date: {}, end_date: {}'.format(start_date, end_date))

        headers = self.get_random_pc_headers()
        headers.update({
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://agent.yrmpay.com/JHAdminConsole/merchantMaterial/page.do',
            'X-Requested-With': 'XMLHttpRequest',
        })
        params = (
            ('_dc', get_now_13_bit_timestamp()),
        )
        data = {
            'merchantCode': '',
            'accType': '',
            'phone': '',
            'approveDate': '',
            'merchantName': '',
            'processStatus': '',
            'startTime': start_date,
            'endTime': end_date,
            'agentName': '',
            'page': str(page_num),
            'start': str((page_num - 1) * 100),     # 开始位置0, 100, 200
            'limit': '100',
        }
        url = 'https://agent.yrmpay.com/JHAdminConsole/merchantMaterial/materialList.do'
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
            default_res={}).get('materialList', [])

        self.lg.info('[{}] page_num: {}'.format(
            '+' if res != [] else '-',
            page_num,
        ))

        return res

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
            # pprint(item)
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
                # 正常情况为: '20190704', 异常为'20190824-20190824'
                txn_day = item['txnDay']
                if re.compile('-').findall(txn_day) != []:
                    txn_day = txn_day.split('-')[0]
                else:
                    pass
                trans_date = date_parse(txn_day)
                trans_status = item['status']
                if trans_status == '已结算':
                    trans_status = 0
                else:
                    raise ValueError('trans_status: {}, 未知交易状态!'.format(trans_status))
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

    async def _get_insert_item_params2(self, item) -> tuple:
        """
        待插入对象, zwm_buss_manage_records table
        :param item:
        :return:
        """
        return tuple([
            item['unique_id'],
            item['create_time'],
            item['modify_time'],
            item['agent_name'],
            item['top_agent_name'],
            item['shop_type'],
            item['is_high_quality_shop'],
            item['shop_id'],
            item['shop_chat_name'],
            item['phone_num'],
            item['shop_chant_num'],
            item['sale'],
            item['is_real_time'],
            item['approve_date'],
            item['rate'],
            item['account_type'],
            item['apply_time'],
            item['process_context'],
            item['is_non_contact'],
            item['approval_status'],
            item['approval_status_change_time'],
        ])

    async def _get_update_item_params(self, item: dict) -> tuple:
        """
        更新对象, zwm_buss_manage_records table
        :param item:
        :return:
        """
        return tuple([
            item['modify_time'],
            item['agent_name'],
            item['top_agent_name'],
            item['shop_type'],
            item['is_high_quality_shop'],
            item['shop_id'],
            item['shop_chat_name'],
            item['phone_num'],
            item['shop_chant_num'],
            item['sale'],
            item['is_real_time'],
            item['approve_date'],
            item['rate'],
            item['account_type'],
            item['apply_time'],
            item['process_context'],
            item['is_non_contact'],
            item['approval_status'],
            item['approval_status_change_time'],

            item['unique_id'],
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
        async def get_tasks_params_list(max_business_settlement_records_page_num) -> list:
            """获取tasks_params_list"""
            tasks_params_list = []
            for page_num in range(1, max_business_settlement_records_page_num):
                tasks_params_list.append({
                    'page_num': page_num,
                })

            return tasks_params_list

        def get_create_task_msg(k) -> str:
            return 'create task[where page_num: {}]...'.format(k['page_num'])

        def get_now_args(k) -> list:
            return [
                k['page_num'],
            ]

        res = await get_or_handle_target_data_by_task_params_list(
            loop=self.loop,
            tasks_params_list=await get_tasks_params_list(
                max_business_settlement_records_page_num=self.max_business_settlement_records_page_num),
            func_name_where_get_create_task_msg=get_create_task_msg,
            func_name=self._get_one_page_business_settlement_records_by_something,
            func_name_where_get_now_args=get_now_args,
            func_name_where_add_one_res_2_all_res=default_add_one_res_2_all_res,
            one_default_res=[],
            step=self.concurrency,
            logger=self.lg,
            get_all_res=True,)

        return res

    @catch_exceptions_with_class_logger(default_res=[])
    def _get_one_page_business_settlement_records_by_something(self,
                                                               page_num :int,
                                                               start_date: str=None,
                                                               end_date: str=None,
                                                               mid: str='',
                                                               agent_name: str='') -> list:
        """
        得到单页商户结算记录
        :param page_num:
        :param start_date:              默认设置前一个月27号, eg: '2019-07-01'
        :param end_date:                eg: '2019-07-16'
        :param mid:                     商户编号
        :param agent_name:              顶级机构名称
        :return:
        """
        start_date = str(self.get_1_on_the_month() if start_date is None else start_date).split(' ')[0]
        # start_date = '2018-01-01'
        end_date = (str(get_shanghai_time()) if end_date is None else end_date).split(' ')[0]
        self.lg.info('start_date: {}, end_date: {}'.format(start_date, end_date))

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

    @catch_exceptions_with_class_logger(default_res=[])
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
        # 避免月底流水无法获取
        day = 5

        now_month = now_time.month
        if now_month > 1:
            now_month -= 1
        else:
            # now_month为1月份
            now_month = 12

        return str(datetime(
            year=now_time.year,
            month=now_month,
            day=day,))

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
        headers = get_random_headers(
            upgrade_insecure_requests=False,
            cache_control='',)
        headers.update({
            'Origin': 'https://agent.yrmpay.com',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            # 'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundarytSJCAoaErjNY4IbM',
            'accept': 'text/plain, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
        })
        return headers

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

def _fck_run():
    zwm = ZWMSpider()
    loop = get_event_loop()
    loop.run_until_complete(zwm._fck_run())

def main():
    print('========主函数开始========')
    daemon_init()
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    _fck_run()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        _fck_run()