import os


GOOGLE_MAPS_CONFIG = {
    "apiKey": "AIzaSyD9u_sCT0qvnGSHGlIHQIiv-sXesIH4b_8",
    "PLACE_RADAR_URL": "https://maps.googleapis.com/maps/api/place/radarsearch/json?location={},{}&radius={}&type={}&key={}",
    "PLACE_DETAIL_URL": "https://maps.googleapis.com/maps/api/place/details/json?placeid={}&key={}"
}

BASIC_REQUEST = {
    "baseURL": "https://www.propertypal.com",
    "forSalePath": "/property-for-sale",
    "forRentPath": "/property-to-rent",
    "sortOptions": {
        "mostPopular": "/sort-hot",
        "recentlyAdded": "/sort-dateHigh",
        "recentlyUpdated": "/sort-updatedHigh",
        "priceLowHigh": "/sort-priceLow",
        "priceHighLow": "/sort-priceHigh"
    },
    "userAgent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0"
}

GEOGRAPHY = {
    "belfast": {
        "coordinates": {
            "latitude": 54.602530,
            "longitude": -5.905154
        }
    },
    "holywood": {
        "coordinates": {
            "latitude": 54.639586,
            "longitude": -5.828433
        }
    }
}

ELASTICSEARCH_QUERY_INFO = {
    "propertyIndex": "properties",
    "propertyDocType": "house"
}

DEPENDENT_VARIABLES = [
    'priceInfo.price'
]

INDEPENDENT_VARIABLES = [
    'postcode',
    'details.bedrooms',
    'details.style',
    'details.heating',
    'details.amenities.bayWindow',
    'details.amenities.driveway',
    'details.amenities.garage',
    'details.amenities.garden'
]
