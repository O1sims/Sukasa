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


class CollectPropertyDataModel(serializers.Serializer):
    area = serializers.CharField()
    propertyType = serializers.ChoiceField(choices=PROPERTY_TYPE_CHOICES)
    sortBy = serializers.ChoiceField(choices=SORTING_CHOICES)
