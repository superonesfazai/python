# coding:utf-8

'''
@author = super_fazai
@File    : server.py
@connect : superonesfazai@gmail.com
'''

# import pika
from pika import (
    BasicProperties,
    BlockingConnection,
    ConnectionParameters,)

connection = BlockingConnection(ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')

def a():
    return "a"

def b():
    return "b"

def on_request(ch, method, props, body):
    funname = props.app_id
    if funname == "a":
        response = a()
    elif funname == "b":
        response = b()
    else:
        raise ValueError('未定义该{}方法!'.format(funname))

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=BasicProperties(correlation_id=props.correlation_id),
        body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')
print("[x] 等待 rpc requests...")
channel.start_consuming()