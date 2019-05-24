# coding:utf-8

'''
@author = super_fazai
@File    : u2_tools.py
@connect : superonesfazai@gmail.com
'''

import uiautomator2 as u2
from gc import collect
from uiautomator2 import UIAutomatorServer
from fzutils.spider.app_utils import *
from fzutils.common_utils import _print
from fzutils.spider.async_always import *

class U2AppTools(object):
    """u2 app 工具类"""
    def __init__(self, device_id_list:list):
        self.device_id_list = device_id_list
        self.loop = get_event_loop()

    async def app_install_all_devices(self, app_url, logger=None) -> None:
        """
        注入所有设备
        or
        直接: $ adb -s 816QECTK24ND8 install xxxx.apk
        :param app_url: 可以用临时文件的形式来下载(先下载好原始apk, 再上传)(eg: https://www.file.io/)
        :param logger:
        :return:
        """
        device_list = await self._init_device_list()

        tasks = []
        for device_obj in device_list:
            _print(msg='create task[where device_id: {}] to install app_url: {} ...'.format(device_obj.device_id, app_url))
            func_args = [
                device_obj,
                app_url,
                logger,
            ]
            tasks.append(self.loop.create_task(unblock_func(
                func_name=self.app_install_someone_device,
                func_args=func_args,
            )))

        all_res = await async_wait_tasks_finished(tasks=tasks)
        _print(msg='所有设备安装完成@', logger=logger)
        try:
            del tasks
        except:
            pass

        return

    async def _get_now_app_pkg_name(self, logger=None):
        """
        获取当前app的pkg_name
        :return:
        """
        device_list = await self._init_device_list()

        tasks = []
        for device_obj in device_list:
            _print(msg='create task[where device_id: {}] ...'.format(device_obj.device_id,))
            tasks.append(self.loop.create_task(unblock_func(
                func_name=self._print_now_pkg_name,
                func_args=[device_obj,]
            )))

        all_res = await async_wait_tasks_finished(tasks=tasks)
        _print(msg='所有设备安装完成@', logger=logger)
        try:
            del tasks
        except:
            pass

        return

    async def _init_device_list(self):
        return await get_u2_init_device_list(
            loop=self.loop,
            u2=u2,
            open_someone_pkg=False,
            device_id_list=self.device_id_list,)

    def _print_now_pkg_name(self, device_obj, logger=None) -> None:
        """
        打印当前pkg_name
        :param device_obj:
        :param logger:
        :return:
        """
        d: UIAutomatorServer = device_obj.d

        print('device_id: {}, now_pkg_name: {}'.format(
            device_obj.device_id,
            d.current_app().get('package', ''),))

        return

    def app_install_someone_device(self, device_obj, app_url, logger=None) -> None:
        """
        app install某设备
        :return:
        """
        # d:UIAutomatorServer = device_obj.d
        d = device_obj.d

        d.app_install(
            url=app_url,
        )

    def __del__(self):
        try:
            del self.loop
        except:
            pass
        collect()

def u2_uninstall_someone_app_by_device_id(device_id: str, pkg_name: str):
    """
    卸载设备的某个app
    :param device_id:
    :param pkg_name:
    :return:
    """
    device_obj = u2_get_device_obj_by_device_id(
        u2=u2,
        device_id=device_id,
        pkg_name=pkg_name,
        open_someone_pkg=False,
    )
    # d: UIAutomatorServer = device_obj.d
    d = device_obj.d

    d.app_stop(pkg_name=pkg_name)
    d.app_uninstall(pkg_name=pkg_name)

    return

if __name__ == '__main__':
    loop = get_event_loop()
    device_id_list = [
        # '816QECTK24ND8',
        # 'JNPJJREEY5NBS88D',
        'KFWORWGQJNIBZPOV',
    ]
    _ = U2AppTools(device_id_list=device_id_list)
    # 测试下载失败
    # res = loop.run_until_complete(_.app_install_all_devices(
    #     # app_url='https://file.io/4bNiGi',
    #     app_url='http://ge.tt/1uNnh2w2'
    # ))

    # 打印当前包名
    res = loop.run_until_complete(_._get_now_app_pkg_name())

    # 卸载atx, 避免编码时与uiautomator viewer冲突
    # u2_uninstall_someone_app_by_device_id(
    #     device_id='JNPJJREEY5NBS88D',
    #     pkg_name='com.github.uiautomator',)

