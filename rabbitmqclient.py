import pika
import logging

import time

import utils
import ConfigParser
import os

config = ConfigParser.ConfigParser()
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
config.readfp(open(__location__ + '/configs.cfg'))

# create logger
logger = logging.getLogger('rabbitmq_client')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


def callback(ch, method, properties, body):
    """
    callback mechanism
    :param ch: channel
    :param method: method
    :param properties: properties
    :param body: message body
    :return:
    """
    print(" [x] Received %r" % body)
    utils.process(data=body)
    time.sleep(1)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


class RabbitMQ:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=os.getenv('RABBIT_PORT_5671_TCP_ADDR', config.get("rabbitmq", "hostname"))))

    def new_task(self, msg):
        """
        task creator to sent message via rabbitmq queue
        :param msg: message to send
        :return: None
        """
        channel = self.connection.channel()

        channel.queue_declare(queue='task_queue', durable=True)

        message = msg
        channel.basic_publish(exchange='',
                              routing_key='task_queue',
                              body=message,
                              properties=pika.BasicProperties(
                                  delivery_mode=2,  # make message persistent
                              ))
        print(" [x] Sent %r" % message)
        self.connection.close()

    def worker(self):
        """
        consumer
        :return: None
        """
        channel = self.connection.channel()

        channel.queue_declare(queue='task_queue', durable=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(callback,
                              queue='task_queue')

        channel.start_consuming()


