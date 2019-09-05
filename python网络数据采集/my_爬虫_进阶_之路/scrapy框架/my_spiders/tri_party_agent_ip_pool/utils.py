# coding:utf-8

'''
@author = super_fazai
@File    : utils.py
@connect : superonesfazai@gmail.com
'''

from settings import (
    HOROCN_API_URL,
    INIT_SCORE,
    HOROCN_TOKEN,
    delete_sql_str,
    update_sql_str,
    select_sql_str,
    insert_sql_str,
    MIN_SCORE,
)
from items import (
    ProxyItem,
)

from termcolor import colored
from urllib.parse import unquote_plus
from requests.exceptions import ProxyError

from fzutils.spider.selector import parse_field
from fzutils.sql_utils import BaseSqlite3Cli
from fzutils.spider.async_always import *

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def _get_db_old_data(tri_id, sqlite3_cli: BaseSqlite3Cli = None) -> list:
    """
    得到db中原先保存的proxy data
    :return:
    """
    db_old_data = _select_all_proxy_data_in_db(sqlite3_cli=sqlite3_cli)
    activity_time = _get_ip_activity_time(id=tri_id)
    db_proxy_item_list = []
    for item in db_old_data:
        ip = item[1]
        port = item[2]
        score = item[3]
        agency_agreement = item[4]
        check_time = string_to_datetime(item[5])

        # 已失效的ip pass
        now_time = get_shanghai_time()
        if datetime_to_timestamp(now_time) - datetime_to_timestamp(check_time) \
                > activity_time - 10:
            continue

        db_proxy_item_list.append({
            'ip': ip,
            'port': port,
            'score': score,
            'agency_agreement': agency_agreement,
            'check_time': check_time,
        })

    return db_proxy_item_list

def _insert_into_db(checked_proxy_list: list, sqlite3_cli: BaseSqlite3Cli = None) -> None:
    """
    插入db
    :return:
    """
    db_old_data = _select_all_proxy_data_in_db(sqlite3_cli=sqlite3_cli)
    db_ip_list = [i[1] for i in db_old_data]
    for item in checked_proxy_list:
        ip = item['ip']
        if ip not in db_ip_list:
            params = _get_insert_params(item)
            # pprint(params)
            cursor = sqlite3_cli._execute(
                sql_str=insert_sql_str,
                params=params)
            res = True if cursor.rowcount > 0 else False
            cursor.close()
            # print('[{}] {}插入db中.'.format('+' if res else '-', item['ip']))

        else:
            pass

    return

def _update_db(checked_proxy_list: list, sqlite3_cli: BaseSqlite3Cli=None) -> None:
    """
    更新db数据(包括低分删除)
    :return:
    """
    print('@@@ 更新db proxy...')
    db_old_data = _select_all_proxy_data_in_db(sqlite3_cli=sqlite3_cli)
    db_ip_list = [i[1] for i in db_old_data]
    checked_ip_list = [i['ip'] for i in checked_proxy_list]
    # pprint(db_ip_list)
    # pprint(checked_ip_list)
    # 删除过期ip
    delete_count = 0
    for ip in db_ip_list:
        if ip not in checked_ip_list:
            delete_res = _delete_proxy_in_db(
                ip=ip,
                sqlite3_cli=sqlite3_cli)
            if delete_res:
                delete_count += 1
            else:
                pass
        else:
            pass

    # 更新ip score
    update_count = 0
    for item in checked_proxy_list:
        ip = item['ip']
        score = item['score']
        check_time = item['check_time']
        if ip in db_ip_list:
            update_res = _update_score_in_db(
                ip=ip,
                score=score,
                check_time=check_time,
                sqlite3_cli=sqlite3_cli,)
            if update_res:
                update_count += 1
            else:
                pass
        else:
            pass

    print('db 删除num: {}, 更新num: {}'.format(delete_count, update_count))
    sleep(5)

    return None

def _select_all_proxy_data_in_db(sqlite3_cli: BaseSqlite3Cli=None) -> list:
    """
    返回db中所有proxy item
    :return:
    """
    cursor = sqlite3_cli._execute(sql_str=select_sql_str)
    db_old_data = cursor.fetchall()
    cursor.close()

    return db_old_data

def _add_to_checked_proxy_list(check_res, checked_proxy_list: list) -> list:
    """
    new add to checked_proxy_list
    :return:
    """
    used_index = 0
    ip_list = [i.get('ip', '') for i in checked_proxy_list] \
        if checked_proxy_list != [] else []
    for item in check_res:
        ip = item.get('ip', '')
        if item.get('used', False):
            used_index += 1
            if ip not in ip_list:
                checked_proxy_list.append(item)

    print('[{}] new add 高匿ip num: {}'.format(
        '+' if used_index > 0 else '-',
        used_index))

    return checked_proxy_list

