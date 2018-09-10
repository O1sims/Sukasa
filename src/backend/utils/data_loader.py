from analytics import config
from api.services.ElasticService import ElasticService
from utils.data.ni_property_data import DEFAULT_NI_PROPERTY_DATA


def save_default_property_data():
    if ElasticService().index_check(
            index=config.ELASTICSEARCH_QUERY_INFO['propertyIndex']):
        ElasticService().drop_database(
            index=config.ELASTICSEARCH_QUERY_INFO['propertyIndex'])
    else:
        ElasticService().create_index(
            index=config.ELASTICSEARCH_QUERY_INFO['propertyIndex'])
    ElasticService().save_to_database(
        index=config.ELASTICSEARCH_QUERY_INFO['propertyIndex'],
        doc_type=config.ELASTICSEARCH_QUERY_INFO['propertyDocType'],
        data=DEFAULT_NI_PROPERTY_DATA[0])
    return (len(DEFAULT_NI_PROPERTY_DATA),
            config.ELASTICSEARCH_QUERY_INFO['propertyIndex'],)

