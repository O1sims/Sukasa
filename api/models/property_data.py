from rest_framework import serializers


SORTING_CHOICES = (
    "mostPopular",
    "recentlyAdded",
    "recentlyUpdated",
    "priceLowHigh",
    "priceHighLow"
)

PROPERTY_TYPE_CHOICES = (
    'sale',
    'rent'
)


class GeneratePropertyDataModel(serializers.Serializer):
    area = serializers.CharField()
    propertyType = serializers.ChoiceField(choices=PROPERTY_TYPE_CHOICES)
    sortBy = serializers.ChoiceField(choices=SORTING_CHOICES)


class PropertyDetailModel(serializers.Serializer):
    bedrooms = serializers.IntegerField(required=False)
    bathrooms = serializers.IntegerField(required=False)
    garage = serializers.BooleanField(required=False)


class GetPropertyDataModel(serializers.Serializer):
    _id = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    area = serializers.CharField(required=False)
    postcode = serializers.CharField(required=False)
    details = PropertyDetailModel(required=False)
