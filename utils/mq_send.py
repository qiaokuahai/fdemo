import pika   

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='127.0.0.1', port=5672, ))     #定义连接池
channel = connection.channel()          
channel.queue_declare(queue='dns_queue1', durable=True)    #声明队列以向其发送消息消息
channel.queue_declare(queue='dns_queue2', durable=True)
for i in range(100):
    channel.basic_publish(exchange='dns', routing_key='test_routing_key', body='Hello World!')  #注意当未定义exchange时，routing_key需和queue的值保持一致
print('send success msg to rabbitmq')
connection.close()   #关闭连接