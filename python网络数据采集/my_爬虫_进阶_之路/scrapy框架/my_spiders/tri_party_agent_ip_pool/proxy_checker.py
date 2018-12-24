# coding:utf-8

'''
@author = super_fazai
@File    : proxy_checker.py
@connect : superonesfazai@gmail.com
'''

from utils import judge_ip_is_anonymity
from items import ProxyItem
from db_controller import (
    create_proxy_obj_table,
    empty_db_proxy_data,)
from settings import (
    CONCURRENCY_NUM,
    INIT_SCORE,
    CHECKED_PROXY_SLEEP_TIME,
    MIN_IP_POOl_NUM,
    MIN_SCORE,
    HOROCN_API_URL,
    HOROCN_TOKEN,)

from requests import session
from gc import collect
from termcolor import colored
from urllib.parse import unquote_plus
from fzutils.spider.async_always import *
from fzutils.sql_utils import BaseSqlite3Cli
from fzutils.spider.selector import async_parse_field

import requests
from requests.exceptions import ProxyError
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class ProxyChecker(AsyncCrawler):
    """
    第三方代理高匿可用度验证器(可扩展)

        已验证(短效高匿代理[下面都为测试单日不限量版]):
        1. 快代理vip(包月:200, 高匿名数量极低)
        2. 蜻蜓代理(包月:240, 高匿数量大, 接口并发: 否[5-10s一次])
        3. 站大爷(包月:475, 太贵)
        4. 蘑菇代理(包月:499, 太贵, 高匿数量大)
    """
    def __init__(self, tri_id, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
        )
        self.concurrency = CONCURRENCY_NUM
        self.local_ip = ''                      # 本地ip值
        self.checked_proxy_list = []            # 已被验证的proxy的list
        self.score = INIT_SCORE
        self.CHECKED_PROXY_SLEEP_TIME = CHECKED_PROXY_SLEEP_TIME
        self.MIN_IP_POOl_NUM = MIN_IP_POOl_NUM
        self.MIN_SCORE = MIN_SCORE
        self._init_base_sql_str()
        self.sqlite3_cli = BaseSqlite3Cli(db_path='proxy.db')
        self.tri_id = tri_id                    # 三方的id

    @staticmethod
    async def _get_rules_list(data=None, area='') -> list:
        '''
        设置三方代理抽取规格
        :param data: data dict中待提取的源对象(源数据 or item), 每个selector可能不同, 需要进行动态的赋值data获取正确的selector
        :param area: '' | '国内' | '国外'
        :return:
        '''
        return [
            {
                'id': 0,
                'api_return_type': 'json',
                'origin': 'www.kuaidaili.com',
                # 高匿
                # 'api_url': 'https://dev.kdlapi.com/api/getproxy/?orderid=964285337936533&num=100&area={}&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=2&method=2&an_ha=1&sp2=1&f_loc=1&f_an=1&f_pr=1&f_sp=1&quality=1&sort=2&format=json&sep=1'.format(unquote_plus(area)),
                # 高匿 or 普匿
                'api_url': 'https://dev.kdlapi.com/api/getproxy/?orderid=964285337936533&num=100&area={}&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=2&method=2&an_an=1&an_ha=1&sp2=1&f_loc=1&f_an=1&f_pr=1&f_sp=1&quality=1&sort=2&format=json&sep=1'.format(unquote_plus(area)),
                'proxy_list': {
                    'method': 'dict_path',
                    'selector': data.get('data', {}).get('proxy_list', []) if isinstance(data, dict) else [],
                },
                'ip': {
                    'method': 're',
                    'selector': '(\d+\.\d+\.\d+\.\d+)',
                },
                'port': {
                    'method': 're',
                    'selector': ':(\d+),',
                },
                'activity_time': None,                      # ip存活时间, int 单位秒
                'add_white_list_url': None,                 # 增加白名单的url
                'api_url_call_frequency_sleep_time': 4.5,   # 非并发api_url单次调用频率的休眠时间
            },
            {
                'id': 1,
                'api_return_type': 'json',
                'origin': 'proxy.horocn.com',
                'api_url': HOROCN_API_URL,
                'proxy_list': {
                    'method': 'dict_path',
                    'selector': data if isinstance(data, list) else [],
                },
                'ip': {
                    'method': 'dict_path',
                    'selector': data.get('host', '') if isinstance(data, dict) else '',
                },
                'port': {
                    'method': 'dict_path',
                    'selector': data.get('port', '') if isinstance(data, dict) else '',
                },
                'activity_time': 6 * 60,                    # 官方3分钟, 此处我设置为6
                'add_white_list_url': 'https://proxy.horocn.com/api/ip/whitelist',
                'api_url_call_frequency_sleep_time': 0,
            },
            {
                'id': 2,
                'api_return_type': 'json',
                'origin': 'www.moguproxy.com',
                'api_url': 'http://piping.mogumiao.com/proxy/api/get_ip_bs?appKey=f6663fc6d2e746219cd6de180d3db78c&count=30&expiryDate=0&format=1&newLine=2',
                'proxy_list': {
                    'method': 'dict_path',
                    'selector': data.get('msg', []) if isinstance(data, dict) else [],
                },
                'ip': {
                    'method': 'dict_path',
                    'selector': data.get('ip', '') if isinstance(data, dict) else '',
                },
                'port': {
                    'method': 'dict_path',
                    'selector': data.get('port', '') if isinstance(data, dict) else '',
                },
                'activity_time': 5 * 60,
                'add_white_list_url': None,
                'api_url_call_frequency_sleep_time': 4.5,
            }
        ]

    @staticmethod
    async def _get_insert_params(item) -> dict:
        '''
        获取待插入的参数
        :return:
        '''
        return {
            'ip': item['ip'],
            'port': int(item['port']),
            'score': item['score'],
            'agency_agreement': item['agency_agreement'],
            'check_time': item['check_time'],
        }

    @staticmethod
    async def _welcome() -> None:
        '''
        欢迎页
        :param self:
        :return:
        '''
        _welcome = r'''
            ____                           ________              __            
           / __ \_________  _  ____  __   / ____/ /_  ___  _____/ /_____  _____
          / /_/ / ___/ __ \| |/_/ / / /  / /   / __ \/ _ \/ ___/ //_/ _ \/ ___/
         / ____/ /  / /_/ />  </ /_/ /  / /___/ / / /  __/ /__/ ,< /  __/ /    
        /_/   /_/   \____/_/|_|\__, /   \____/_/ /_/\___/\___/_/|_|\___/_/     
                              /____/                                           
        '''
        _author = r'''
                                                                By: super_fazai
        '''
        print(colored(_welcome, 'green'))
        print(colored(_author, 'red'))

        return None

    async def _fck_run(self) -> None:
        '''
        main
        :return:
        '''
        await self._welcome()
        self.local_ip = await self._get_local_ip()
        create_proxy_obj_table()
        # 每次启动先清空一次过期table
        print('Empty db old ip...')
        empty_db_proxy_data()
        # 添加本机到白名单
        await self._add_to_white_list()
        self.checked_proxy_list = await self._get_db_old_data()
        activity_time = await self._get_ip_activity_time()
        # 非并发api_url单次调用频率的休眠时间
        api_url_call_frequency_sleep_time = await self._get_api_url_call_frequency_sleep_time()
        while True:
            while len(self.checked_proxy_list) < self.MIN_IP_POOl_NUM:
                print('--->>> Ip Pool num: {} 个'.format(len(self.checked_proxy_list)))
                try:
                    # 单次请求api获取数据
                    proxy_list = await self._get_proxy_list(id=self.tri_id)
                except:
                    await async_sleep(4)
                    continue

                # pprint(proxy_list)
                if proxy_list == []:
                    await async_sleep(4)

                # 验证此次api返回数据的可用性
                check_res = await self._check_proxy_list(proxy_list=proxy_list)
                # pprint(check_res)
                await self._add_to_checked_proxy_list(check_res=check_res)
                await self._insert_into_db()
                await async_sleep(api_url_call_frequency_sleep_time)    # 避免调用频次过快

            # 检验所有可用proxy
            if activity_time is None:
                # activity_time为空，则表明存活时间未知, 调用检测
                await self._check_proxy_list(proxy_list=self.checked_proxy_list)

            self.checked_proxy_list = await self._delete_proxy_item()

            # 更新db proxy
            await self._update_db()

            if activity_time is None:
                print('self.checked_proxy_list验证完毕, 进入休眠{}s...'.format(self.CHECKED_PROXY_SLEEP_TIME))
                await async_sleep(self.CHECKED_PROXY_SLEEP_TIME)
            else:   # activity_time不为空, 则实时监控
                pass

    async def _get_api_url_call_frequency_sleep_time(self) -> (int, float):
        '''
        得到api_url的单次调用频率
        :return:
        '''
        rules_list = await self._get_rules_list()
        for i in rules_list:
            if i['id'] == self.tri_id:
                api_url_call_frequency_sleep_time = i['api_url_call_frequency_sleep_time']

                return api_url_call_frequency_sleep_time

        raise NotImplementedError

    async def _add_to_white_list(self) -> bool:
        '''
        添加本机ip到白名单
        :return:
        '''
        add_white_list_url = None
        rules_list = await self._get_rules_list()
        for i in rules_list:
            if i['id'] == self.tri_id:
                add_white_list_url = i['add_white_list_url']

        if add_white_list_url is None:
            return False

        with session() as s:
            if self.tri_id == 1:
                params = (
                    ('token', HOROCN_TOKEN),
                    ('ip', self.local_ip),
                )
                with s.put(url=add_white_list_url, params=params) as resp:
                    res = json_2_dict(resp.text).get('msg', 'err')
                    if res == 'ok' or '白名单记录已存在' in res:
                        print('{} add to 白名单 success!'.format(self.local_ip))
                        return True
                    assert res != 'err', '添加ip白名单失败!'

            else:
                raise NotImplementedError

    async def _get_db_old_data(self) -> list:
        '''
        得到db中原先保存的proxy data
        :return:
        '''
        db_old_data = await self._select_all_proxy_data_in_db()
        activity_time = await self._get_ip_activity_time()
        _ = []
        for item in db_old_data:
            ip = item[1]
            port = item[2]
            score = item[3]
            agency_agreement = item[4]
            check_time = string_to_datetime(item[5])

            # 已失效的ip pass
            now_time = get_shanghai_time()
            if datetime_to_timestamp(now_time) - datetime_to_timestamp(check_time) > activity_time - 10:
                continue

            _.append({
                'ip': ip,
                'port': port,
                'score': score,
                'agency_agreement': agency_agreement,
                'check_time': now_time,
            })

        return _

    async def _select_all_proxy_data_in_db(self) -> list:
        '''
        返回db中所有proxy item
        :return:
        '''
        cursor = self.sqlite3_cli._execute(sql_str=self.select_sql_str)
        db_old_data = cursor.fetchall()
        cursor.close()

        return db_old_data

    async def _get_ip_activity_time(self, id:int=None) -> int:
        '''
        得到规则中的单个ip存活时长(单位秒)
        :return:
        '''
        id = self.tri_id if id is None else id
        rules_list = await self._get_rules_list()
        for i in rules_list:
            if i['id'] == id:
                activity_time = i['activity_time']

                return activity_time

        raise NotImplementedError

    async def _insert_into_db(self) -> None:
        '''
        插入db
        :return:
        '''
        db_old_data = await self._select_all_proxy_data_in_db()
        db_ip_list = [i[1] for i in db_old_data]
        for item in self.checked_proxy_list:
            ip = item['ip']
            if ip not in db_ip_list:
                params = await self._get_insert_params(item)
                # pprint(params)
                cursor = self.sqlite3_cli._execute(sql_str=self.insert_sql_str, params=params)
                res = True if cursor.rowcount > 0 else False
                cursor.close()
                # print('[{}] {}插入db中.'.format('+' if res else '-', item['ip']))

        return

    async def _update_db(self) -> None:
        '''
        更新db数据(包括低分删除)
        :return:
        '''
        print('@@@ 更新db proxy...')
        db_old_data = await self._select_all_proxy_data_in_db()
        db_ip_list = [i[1] for i in db_old_data]
        checked_ip_list = [i['ip'] for i in self.checked_proxy_list]
        # 删除过期ip
        delete_count = 0
        for ip in db_ip_list:
            if ip not in checked_ip_list:
                delete_res = await self._delete_proxy_in_db(ip=ip)
                if delete_res:
                    delete_count += 1

        # 更新ip score
        update_count = 0
        for item in self.checked_proxy_list:
            ip = item['ip']
            score = item['score']
            check_time = item['check_time']
            if ip in db_ip_list:
                update_res = await self._update_score_in_db(ip=ip, score=score, check_time=check_time)
                if update_res:
                    update_count += 1

        print('db 删除num: {}, 更新num: {}'.format(delete_count, update_count))
        await async_sleep(5)

        return None

    async def _delete_proxy_in_db(self, ip) -> bool:
        '''
        删除db中的ip
        :return:
        '''
        cursor = self.sqlite3_cli._execute(sql_str=self.delete_sql_str, params=(ip,))
        res = True if cursor.rowcount > 0 else False
        # print('[{}] {} delete {}'.format('+' if res else '-', ip, 'success' if res else 'error'))
        cursor.close()

        return res

    async def _update_score_in_db(self, ip, score, check_time) -> bool:
        '''
        更新db中的score
        :return:
        '''
        cursor = self.sqlite3_cli._execute(sql_str=self.update_sql_str, params=(score, check_time, ip,))
        res = True if cursor.rowcount > 0 else False
        # print('[{}] {} update {} {}'.format('+' if res else '-', ip, score, check_time))
        cursor.close()

        return res

    async def _delete_proxy_item(self) -> list:
        '''
        删除score低的proxy
        :return:
        '''
        new = []
        now_time = get_shanghai_time()
        activity_time = await self._get_ip_activity_time()
        for item in self.checked_proxy_list:
            # 两个判断条件分开: 针对不同情况进行优先级判断
            if datetime_to_timestamp(now_time) - datetime_to_timestamp(item['check_time']) > activity_time - 10:
                continue

            if item.get('score') < self.MIN_SCORE:
                continue

            new.append(item)

        return new

    async def _dynamic_get_new_dict_rule(self, **kwargs) -> dict:
        '''
        动态刷新并获取新规则(其他的类似就行修改即可)
        :return:
        '''
        data = kwargs.get('data')
        area = kwargs.get('area', '')
        id = kwargs.get('id')

        try:
            rules_list = await self._get_rules_list(data=data, area=area)
            # pprint(three_party_agent_rules_list)
        except AttributeError:
            raise AttributeError('此次获取失败!')

        this_rules = {}
        for item in rules_list:
            if item['id'] == id:
                this_rules = item
                break

        assert this_rules != {}, 'this_rules为空dict!'

        return this_rules

    async def _get_proxy_list(self, id, area='') -> list:
        '''
        根据api获取并解析得到proxy_list
        :param id:
        :param area: '国内' or '国外'
        :return:
        '''
        # 先调用一次获取api_url and api_return_type
        api_url = ''
        api_return_type = ''
        _ = await self._get_rules_list(area=area)
        for item in _:
            if item['id'] == id:
                api_url = item['api_url']
                api_return_type = item['api_return_type']
                break
        assert api_url != '' or api_return_type != '', 'api_url为空值 or api_return_type为空值!'

        with session() as s:
            with s.get(api_url, headers=get_base_headers(), params=None) as response:
                body = response.text
                # print(body)
                data = body if api_return_type != 'json' else json_2_dict(body)
                # pprint(data)
                # 对应提取规则

        all = await self._parse_ori_proxy_list_data(data=data, area=area, id=id)

        return all

    async def _parse_ori_proxy_list_data(self, **kwargs) -> list:
        '''
        解析原始proxy_list数据
        :return:
        '''
        all = []
        data = kwargs.get('data', {})
        area = kwargs.get('area', '')
        id = kwargs.get('id')

        try:
            this_rule = await self._dynamic_get_new_dict_rule(data=data, area=area, id=id)
            proxy_list = await self._get_ori_proxy_list(parser=this_rule['proxy_list'], target_obj=data)
        except Exception as e:
            print(e)
            return all

        for item in proxy_list:
            try:
                this_rule = await self._dynamic_get_new_dict_rule(data=item, area=area, id=id)
                ip = await self._get_ip(parser=this_rule['ip'], target_obj=item)
                port = await self._get_port(parser=this_rule['port'], target_obj=item)
            except Exception as e:
                print(e)
                continue
            proxy_item = ProxyItem()
            proxy_item['ip'] = ip
            proxy_item['port'] = port
            proxy_item['agency_agreement'] = 'https'
            proxy_item['score'] = self.score
            proxy_item['check_time'] = get_shanghai_time()
            all.append(dict(proxy_item))

        return all

    async def _get_ori_proxy_list(self, parser, target_obj) -> list:
        '''
        获取origin proxy_list地址
        :param parser:
        :param target_obj:
        :return:
        '''
        proxy_list = await async_parse_field(parser=parser, target_obj=target_obj)
        assert  proxy_list != [], 'proxy_list为空list!'

        return proxy_list

    async def _get_ip(self, parser, target_obj) -> str:
        '''
        获取ip address
        :return:
        '''
        ip = await async_parse_field(parser=parser, target_obj=target_obj)
        assert ip != '', '获取到的ip为空值!'

        return ip

    async def _get_port(self, parser, target_obj):
        '''
        获取ip的端口
        :param parser:
        :param target_obj:
        :return:
        '''
        port = await async_parse_field(parser=parser, target_obj=target_obj)
        assert port != '', '获取到的port为空值!'

        return port

    async def _check_proxy_list(self, proxy_list):
        '''
        验证代理ip可用度
        :return:
        '''
        tasks_params_list = TasksParamsListObj(tasks_params_list=proxy_list, step=self.concurrency)
        all_res = []
        while True:
            try:
                slice_params_list = tasks_params_list.__next__()
                # self.lg.info(str(slice_params_list))
            except AssertionError:  # 全部提取完毕, 正常退出
                break

            tasks = []
            for item in slice_params_list:
                # ip = item.get('ip', '')
                # port = item.get('port', '')
                # print('create task: {}:{}'.format(ip, port))
                tasks.append(self.loop.create_task(self._check_one(item=item)))

            one_part_res = await async_wait_tasks_finished(tasks=tasks)
            for i in one_part_res:
                all_res.append(i)

        return all_res

    async def _check_one(self, **kwargs) -> dict:
        '''
        检测单个(只验证https, 保证高匿可用)
        :param kwargs:
        :return:
        '''
        async def _update_item() -> dict:
            '''更新item'''
            nonlocal res

            item.update({
                'used': res,
                'check_time': get_shanghai_time(),
            })
            score = item.get('score')
            if score is not None:
                if res:
                    score += 5
                else:
                    score -= 5
                item.update({
                    'score': score,
                })

            return item

        res = False     # 标记该proxy是否可用
        item = kwargs.get('item', {})
        ip = item.get('ip', '')
        port = item.get('port', '')

        # print('check {}:{}...'.format(ip, port))
        loop = get_event_loop()
        now_ip = self.local_ip
        try:
            # 返回ip地址
            now_ip = await loop.run_in_executor(None, judge_ip_is_anonymity, ip, port, True, True, 10)
        except ProxyError:
            pass
        except Exception as e:
            # print('检验proxy可用性时报错:')
            # print(e)
            pass
        finally:
            try:
                del loop
            except:
                pass
            collect()

        if self.local_ip != now_ip \
                and ',' not in now_ip:
            # print(now_ip)
            res = True

        return await _update_item()

    async def _get_local_ip(self) -> str:
        '''
        获取本地ip
        :return:
        '''
        # 检验两次确保本地ip获取正确
        first_ip = ''
        second_ip = ''
        print('正在获取本地ip...')
        while True:
            if (first_ip != '' and second_ip != '') and (first_ip == second_ip):
                break
            try:
                local_ip = judge_ip_is_anonymity(httpbin=False, use_proxy=False)
                first_ip = local_ip if first_ip == '' else first_ip
                second_ip = local_ip if first_ip != '' else second_ip
            except ProxyError:
                sleep_time = 6
                print('获取local_ip 失败!休眠{}s...'.format(5))
                await async_sleep(sleep_time)

        print('[local_ip]: {}'.format(second_ip))

        return second_ip

    async def _add_to_checked_proxy_list(self, check_res) -> int:
        '''
        new add to self.checked_proxy_list
        :return:
        '''
        used_index = 0
        _ = [i.get('ip', '') for i in self.checked_proxy_list] if self.checked_proxy_list != [] else []
        for item in check_res:
            ip = item.get('ip', '')
            if item.get('used', False):
                used_index += 1
                if ip not in _:
                    self.checked_proxy_list.append(item)

        print('[{}] new add 高匿ip num: {}'.format('+' if used_index > 0 else '-', used_index))

        return used_index

    def _init_base_sql_str(self) -> None:
        '''
        初始化基础sql_str
        :return:
        '''
        self.select_sql_str = 'select * from proxy_obj_table'
        self.insert_sql_str = 'insert into proxy_obj_table(ip, port, score, agency_agreement, check_time) values(:ip, :port, :score, :agency_agreement, :check_time)'
        self.delete_sql_str = 'delete from proxy_obj_table where ip=?'
        self.update_sql_str = 'update proxy_obj_table set score=?, check_time=? where ip=?'
        self.drop_table = 'drop table proxy_obj_table;'

    def __del__(self):
        try:
            del self.loop
        except:
            pass
        try:
            del self.sqlite3_cli
        except:
            pass
        collect()

def main():
    _ = ProxyChecker(tri_id=1)
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())

if __name__ == '__main__':
    main()