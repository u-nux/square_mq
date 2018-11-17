import rabbitmqclient

mq = rabbitmqclient.RabbitMQ()
mq.worker()

