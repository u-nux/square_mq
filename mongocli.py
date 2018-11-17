import ConfigParser
import os

from pymongo import MongoClient, ASCENDING

from bson.json_util import dumps

from datetime import datetime

config = ConfigParser.ConfigParser()
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
config.readfp(open(__location__ + '/configs.cfg'))


class MongoCli:
    def __init__(self):
        self.client = None
        self.db = None

    def connect_to_db(self):
        """
        creates mongoDB connection
        """
        uri = ["mongodb://" + os.getenv('MONGO_PORT_27017_TCP_ADDR', config.get("mongodb", "hostname")) + ":27017/squared"]
        self.client = MongoClient(uri)
        self.db = self.client.get_default_database()

    def upsert_new_square(self, number, square):
        """
        inserts or updates numbers square
        :param number: given number
        :param square: calculated square
        :return: None
        """
        self.db["squares"].update_one({u'number': number},
                                      {'$set': {u'number': number, u"square": square, u"timestamp": datetime.today()}},
                                      upsert=True)

    def get_square(self, number):
        """
        gets squares of given number
        :param number: given number
        :return: result of number
        """
        return dumps(self.db["squares"].find_one({"number": number}, {"_id": 0, "timestamp": 0}))

    def get_all_squares(self):
        """
        gets all squares as json array
        :return: squares of numbers calculated
        """
        return dumps(self.db["squares"].find({}, {"_id": 0, "timestamp": 0}).sort([(u"number", ASCENDING)]))

    def close_db_connection(self):
        """
        closes mongoDB connection
        """
        if self.client is not None:
            self.client.close()
