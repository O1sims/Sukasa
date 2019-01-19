from drf_yasg.utils import swagger_auto_schema

from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import CreateAPIView

from analytics.property_valuation_estimator import predict_property_price
from api.models.property_valuation import PropertyValuationEstimationModel, PropertyValuationDifferentialModel


def myopic_differential(given_price, estimation):
    difference = given_price - estimation
    if difference > 5:
        label = "overvalued"
    elif difference < -5:
        label = "undervalued"
    else:
        label = "correctly valued"
    return {
        "difference": difference,
        "label": label
    }


class PropertyValuationEstimationView(CreateAPIView):
    renderer_classes = (JSONRenderer, )
    serializer_class = PropertyValuationEstimationModel

    @swagger_auto_schema(responses={201: "Created"})
    def post(self, request, *args, **kwargs):
        PropertyValuationEstimationModel(
            data=request.data).is_valid(
            raise_exception=True)
        valuation = predict_property_price(
            property_data=request.data)
        return Response(
            data={"estimatedPrice": valuation},
            status=201)


class PropertyValuationDifferentialView(CreateAPIView):
    renderer_classes = (JSONRenderer, )
    serializer_class = PropertyValuationDifferentialModel

    @swagger_auto_schema(responses={201: "Created"})
    def post(self, request, *args, **kwargs):
        PropertyValuationDifferentialModel(
            data=request.data).is_valid(
            raise_exception=True)
        valuation = predict_property_price(
            property_data=request.data['propertyInfo'])
        differential = myopic_differential(
            given_price=request.data['givenPrice'],
            estimation=valuation)
        return Response(
            data={
                "estimatedPrice": valuation,
                "differential": differential
            },
            status=201)
