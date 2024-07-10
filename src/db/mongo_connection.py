import pymongo
from config import Config


def get_db():
    client = pymongo.MongoClient(Config.MONGODB_URI)
    return client.my_mongo_db
