from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import CreateAPIView

from api.services.ElasticService import ElasticService
from api.models.property_data import GeneratePropertyDataModel, GetPropertyDataModel

import analytics.config as config
from analytics.utilities.CollectPropertyData import send_property_dataset


class GeneratePropertyDataView(CreateAPIView):
    renderer_classes = (JSONRenderer, )
    serializer_class = GeneratePropertyDataModel

    def post(self, request, *args, **kwargs):
        GeneratePropertyDataModel(
            data=request.data).is_valid(
            raise_exception=True)
        send_property_dataset(
            property_type=request.data['propertyType'],
            area=request.data['area'],
            sort_by=request.data['sortBy'])
        return Response(status=201)


class GetPropertyDataView(CreateAPIView):
    renderer_classes = (JSONRenderer, )
    serializer_class = GetPropertyDataModel

    def post(self, request, *args, **kwargs):
        GetPropertyDataModel(
            data=request.data).is_valid(
            raise_exception=True)
        properties = ElasticService().search_database(
            index=config.ELASTICSEARCH_QUERY_INFO['propertyIndex'],
            query_dict=request.data)
        return Response(
            data=properties,
            status=200)
