from rest_framework import serializers


HOUSE_STYLE_CHOICES = (
    "apartment",
    "bungalow",
    "detached",
    "end-terrace",
    "semi-detached",
    "terrace",
    "townhouse"
)

HEATING_CHOICES = (
    "economy 7",
    "gas",
    "oil"
)

SORTING_CHOICES = (
    "recentlyAdded",
    "mostPopular",
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


class PropertyLocationModel(serializers.Serializer):
    lat = serializers.FloatField(required=False)
    lon = serializers.FloatField(required=False)


class BandScoreModel(serializers.Serializer):
    band = serializers.CharField(required=False)
    score = serializers.IntegerField(required=False)


class EPCChartModel(serializers.Serializer):
    actual = BandScoreModel(required=False)
    potential = BandScoreModel(required=False)


class PropertyAmenitiesModel(serializers.Serializer):
    garage = serializers.BooleanField(required=False)
    parking = serializers.BooleanField(required=False)
    garden = serializers.BooleanField(required=False)
    driveway = serializers.BooleanField(required=False)
    bayWindow = serializers.BooleanField(required=False)


class PropertyDetailModel(serializers.Serializer):
    style = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    bedrooms = serializers.IntegerField(required=False)
    bathrooms = serializers.IntegerField(required=False)
    receptions = serializers.IntegerField(required=False)
    rates = serializers.FloatField(required=False)
    typicalMortgage = serializers.CharField(required=False)
    location = PropertyLocationModel(required=False)
    amenities = PropertyAmenitiesModel(required=False)
    heating = serializers.ChoiceField(
        choices=HEATING_CHOICES, 
        required=False)
    keyInformation = serializers.CharField(required=False)
    epcChart = EPCChartModel(required=False)
    propertyImages = serializers.ListField(required=False)
    longPostcode = serializers.CharField(required=False)
    aggregateStyle = serializers.ChoiceField(
        choices=HOUSE_STYLE_CHOICES,
        required=False)


class EstateAgentModel(serializers.Serializer):
    branch = serializers.CharField(required=False)
    name = serializers.CharField(required=False)


class PriceModel(serializers.Serializer):
    price = serializers.IntegerField(required=False)
    timestamp = serializers.DateTimeField(required=False)

class PriceInformationModel(serializers.Serializer):
    maxPrice = serializers.ListField(required=False)
    minPrice = serializers.ListField(required=False)
    currency = serializers.CharField(required=False)
    price = PriceModel(many=True, required=False)
    offer = serializers.CharField(required=False)

class StatusModel(serializers.Serializer):
    status = serializers.CharField(required=False)
    timestamp = serializers.DateTimeField(required=False)

class PropertyImageModel(serializers.Serializer):
    propertyImage = serializers.ImageField(required=False)

class PropertyDataModel(serializers.Serializer):
    status = StatusModel(many=True, required=False)
    timeAdded = serializers.DateTimeField(required=False)
    lastUpdated = serializers.DateTimeField(required=False)
    propertyId = serializers.CharField(required=False)
    tags = serializers.ListField(required=False) 
    address = serializers.CharField(required=False)
    town = serializers.CharField(required=False)
    area = serializers.CharField(required=False)
    image = serializers.CharField(required=False)
    postcode = serializers.CharField(required=False)
    priceInfo = PriceInformationModel(required=False)
    brief = serializers.CharField(required=False)
    estateAgent = EstateAgentModel(required=False)
    hyperlink = serializers.CharField(required=False)
    details = PropertyDetailModel(required=False)
    owner = serializers.CharField(required=False)
