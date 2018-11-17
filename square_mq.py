from flask import Flask, request, logging

from logging import StreamHandler

import mongocli
import rabbitmqclient

import ConfigParser
import os

config = ConfigParser.ConfigParser()
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
config.readfp(open(__location__ + '/configs.cfg'))

app = Flask(__name__)
app.debug = False


@app.route('/results/<int:num_to_get>', methods=['GET'])
def result(num_to_get):
    """
    result for given number
    :param num_to_get: number
    :return: data as json / error
    """
    mdbc = mongocli.MongoCli()
    mdbc.connect_to_db()
    data = mdbc.get_square(num_to_get)
    mdbc.close_db_connection()

    if data:
        return data
    else:
        return '{"number": '+str(num_to_get)+' ,"error": there is no data for given number '+str(num_to_get)+'}'


@app.route('/results')
def results():
    """
    gives all results as json array object
    :return: data
    """
    mdbc = mongocli.MongoCli()
    mdbc.connect_to_db()
    data = mdbc.get_all_squares()
    mdbc.close_db_connection()

    return data


@app.route('/calculate', methods=['POST'])
def send_to_calculate():
    """
    send data to calculate
    usage: post json given json format: {"number": <number>}
    :return: message
    """
    data_to_send = request.get_json()
    app.logger.debug(str(data_to_send))
    mq = rabbitmqclient.RabbitMQ()
    mq.new_task(str(data_to_send))

    return str(data_to_send), "sent\n"


if __name__ == '__main__':
    handler = StreamHandler()
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

    host = os.getenv('FLASK_HOST', config.get("flask", "host"))
    port = os.getenv('FLASK_PORT', config.get("flask", "port"))
    app.run(host=host, port=int(port))
