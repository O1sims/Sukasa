import json

from sukasa.config import BASE_PATH, MONGO_DB_INFO
from api.services.MongoService import MongoService


def insert_default_property_data():
    belfast_property_data = open('{}utils/data/belfastPropertyData.json'.format(BASE_PATH))
    belfast_master_data = open('{}utils/data/belfastMasterData.json'.format(BASE_PATH))
    belfast_properties = json.load(belfast_property_data)
    master_data = json.load(belfast_property_data)
    if MongoService().check_collection(
            collection_name=MONGO_DB_INFO['propertyCollection']):
        MongoService().drop_database(
            collection_name=MONGO_DB_INFO['propertyCollection'])
        MongoService().drop_database(
            collection_name=MONGO_DB_INFO['masterCollection'])
    MongoService().insert_to_collection(
        collection_name=MONGO_DB_INFO['propertyCollection'],
        data=belfast_properties)
    MongoService().insert_to_collection(
        collection_name=MONGO_DB_INFO['masterCollection'],
        data=belfast_master_data)
    return belfast_properties
