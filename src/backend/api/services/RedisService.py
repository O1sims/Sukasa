import os
import pymongo as pm


class RedisService:
    def __init__(self):
        self.mongo_connection = pm.MongoClient(
            host=os.environ.get('MONGO_HOSTNAME'),
            port=int(os.environ.get('MONGO_PORT')))
