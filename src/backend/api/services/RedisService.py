import redis as rd
import pandas as pd
import pickle as pk

from sukasa.config import REDIS_CONNECTION


class RedisService:
    def __init__(self):
        self.redis_connection = rd.Redis(
            host=REDIS_CONNECTION['host'],
            port=REDIS_CONNECTION['port'])

    def set_token(self, redis_key):
        setter_output = self.redis_connection.set(
            name=redis_key, 
            value="authToken", 
            ex=1200)
        if setter_output:
            print("Successfully set token into the `{}` key".format(
                redis_key))

    def check_token(self, redis_key):
        return self.redis_connection.exists(
            names=redis_key)

    def set_dataframe(self, dataframe, redis_key):
        setter_output = self.redis_connection.set(
            name=redis_key,
            value=dataframe.to_msgpack(
                compress='zlib'))
        if setter_output:
            print("Successfully set dataframe into the `{}` key".format(
                redis_key))

    def get_dataframe(self, redis_key):
        dataframe = pd.read_msgpack(self.redis_connection.get(redis_key))
        return dataframe

    def set_skl_model(self, model, redis_key):
        setter_output = self.redis_connection.set(
            name=redis_key,
            value=pk.dumps(model))
        if setter_output:
            print("Successfully set model into the `{}` key".format(
                redis_key))

    def get_skl_model(self, redis_key):
        skl_model = pk.loads(self.redis_connection.get(redis_key))
        return skl_model

    def getter(self, redis_key):
        return self.redis_connection.get(redis_key)

    def setter(self, value, redis_key):
        self.redis_connection.set(
            name=redis_key, 
            value=value)
