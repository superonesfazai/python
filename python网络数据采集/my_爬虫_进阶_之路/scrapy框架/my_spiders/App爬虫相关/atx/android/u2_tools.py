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
        device_list = await get_u2_init_device_list(
            loop=self.loop,
            u2=u2,
            open_someone_pkg=False,
            device_id_list=self.device_id_list,)

        tasks = []
        for device_obj in device_list:
            _print(msg='create task[where device_id: {}] to install app_url: {} ...'.format(device_obj.device_id, app_url))
            tasks.append(self.loop.create_task(self.async_app_install_someone_device(
                device_obj=device_obj,
                app_url=app_url,
                logger=logger,
            )))

        all_res = await async_wait_tasks_finished(tasks=tasks)
        _print(msg='所有设备安装完成@', logger=logger)
        try:
            del tasks
        except:
            pass

        return

    async def async_app_install_someone_device(self, device_obj, app_url, logger=None):
        """
        异步注入app
        :param device_obj:
        :param app_url:
        :return:
        """
        async def _get_args() -> list:
            """获取args"""
            return [
                device_obj,
                app_url,
                logger,
            ]

        loop = get_event_loop()
        args = await _get_args()
        device_obj = None
        try:
            device_obj = await loop.run_in_executor(None, self.app_install_someone_device, *args)
        except Exception as e:
            _print(msg='遇到错误:', logger=logger, log_level=2, exception=e)
        finally:
            # loop.close()
            try:
                del loop
            except:
                pass
            collect()

            return device_obj

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
    # loop = get_event_loop()
    # device_id_list = [
    #     # '816QECTK24ND8',
    #     'JNPJJREEY5NBS88D',
    # ]
    # _ = U2AppTools(device_id_list=device_id_list)
    # # 测试下载失败
    # res = loop.run_until_complete(_.app_install_all_devices(
    #     # app_url='https://file.io/4bNiGi',
    #     app_url='http://ge.tt/1uNnh2w2'
    # ))

    # 卸载atx, 避免编码时与uiautomator viewer冲突
    u2_uninstall_someone_app_by_device_id(
        device_id='JNPJJREEY5NBS88D',
        pkg_name='com.github.uiautomator',)

