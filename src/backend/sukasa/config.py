import os


BASE_PATH = '/sukasa/'

API_VERSION = '1.0.0'

DEVELOPMENT = os.getenv(
    key='DEVELOPMENT',
    default=True)

MONGO_CONNECTION = {
    "host": os.getenv(
        key='MONGO_HOSTNAME',
        default='mongo'),
    "port": int(os.getenv(
        key='MONGO_PORT',
        default=27017)),
    "db": os.getenv(
        key='DB_NAME',
        default='Sukasa')
}

MONGO_DB_INFO = {
    "propertyCollection": "properties",
    "masterCollection": "master",
    "userCollection": "users"
}

REDIS_CONNECTION = {
    "host": os.getenv(
        key='REDIS_HOSTNAME',
        default='sukasa-redis'),
    "port": os.getenv(
        key='REDIS_PORT',
        default='6379')
}

REDIS_TOKEN_EXP = 60

REDIS_KEYS = {
    "independentVariables": "independentVariables",
    "propertyValuationModel": "propertyValuationModel",
    "standardDeviation": "standardDeviation"
}
