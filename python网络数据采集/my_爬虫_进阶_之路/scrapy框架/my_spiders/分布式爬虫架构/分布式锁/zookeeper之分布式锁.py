# coding:utf-8

'''
@author = super_fazai
@File    : zookeeper之分布式锁.py
@connect : superonesfazai@gmail.com
'''

import logging, os, time
from kazoo.client import KazooClient
from kazoo.client import KazooState
from kazoo.recipe.lock import Lock


class ZooKeeperLock():
    def __init__(self, hosts, id_str, lock_name, logger=None, timeout=1):
        self.hosts = hosts
        self.id_str = id_str
        self.zk_client = None
        self.timeout = timeout
        self.logger = logger
        self.name = lock_name
        self.lock_handle = None

        self.create_lock()

    def create_lock(self):
        try:
            self.zk_client = KazooClient(hosts=self.hosts, logger=self.logger, timeout=self.timeout)
            self.zk_client.start(timeout=self.timeout)
        except Exception as ex:
            self.init_ret = False
            self.err_str = "Create KazooClient failed! Exception: %s" % str(ex)
            logging.error(self.err_str)
            return

        try:
            lock_path = os.path.join("/", "locks", self.name)
            self.lock_handle = Lock(self.zk_client, lock_path)
        except Exception as ex:
            self.init_ret = False
            self.err_str = "Create lock failed! Exception: %s" % str(ex)
            logging.error(self.err_str)
            return

    def destroy_lock(self):
        # self.release()  

        if self.zk_client != None:
            self.zk_client.stop()
            self.zk_client = None

    def acquire(self, blocking=True, timeout=None):
        if self.lock_handle == None:
            return None

        try:
            return self.lock_handle.acquire(blocking=blocking, timeout=timeout)
        except Exception as ex:
            self.err_str = "Acquire lock failed! Exception: %s" % str(ex)
            logging.error(self.err_str)
            return None

    def release(self):
        if self.lock_handle == None:
            return None
        return self.lock_handle.release()

    def __del__(self):
        self.destroy_lock()


def main():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s -%(module)s:%(filename)s-L%(lineno)d-%(levelname)s: %(message)s')
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    zookeeper_hosts = "192.168.10.2:2181, 192.168.10.3:2181, 192.168.10.4:2181"
    lock_name = "test"

    lock = ZooKeeperLock(zookeeper_hosts, "myid is 1", lock_name, logger=logger)
    ret = lock.acquire()
    if not ret:
        logging.info("Can't get lock! Ret: %s", ret)
        return

    logging.info("Get lock! Do something! Sleep 10 secs!")
    for i in range(1, 11):
        time.sleep(1)
        print(str(i))

    lock.release()

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print("Ocurred Exception: %s" % str(ex))
        quit()  