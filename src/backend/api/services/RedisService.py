import os

import redis as rd
import pandas as pd
import pickle as pk


class RedisService:
    def __init__(self):
        self.redis_connection = rd.Redis(
            host=os.environ.get('REDIS_HOSTNAME'),
            port=os.environ.get('REDIS_PORT'))

    def set_dataframe(self, dataframe, redis_key):
        setter_output = self.redis_connection.set(
            name=redis_key,
            value=dataframe.to_msgpack(
                compress='zlib'))
        if setter_output:
            print "Successfully set dataframe into the {} key".format(
                redis_key)

    def get_dataframe(self, redis_key):
        dataframe = pd.read_msgpack(self.redis_connection.get(redis_key))
        return dataframe

    def set_skl_model(self, model, redis_key):
        setter_output = self.redis_connection.set(
            name=redis_key,
            value=pk.dumps(model))
        if setter_output:
            print "Successfully set model into the {} key".format(
                redis_key)

    def get_skl_model(self, redis_key):
        skl_model = pk.loads(self.redis_connection.get(redis_key))
        return skl_model
