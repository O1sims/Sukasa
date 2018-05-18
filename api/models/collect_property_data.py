from rest_framework import serializers


SORTING_CHOICES = (
    "mostPopular",
    "recentlyAdded",
    "recentlyUpdated",
    "priceLowHigh",
    "priceHighLow"
)


class CollectPropertyDataModel(serializers.Serializer):
    area = serializers.CharField()
    propertyType = serializers.CharField()
    sortBy = serializers.ChoiceField(choices=SORTING_CHOICES)
