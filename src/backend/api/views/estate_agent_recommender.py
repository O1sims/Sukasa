from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import CreateAPIView

from analytics.estate_agent_recommender import EstateAgentRecommender
from analytics.property_valuation_estimator import predict_property_price

from api.services.MongoService import MongoService
from api.models.estate_agent_recommender import EstateAgentRecommenderModel

from sukasa.config import MONGO_DB_INFO



def prepare_property_data(property_data):
    property_data = property_data['propertyData']
    property_data['postcode'] = EstateAgentRecommender().shorten_postcode(
        long_postcode=property_data['postcode'])
    property_data['details']['aggregateStyle'] = property_data['aggregateStyle']
    del(property_data['town'])
    del(property_data['address'])
    del(property_data['aggregateStyle'])
    return property_data


class EstateAgentRecommenderView(CreateAPIView):
    renderer_classes = (JSONRenderer, )
    serializer_class = EstateAgentRecommenderModel

    @swagger_auto_schema(
        responses={
            200: "Success", 
            201: "Created"})
    def post(self, request, *args, **kwargs):
        EstateAgentRecommenderModel(
            data=request.data).is_valid(
            raise_exception=True)
        master_data = MongoService().get_from_collection(
            collection_name=MONGO_DB_INFO["masterCollection"])
        estate_agent_recommendations = EstateAgentRecommender().find_recommended_estate_agent(
            master_data=master_data, 
            request_object=request.data)
        prepared_property_data = prepare_property_data(
            property_data=request.data)
        estate_agent_recommendations['priceExpectation'] = predict_property_price(
            property_data=prepared_property_data)
        return Response(
            data=estate_agent_recommendations,
            status=200)

