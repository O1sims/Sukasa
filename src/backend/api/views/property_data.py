from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from api.services.MongoService import MongoService
from api.models.property_data import GeneratePropertyDataModel, PropertyDataModel

from sukasa.config import MONGO_DB_INFO


SEARCH_Q = openapi.Parameter(
    name='q',
    in_=openapi.IN_QUERY,
    description='A string of search keywords',
    type=openapi.TYPE_STRING,
    required=True)

def generate_brief(property_data):
    return "{} bed {} for sale".format(
        property_data['details']['bedrooms'],
        property_data['details']['style']
    )

def generate_tags(property_data):
    return [
        property_data['address'].lower(),
        property_data['postcode'].lower(),
        property_data['town'].lower()
    ]

class PropertyDataView(ListCreateAPIView):
    renderer_classes = (JSONRenderer, )
    serializer_class = PropertyDataModel

    @swagger_auto_schema(manual_parameters=[SEARCH_Q])
    def get(self, request, *args, **kwargs):
        search_query = self.request.GET.get('q', None)
        if search_query is None:
            raise ValueError(
                'Please provide some search query with the `q` query parameter')
        properties = MongoService().search_collection(
            collection_name=MONGO_DB_INFO['propertyCollection'],
            search_string=search_query.lower())
        return Response(
            data=properties,
            status=200)

    @swagger_auto_schema(responses={201: "Created"})
    def post(self, request, *args, **kwargs):
        PropertyDataModel(
            data=request.data).is_valid(
            raise_exception=True)
        request.data['brief'] = generate_brief(
            property_data=request.data)
        request.data['tags'] = generate_tags(
            property_data=request.data)
        MongoService().insert_to_collection(
            collection_name=MONGO_DB_INFO['propertyCollection'],
            data=request.data)
        return Response(status=201)


class PropertyDataIdView(RetrieveUpdateDestroyAPIView):
    renderer_classes = (JSONRenderer, )
    serializer_class = PropertyDataModel

    def get(self, request, *args, **kwargs):
        property = MongoService().get_from_collection(
            collection_name=MONGO_DB_INFO['propertyCollection'],
            property_id=self.kwargs['propertyId'])
        return Response(
            data=property,
            status=200)

    # TODO: Add delete property by ID
    def delete(self, request, *args, **kwargs):
        return Response(status=204)
