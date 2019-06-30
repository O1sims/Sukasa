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


class EstateAgentRecommenderView(CreateAPIView):
    renderer_classes = (JSONRenderer, )
    serializer_class = EstateAgentRecommenderModel

    @swagger_auto_schema(responses={200: "Success"})
    def post(self, request, *args, **kwargs):
        EstateAgentRecommenderModel(
            data=request.data).is_valid(
            raise_exception=True)
        master_data = MongoService().get_from_collection(
            collection_name=MONGO_DB_INFO["masterCollection"])
        estateAgentRecommendations = EstateAgentRecommender().find_related_properties(
            master_data= master_data, 
            request_object=request.data)
        # TODO: Re-structure data to price valuation data
        # estateAgentRecommendations["priceEstimate"] = predict_property_price(
        #     property_data=request.data)
        return Response(
            data=estateAgentRecommendations,
            status=200)