def _delete_proxy_item(tri_id, checked_proxy_list: list) -> list:
    """
    删除score低的proxy
    :return:
    """
    now_time = get_shanghai_time()
    activity_time = _get_ip_activity_time(id=tri_id)
    # print(activity_time)

    new_checked_proxy_list = []
    # pprint(checked_proxy_list)
    for item in checked_proxy_list:
        # 两个判断条件分开: 针对不同情况进行优先级判断
        # print('now_time: {}, item_check_time: {}'.format(
        #     now_time,
        #     item['check_time'],))
        if datetime_to_timestamp(now_time) - datetime_to_timestamp(item['check_time']) \
                > activity_time - 10:
            continue

        if item.get('score') < MIN_SCORE:
            continue

        new_checked_proxy_list.append(item)

    return new_checked_proxy_list

def _get_ip_activity_time(id: int) -> int:
    """
    得到规则中的单个ip存活时长(单位秒)
    :return:
    """
    rules_list = get_proxy_rules_list()
    for i in rules_list:
        if i['id'] == id:
            activity_time = i['activity_time']

            return activity_time

    raise NotImplementedError

def _update_score_in_db(ip,
                        score,
                        check_time,
                        sqlite3_cli: BaseSqlite3Cli=None,) -> bool:
    """
    更新db中的score
    :return:
    """
    cursor = sqlite3_cli._execute(sql_str=update_sql_str, params=(score, check_time, ip,))
    res = True if cursor.rowcount > 0 else False
    # print('[{}] {} update {} {}'.format('+' if res else '-', ip, score, check_time))
    cursor.close()

    return res

def _delete_proxy_in_db(ip, sqlite3_cli: BaseSqlite3Cli=None,) -> bool:
    """
    删除db中的ip
    :param sqlite3_cli:
    :param ip:
    :return:
    """
    cursor = sqlite3_cli._execute(sql_str=delete_sql_str, params=(ip,))
    res = True if cursor.rowcount > 0 else False
    # print('[{}] {} delete {}'.format('+' if res else '-', ip, 'success' if res else 'error'))
    cursor.close()

    return res

def _check_one_proxy(local_ip, item=None) -> dict:
    """
    检测单个(只验证https, 保证高匿可用)
    :param kwargs:
    :return:
    """
    def _update_item() -> dict:
        """更新item"""
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

    res = False  # 标记该proxy是否可用
    item = item if item is not None else {}
    ip = item.get('ip', '')
    port = item.get('port', 0)

    # print('check {}:{}...'.format(ip, port))
    now_ip = unblock_judge_ip_is_anonymity(
        ip_address=ip,
        port=port,
        httpbin=True,
        use_proxy=True,
        timeout=10, )
    # print(now_ip)

    # TODO 下面是老版的httpbin.org判断
    # if self.local_ip != now_ip \
    #         and ',' not in now_ip:
    #     # print(now_ip)
    #     res = True

    # 新版判断, 新版不用代理请求httpbin返回格式: '原ip, 原ip'
    local_ip_str = '{}, {}'.format(local_ip, local_ip)
    if local_ip_str != now_ip \
            and local_ip not in now_ip:
        # print(now_ip)
        res = True

    return _update_item()

def _get_insert_params(item) -> dict:
    """
    获取待插入的参数
    :return:
    """
    return {
        'ip': item['ip'],
        'port': int(item['port']),
        'score': item['score'],
        'agency_agreement': item['agency_agreement'],
        'check_time': item['check_time'],
    }

def _get_api_url_call_frequency_sleep_time(tri_id) -> (int, float):
    """
    得到api_url的单次调用频率
    :return:
    """
    rules_list = get_proxy_rules_list()
    for i in rules_list:
        if i['id'] == tri_id:
            api_url_call_frequency_sleep_time = i['api_url_call_frequency_sleep_time']

            return api_url_call_frequency_sleep_time

    raise NotImplementedError

