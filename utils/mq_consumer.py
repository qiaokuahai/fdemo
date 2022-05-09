import pika   
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='127.0.0.1', port=5672, ))     #定义连接池
channel = connection.channel()          
channel.queue_declare(queue='dns_queue1', durable=True)    #声明队列以向其发送消息消息
channel.queue_declare(queue='dns_queue2', durable=True)
def callback(ch, method, properties, body):
    print("received [x] message: %r" % ch, method, property, body)
    time.sleep(1)

# 接收消息：routing_key--队列名称，body--消息
channel.basic_consume(
    "dns_queue1",
    callback
)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
print("before close")
connection.close()   #关闭连接
print("after close")
