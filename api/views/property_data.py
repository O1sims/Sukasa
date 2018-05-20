from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import CreateAPIView

from api.models.property_data import CollectPropertyDataModel, GetPropertyDataModel
from analytics.utilities.CollectPropertyData import send_property_dataset


class CollectPropertyDataView(CreateAPIView):
    renderer_classes = (JSONRenderer, )
    serializer_class = CollectPropertyDataModel

    def post(self, request, *args, **kwargs):
        CollectPropertyDataModel(
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
        return Response(status=200)