def _get_local_ip() -> str:
    """
    获取本地ip
    :return:
    """
    # httpbin = True
    httpbin = False

    # 检验两次确保本地ip获取正确
    first_ip = ''
    second_ip = ''
    print('正在获取本地ip...')
    while True:
        if (first_ip != '' and second_ip != '') and (first_ip == second_ip):
            break
        try:
            local_ip = unblock_judge_ip_is_anonymity(
                httpbin=httpbin,
                use_proxy=False,
            )
            if httpbin:
                local_ip = local_ip.split(',')[0]
            else:
                pass
            first_ip = local_ip if first_ip == '' else first_ip
            second_ip = local_ip if first_ip != '' else second_ip
        except ProxyError:
            sleep_time = 6
            print('获取local_ip 失败!休眠{}s...'.format(5))
            sleep(sleep_time)

    print('[local_ip]: {}'.format(second_ip))

    return second_ip

def _add_to_white_list(tri_id, local_ip) -> bool:
    """
    添加本机ip到白名单
    :return:
    """
    add_white_list_url = None
    rules_list = get_proxy_rules_list()
    for i in rules_list:
        if i['id'] == tri_id:
            add_white_list_url = i['add_white_list_url']

    if add_white_list_url is None:
        return False

    if tri_id == 1:
        params = (
            ('token', HOROCN_TOKEN),
            ('ip', local_ip),
        )
        body = Requests.get_url_body(
            # 注意这里方法是put
            method='put',
            use_proxy=False,
            url=add_white_list_url,
            params=params, )
        res = json_2_dict(
            json_str=body,
            default_res={}).get('msg', 'err')
        if res == 'ok' or '白名单记录已存在' in res:
            print('{} add to 白名单 success!'.format(local_ip))
            return True
        assert res != 'err', '添加ip白名单失败!'

    else:
        raise NotImplementedError

def unblock_judge_ip_is_anonymity(ip_address='',
                                  port=0,
                                  httpbin=True,
                                  use_proxy=True,
                                  timeout=10,
                                  logger=None,) -> str:
    """
    阻塞返回当前的ip地址
    :param ip_address:
    :param port:
    :param httpbin:
    :param use_proxy:
    :param timeout:
    :return:
    """
    def _get_proxies():
        return {
            # 暴露原地址
            # 'http': ip_address + ':' + str(port),
            'https': ip_address + ':' + str(port),
        }

    url = 'https://www.whatismybrowser.com/' if not httpbin else 'https://www.httpbin.org/get'
    headers = get_random_headers(user_agent_type=1,)
    proxies = _get_proxies() if use_proxy else {}
    body = Requests.get_url_body(
        url=url,
        headers=headers,
        use_proxy=use_proxy,
        proxies=proxies,
        timeout=timeout,
        verify=False,)
    # print(body)

    if not httpbin:
        now_ip_selector = {
            'method': 'css',
            'selector': 'div#ip-address:nth-child(2) .detected-column a:nth-child(1) ::text',
        }
        now_ip = parse_field(
            parser=now_ip_selector,
            target_obj=body,
            is_first=True,)

    else:
        now_ip = json_2_dict(
            json_str=body,
            default_res={},).get('origin', '')

    return now_ip

async def async_judge_ip_is_anonymity(ip_address='',
                                      port=0,
                                      httpbin=True,
                                      use_proxy=True,
                                      timeout=10,
                                      logger=None,):
    '''
    异步返回当前ip地址(用于判断ip地址是否高匿)
    :param ip_address:
    :param port:
    :param httpbin:
    :param use_proxy:
    :param timeout:
    :return:
    '''
    func_args = [
        ip_address,
        port,
        httpbin,
        use_proxy,
        timeout,
        logger,
    ]
    res = await unblock_func(
        func_name=unblock_judge_ip_is_anonymity,
        func_args=func_args,
        logger=logger,
        default_res='',)

    return res

def proxy_checker_welcome_page():
    """
    欢迎页
    :param self:
    :return:
    """
    _welcome = r"""
        ____                           ________              __            
       / __ \_________  _  ____  __   / ____/ /_  ___  _____/ /_____  _____
      / /_/ / ___/ __ \| |/_/ / / /  / /   / __ \/ _ \/ ___/ //_/ _ \/ ___/
     / ____/ /  / /_/ />  </ /_/ /  / /___/ / / /  __/ /__/ ,< /  __/ /    
    /_/   /_/   \____/_/|_|\__, /   \____/_/ /_/\___/\___/_/|_|\___/_/     
                          /____/                                           
    """
    _author = r"""
                                                            By: super_fazai
    """
    print(colored(_welcome, 'green'))
    print(colored(_author, 'red'))

    return None

