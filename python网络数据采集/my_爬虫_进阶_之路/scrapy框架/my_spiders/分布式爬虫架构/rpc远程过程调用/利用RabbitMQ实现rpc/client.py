# coding:utf-8

'''
@author = super_fazai
@File    : client.py
@connect : superonesfazai@gmail.com
'''

# import pika
from pika import (
    BlockingConnection,
    ConnectionParameters,
    BasicProperties,
)
from uuid import uuid4

class RpcClient(object):
    def __init__(self):
        self.connection = BlockingConnection(ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, name):
        '''
        接收参数name作为被调用的远程函数的名字，通过app_id传给服务端程序
        :param name:
        :return:
        '''
        self.response = None
        self.corr_id = str(uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=BasicProperties(
               reply_to=self.callback_queue,
               correlation_id=self.corr_id,
               app_id=str(name),
            ),
            body="request")

        while self.response is None:
            self.connection.process_data_events()

        return str(self.response)

rpc = RpcClient()
print("[x] Requesting")
index = 0
while True:
    if index > 1000:
        break
    response = rpc.call("b")
    print("[.] Got %r" % response)
    index += 1