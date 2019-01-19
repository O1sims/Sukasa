from rest_framework.response import Response
from rest_framework.generics import DestroyAPIView

from api.services.MongoService import MongoService

from utils.data_loader import insert_default_property_data


class ResetDatabase(DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        MongoService().drop_database()
        insert_default_property_data()
        return Response(status=204)
