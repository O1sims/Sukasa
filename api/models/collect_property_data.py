from rest_framework import serializers


class CollectPropertyDataModel(serializers.Serializer):
    area = serializers.CharField()
    propertyType = serializers.CharField()
    sortBy = serializers.CharField()
