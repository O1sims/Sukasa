from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from api.services.ElasticService import ElasticService
from api.models.property_data import GeneratePropertyDataModel, PropertyDataModel

import analytics.config as config
from analytics.utilities.CollectPropertyData import send_property_dataset


SEARCH_Q = openapi.Parameter(
    name='q',
    in_=openapi.IN_QUERY,
    description='A string of search keywords',
    type=openapi.TYPE_STRING,
    required=True)


class GeneratePropertyDataView(CreateAPIView):
    renderer_classes = (JSONRenderer, )
    serializer_class = GeneratePropertyDataModel

    @swagger_auto_schema(responses={201: "Created"})
    def post(self, request, *args, **kwargs):
        GeneratePropertyDataModel(
            data=request.data).is_valid(
            raise_exception=True)
        sent_properties = send_property_dataset(
            property_type=request.data['propertyType'],
            area=request.data['area'],
            sort_by=request.data['sortBy'])
        return Response(
            data={'report': 'Created {} properties'.format(
                sent_properties)},
            status=201)


class PropertyDataView(ListCreateAPIView):
    renderer_classes = (JSONRenderer, )
    serializer_class = PropertyDataModel

    @swagger_auto_schema(manual_parameters=[SEARCH_Q])
    def get(self, request, *args, **kwargs):
        search_query = self.request.GET.get('q', None)
        if search_query is None:
            raise ValueError(
                'Please provide some search query with the `q` query parameter')
        properties = ElasticService().search_database(
            index=config.ELASTICSEARCH_QUERY_INFO['propertyIndex'],
            query_dict={'tags': search_query.lower()})
        return Response(
            data=properties,
            status=200)

    @swagger_auto_schema(responses={201: "Created"})
    def post(self, request, *args, **kwargs):
        PropertyDataModel(
            data=request.data).is_valid(
            raise_exception=True)
        properties = ElasticService().save_to_database(
            index=config.ELASTICSEARCH_QUERY_INFO['propertyIndex'],
            doc_type=config.ELASTICSEARCH_QUERY_INFO['propertyDocType'],
            data=request.data)
        return Response(
            data=properties,
            status=200)


class PropertyIdView(RetrieveUpdateDestroyAPIView):
    renderer_classes = (JSONRenderer, )
    serializer_class = PropertyDataModel

    def get(self, request, *args, **kwargs):
        properties = ElasticService().search_database(
            index=config.ELASTICSEARCH_QUERY_INFO['propertyIndex'],
            query_dict={'_id': self.kwargs['property_id']})
        return Response(
            data=properties,
            status=200)

    def delete(self, request, *args, **kwargs):
        delete_property = ElasticService().delete_document(
            index=config.ELASTICSEARCH_QUERY_INFO['propertyIndex'],
            doc_type=config.ELASTICSEARCH_QUERY_INFO['propertyDocType'],
            elastic_id=self.kwargs['property_id'])
        return Response(status=204)
