from rest_framework import serializers

from api.models.property_data import EPCChartModel, PropertyAmenitiesModel
from api.models.property_valuation import HOUSE_STYLE_CHOICES, HEATING_CHOICES, POSTCODE_CHOICES


class PropertyDetailsEAModel(serializers.Serializer):
    epcChart = EPCChartModel(required=False)
    amenities = PropertyAmenitiesModel(required=False)
    bedrooms = serializers.IntegerField(required=False)
    bathrooms = serializers.IntegerField(required=False)
    receptions = serializers.IntegerField(required=False)
    heating = serializers.ChoiceField(
        choices=HEATING_CHOICES,
        required=False) 


class PropertyDataEAModel(serializers.Serializer):
    address = serializers.CharField(required=False)
    town = serializers.CharField(required=False)
    shortPostcode = serializers.ChoiceField(
        choices=POSTCODE_CHOICES,
        required=False)
    longPostcode = serializers.CharField(required=False)
    aggregateStyle = serializers.ChoiceField(
        choices=HOUSE_STYLE_CHOICES,
        required=False)
    details = PropertyDetailsEAModel()


class EstateAgentRecommenderModel(serializers.Serializer):
    propertyData = PropertyDataEAModel()
