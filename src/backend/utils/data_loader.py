import json

from api.config import BASE_PATH, MONGO_DB_INFO
from api.services.MongoService import MongoService


def insert_default_property_data():
    json_data = open(BASE_PATH + 'utils/data/belfast_property_data.json')
    belfast_properties = json.load(json_data)
    if MongoService().check_collection(
            collection_name=MONGO_DB_INFO['propertyCollection']):
        MongoService().drop_database(
            collection_name=MONGO_DB_INFO['propertyCollection'])
    MongoService().insert_to_collection(
        collection_name=MONGO_DB_INFO['propertyCollection'],
        data=belfast_properties)
    return belfast_properties
