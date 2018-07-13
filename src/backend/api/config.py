#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os

ELASTICSEARCH_CONNECTION = {
    "host": os.environ.get(
        key='ELASTICSEARCH_HOSTNAME',
        failobj='elasticsearch'),
    "port": os.environ.get(
        key='ELASTICSEARCH_PORT',
        failobj=9200)
}
