#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os


BASE_PATH = '/sukasa/'

API_VERSION = "1.0.0"

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
