from rest_framework import serializers

from api.models.property_data import HOUSE_STYLE_CHOICES, HEATING_CHOICES, \
    POSTCODE_CHOICES, EPCChartModel, PropertyAmenitiesModel


class PropertyDetailsModel(serializers.Serializer):
    epcChart = EPCChartModel(required=False)
    amenities = PropertyAmenitiesModel(required=False)
    bedrooms = serializers.IntegerField(required=False)
    bathrooms = serializers.IntegerField(required=False)
    receptions = serializers.IntegerField(required=False)
    heating = serializers.ChoiceField(
        choices=HEATING_CHOICES,
        required=False) 


class PropertyDataModel(serializers.Serializer):
    address = serializers.CharField(required=False)
    town = serializers.CharField(required=False)
    shortPostcode = serializers.ChoiceField(
        choices=POSTCODE_CHOICES,
        required=False)
    longPostcode = serializers.CharField(required=False)
    style = serializers.ChoiceField(
        choices=HOUSE_STYLE_CHOICES,
        required=False)
    details = PropertyDetailsModel()


class EstateAgentRecommenderModel(serializers.Serializer):
    propertyData = PropertyDataModel()
