import ast
import mongocli


def square_number(number):
    """
    calculates square of an integer
    :param number: num
    :return: squared num
    """
    acc = 0
    for i in range(number):
        acc += number

    return acc


def process(data):
    """
    processes consumed data
    :param data: consumed data
    :return: None
    """
    try:
        d = ast.literal_eval(data)
        number = int(d["number"])
        squared = square_number(number)
        mdbc = mongocli.MongoCli()
        mdbc.connect_to_db()
        mdbc.upsert_new_square(number, squared)
        mdbc.close_db_connection()
    except ValueError as e:
        print "unexpected data came via rabbitmq with error:", e
    else:
        print "calculated"


