#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 12:51:12 2018

@author: owen
"""


import json
import requests

from analytics import config


def get_all_schools(location, radius=5000, place_type='school'):
    schools_response = requests.get(
        url=config.GOOGLE_MAPS_CONFIG['PLACE_RADAR_URL'].format(
            location['latitude'],
            location['longitude'],
            radius,
            place_type,
            config.GOOGLE_MAPS_CONFIG['apiKey'])).content
    all_schools = json.loads(schools_response)['results']
    
    for school in all_schools:
        place_desc = requests.get(
            url=config.GOOGLE_MAPS_CONFIG['PLACE_DETAIL_URL'].format(
                school['place_id'],
                config.GOOGLE_MAPS_CONFIG['apiKey'])).content
        school['placeData'] = json.loads(place_desc)['result']
    return all_schools
