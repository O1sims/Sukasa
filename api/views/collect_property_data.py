from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import CreateAPIView

from api.models.collect_property_data import CollectPropertyDataModel
from analytics.utilities.CollectPropertyData import send_property_dataset


class CollectPropertyDataView(CreateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = CollectPropertyDataModel

    def post(self, request, **kwargs):
        send_property_dataset(
            property_type=request.data['propertyType'],
            area=request.data['area'],
            sort_by=request.data['sortBy'])
        return Response(status=201)
