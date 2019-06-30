import os
import re
import json

from collections import Counter
from geopy.geocoders import Nominatim

from math import sin, cos, sqrt, atan2, radians



EARTH_RADIUS_KM = 6373.0

GEOLOCATOR = Nominatim(
    user_agent="specify_your_app_name_here")


class EstateAgentRecommender():
    def __init__():
        pass

    def calculate_time_to_agree(self, master_data):
        for property in master_data:
            if int(property['timeAdded']['$date']/1000) > 1554761377 and property['status'][-1]['status'].lower() == "sale agreed":
                time_taken = int(
                    property['status'][-1]['timestamp']['$date']/1000) - int(
                        property['timeAdded']['$date']/1000)
                if time_taken > 0:
                    property['timeToAgree'] = time_taken
                else:
                    property['timeToAgree'] = None
            else:
                property['timeToAgree'] = None
        return master_data


    def shorten_postcode(self, long_postcode):
        """
        Find first 
        Examples: ["BT18 0HZ", "BT57JH", "BT473XY"]
        """
        long_postcode_ws = re.sub(
            pattern=" ", 
            repl="", 
            string=long_postcode)
        if len(long_postcode_ws) > 6:
            short_postcode = long_postcode_ws[:4]
        elif len(long_postcode_ws) <= 6:
            short_postcode = long_postcode_ws[:3]
        return short_postcode


    def calculate_distance(self, property_coordinates, coordinates_to):
        if property_coordinates is not None:
            lat1 = radians(property_coordinates.latitude)
            lon1 = radians(property_coordinates.longitude)
            lat2 = radians(coordinates_to['lat'])
            lon2 = radians(coordinates_to['lon'])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            return round(EARTH_RADIUS_KM * c, 2)
        else:
            return None


    def calculate_similarity_index(self, request_object, related_properties):
        full_address = "{}, {}, Northern Ireland".format(
            request_object['propertyData']['address'], 
            request_object['propertyData']['town'])
        property_coordinates = GEOLOCATOR.geocode(
            query=full_address,
            country_codes="GB")
        request_amenities = request_object['propertyData']['details']['amenities']
        amenity_keys = list(request_amenities.keys())
        for property in related_properties:
            amenity_similarity = 0
            if property['details'] is None:
                property['similarityIndex'] = amenity_similarity
            else:
                property_amenities = property['details']['amenities']
                for a in amenity_keys:
                    if request_amenities[a] == property_amenities[a]:
                        amenity_similarity += 1
                geo_distance = self.calculate_distance(
                    property_coordinates=property_coordinates, 
                    coordinates_to=property['details']['location'])
                if geo_distance is None:
                    amenity_similarity += 0
                elif geo_distance < 1:
                    amenity_similarity += 5
                elif geo_distance < 5:
                    amenity_similarity += 3
                elif geo_distance < 10:
                    amenity_similarity += 1
                if 'heating' in property['details'].keys():
                    if property['details']['heating'] == request_object['propertyData']['details']['heating']:
                        amenity_similarity += 3
                if property['details']['longPostcode'] == request_object['propertyData']['postcode']:
                    amenity_similarity += 3
                property['similarityIndex'] = amenity_similarity/16
        return related_properties


    def find_related_properties(self, master_data, request_object):
        """
        Find all related properties either agreed or for sale.
        """
        related_properties = []
        short_postcode = self.shorten_postcode(
            long_postcode=request_object['propertyData']['postcode'])
        for property in master_data:
            if property['details'] is not None and \
                'bedrooms' in property['details'] and \
                'aggregateStyle' in property['details'] and \
                property['postcode'] is not None:
                if property['details']['bedrooms'] == request_object['propertyData']['details']['bedrooms'] and \
                    property['details']['aggregateStyle'] == request_object['propertyData']['aggregateStyle'] and \
                    property['postcode'] == short_postcode:
                    related_properties.append(property)
        related_properties = self.calculate_similarity_index(
            request_object=request_object,
            related_properties=related_properties)
        return sorted(
            related_properties, 
            key=lambda k: -k['similarityIndex'])


    def recommended_estate_agent(self, request_object, related_properties):
        """
        Estate agent recommendation based on three aspects: price changes, time, and experience.
        """
        # How many agreements
        agreed_properties = list(filter(
            lambda x: x['status'][-1]['status'].lower() == "sale agreed", 
            related_properties))
        estate_agents = [property['estateAgent']['name'] for property in agreed_properties]
        estate_agents = dict(Counter(estate_agents))
        
        # Calculate recommended agent as a function of: 
        # (a) price changes;
        # (b) time taken to agree; and
        # (c) number of properties agreed
        recommended_agents = []
        price_drop = {}; time_taken = {}
        for agent in estate_agents.keys():
            agreed_properties_ea = list(filter(
                lambda x: x['estateAgent']['name'] == agent,
                agreed_properties))
            timings = []
            price_changes = []
            for property in agreed_properties_ea:
                price_changes.append(
                    (property['priceInfo']['price'][-1]['price'] - 
                    property['priceInfo']['price'][0]['price']) / 
                    property['priceInfo']['price'][0]['price'])
                timings.append(
                    int(property['status'][-1]['timestamp']['$date'] / 1000) - 
                    int(property['status'][0]['timestamp']['$date'] / 1000))
            price_drop[agent] = sum(price_changes) / len(price_changes)
            time_taken[agent] = (sum(timings) / len(timings)) / (60 * 60 * 24)
            score = 2 + (estate_agents[agent]/sum(estate_agents.values()) -
                price_drop[agent]/(max(sum(price_drop.values()), 1)) -
                time_taken[agent]/(max(sum(time_taken.values()), 1)))
            recommended_agents.append({
                'name': agent, 
                'score': score})
        return sorted(
            recommended_agents, 
            key=lambda k: -k['score'])


        def find_recommended_estate_agent(master_data, request_object):
            """
            Construct the recommended agents model
            """
            related_properties = self.find_related_properties(
                master_data=master_data,
                request_object=request_object)
            recommended_agents = self.recommended_estate_agent(
                request_object=request_object,
                related_properties=related_properties)
            return {
                "relatedProperties": related_properties,
                "recommendedAgents": recommended_agents
            }