def _get_proxy_list(id, area='') -> list:
    """
    根据api获取并解析得到proxy_list
    :param id:
    :param area: '国内' or '国外'
    :return:
    """
    # 先调用一次获取api_url and api_return_type
    api_url = ''
    api_return_type = ''
    _ = get_proxy_rules_list(area=area)
    for item in _:
        if item['id'] == id:
            api_url = item['api_url']
            api_return_type = item['api_return_type']
            break
    assert api_url != '' or api_return_type != '', 'api_url为空值 or api_return_type为空值!'

    headers = get_random_headers(
        connection_status_keep_alive=False,
        upgrade_insecure_requests=False,
        cache_control='',)
    body = Requests.get_url_body(
        use_proxy=False,
        url=api_url,
        headers=headers,
        params=None,)
    data = body \
        if api_return_type != 'json' \
        else json_2_dict(body)
    # pprint(data)
    # 对应提取规则

    all = parse_ori_proxy_list_data(data=data, area=area, id=id)

    return all

def parse_ori_proxy_list_data(**kwargs) -> list:
    """
    解析原始proxy_list数据
    :return:
    """
    all = []
    data = kwargs.get('data', {})
    area = kwargs.get('area', '')
    id = kwargs.get('id')

    try:
        this_rule = dynamic_get_new_dict_rule(
            data=data,
            area=area,
            id=id,)
        proxy_list = _get_ori_proxy_list(
            parser=this_rule['proxy_list'],
            target_obj=data,)
    except Exception as e:
        print(e)
        return all

    for item in proxy_list:
        try:
            this_rule = dynamic_get_new_dict_rule(data=item, area=area, id=id)
            ip = _get_ip(parser=this_rule['ip'], target_obj=item)
            port = _get_port(parser=this_rule['port'], target_obj=item)
        except Exception as e:
            print(e)
            continue
        proxy_item = ProxyItem()
        proxy_item['ip'] = ip
        proxy_item['port'] = port
        proxy_item['agency_agreement'] = 'https'
        proxy_item['score'] = INIT_SCORE
        proxy_item['check_time'] = get_shanghai_time()
        all.append(dict(proxy_item))

    return all

def dynamic_get_new_dict_rule(**kwargs) -> dict:
    """
    动态刷新并获取新规则(其他的类似就行修改即可)
    :return:
    """
    data = kwargs.get('data')
    area = kwargs.get('area', '')
    id = kwargs.get('id')

    try:
        rules_list = get_proxy_rules_list(data=data, area=area)
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

def _get_ori_proxy_list(parser, target_obj) -> list:
    """
    获取origin proxy_list地址
    :param parser:
    :param target_obj:
    :return:
    """
    # print(target_obj)
    proxy_list = parse_field(
        parser=parser,
        target_obj=target_obj)
    assert  proxy_list != [], 'proxy_list为空list!'

    return proxy_list

def _get_ip(parser, target_obj) -> str:
    """
    获取ip address
    :return:
    """
    ip = parse_field(parser=parser, target_obj=target_obj)
    assert ip != '', '获取到的ip为空值!'

    return ip

def _get_port(parser, target_obj):
    """
    获取ip的端口
    :param parser:
    :param target_obj:
    :return:
    """
    port = parse_field(parser=parser, target_obj=target_obj)
    assert port != '', '获取到的port为空值!'

    return port

def get_proxy_rules_list(data=None, area='') -> list:
    """
    设置三方代理抽取规格
    :param data: data dict中待提取的源对象(源数据 or item), 每个selector可能不同, 需要进行动态的赋值data获取正确的selector
    :param area: '' | '国内' | '国外'
    :return:
    """
    return [
        {
            'id': 0,
            'api_return_type': 'json',
            'origin': 'www.kuaidaili.com',
            # 高匿
            # 'api_url': 'https://dev.kdlapi.com/api/getproxy/?orderid=964285337936533&num=100&area={}&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=2&method=2&an_ha=1&sp2=1&f_loc=1&f_an=1&f_pr=1&f_sp=1&quality=1&sort=2&format=json&sep=1'.format(unquote_plus(area)),
            # 高匿 or 普匿
            'api_url': 'https://dev.kdlapi.com/api/getproxy/?orderid=964285337936533&num=100&area={}&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=2&method=2&an_an=1&an_ha=1&sp2=1&f_loc=1&f_an=1&f_pr=1&f_sp=1&quality=1&sort=2&format=json&sep=1'.format(
                unquote_plus(area)),
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
            'activity_time': None,  # ip存活时间, int 单位秒
            'add_white_list_url': None,  # 增加白名单的url
            'api_url_call_frequency_sleep_time': 4.5,  # 非并发api_url单次调用频率的休眠时间
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
            'activity_time': 4 * 60,  # 官方1-3分钟, 此处我设置为4(不可太大, 否则采集失败率高)
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