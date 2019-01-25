import os


BASE_PATH = '/sukasa/'

API_VERSION = '1.0.0'

DEVELOPMENT = os.environ.get(
    key='DEVELOPMENT',
    failobj=True)

MONGO_CONNECTION = {
    "host": os.environ.get(
        key='MONGO_HOSTNAME',
        failobj='mongo'),
    "port": os.environ.get(
        key='MONGO_PORT',
        failobj=27017)
}

MONGO_DB_INFO = {
    "propertyCollection": "properties"
}

REDIS_KEYS = {
    "independentVariables": "independentVariables",
    "propertyValuationModel": "propertyValuationModel"
}
