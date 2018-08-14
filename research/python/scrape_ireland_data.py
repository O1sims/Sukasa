#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 16:36:25 2018

@author: owen
"""

import re
import json
import requests
import datetime

from bson import json_util
from bs4 import BeautifulSoup


SEARCH_AREA = ""

DIR_PATH = '/home/owen/Code/PropertyData/src/data'

BASIC_REQUEST = {
    "baseURL": "https://www.daft.ie",
    "forSalePath": "/property-for-sale",
    "forRentPath": "/property-to-rent",
    "sortOptions": {
        "recentlyAdded": "/?s%5Bsort_by%5D=date&s%5Bsort_type%5D=d"
    },
    "userAgent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0"
}
    

IRELAND_COUNTIES = [
    'Antrim',
    'Armagh',
    'Carlow',
    'Cavan',
    'Clare',
    'Cork',
    'Derry',
    'Donegal',
    'Dublin',
    'Fermanagh',
    'Galway',
    'Kerry',
    'Kildare',
    'Kilkenny',
    'Laois',
    'Leitrim',
    'Limerick',
    'Longford',
    'Louth',
    'Mayo',
    'Meath',
    'Monaghan',
    'Offaly',
    'Roscommon',
    'Sligo',
    'Tipperary',
    'Tyrone',
    'Waterford',
    'Westmeath',
    'Wexford',
    'Wicklow'
]
    
    
def get_number_of_properties(first_page):
    section_text = first_page.find('div', {'class': 'section'}).get_text()
    clean_section_text = re.sub(',', '', section_text)
    listings_number = re.findall(r'\d+', clean_section_text)
    return int(listings_number[0])
    
    
def get_property_page(area, offset, property_type, sort_by):
    type_url = 'forSalePath' if property_type == 'sale' else 'forRentPath'
    url = '{}{}'.format(
        BASIC_REQUEST['baseURL'] + '/ireland',
        BASIC_REQUEST[type_url])
    if area:
        url += '/{}'.format(area)
    if sort_by is not None:
        url += BASIC_REQUEST['sortOptions'][sort_by]
    if offset > 1:
        url += '&offset={}'.format(offset)
    request_page = requests.get(
        url=url,
        headers={'User-Agent': BASIC_REQUEST['userAgent']})
    if request_page.status_code == 200:
        return BeautifulSoup(request_page.content, "lxml")
    else:
        raise ValueError(
            'Page not found: The request received a {} status code'.format(
                request_page.status_code))


def get_all_search_images(page_soup):
    property_images = []
    all_images = page_soup.findAll("img", {"class": "main_photo"})
    for image in all_images:
        if 'data-original' in image.attrs.keys():
            image_url = image.attrs['data-original']
        else:
            image_url = None
        property_images.append(image_url)
    return property_images


def get_county(address):
    for county in IRELAND_COUNTIES:
        if county in address:
            return county
    return None


def get_property_id(search_result):
    image_box = search_result.find("div", {"class": "image"})
    image = image_box.find("img")
    if 'id' in image.attrs.keys():
        property_id = image.attrs['id']
    else:
        property_id = None
    return property_id


def get_address(search_result):
    raw_address = search_result.find("div", {"class": "search_result_title_box"}).get_text()
    part_address = raw_address.split(". \n\n            ", 1)[1]
    address = part_address.split("            -", 1)[0]
    return address


def get_price(search_result):
    raw_price = search_result.find("strong", {"class": "price"}).get_text()
    clean_price = raw_price.encode('ascii', 'ignore').strip().replace(',', '')
    return clean_price


def get_hyperlink(search_result):
    raw_result = search_result.find("div", {"class": "search_result_title_box"})
    hyperlink = raw_result.find('a').attrs['href']
    return hyperlink


def property_dataset(page_soup):
    dataset = []
    property_list = page_soup.findAll("div", {"class": "box"})
    property_images = get_all_search_images(page_soup)
    number_of_properties = len(property_list)
    number_of_images = len(property_images)
    if number_of_properties != number_of_images:
        raise ValueError(
            'Mis-match: We collected {} properties and {} images'.format(
                number_of_properties,
                number_of_images))
    for i in range(number_of_properties):
        address = get_address(
            search_result=property_list[i])
        county = get_county(
            address=address)
        hyperlink = get_hyperlink(
            search_result=property_list[i])
        property_id = get_property_id(
                search_result=property_list[i])
        dataset.append({
            'timeAdded': datetime.datetime.now(),
            'propertyId': property_id,
            'hyperlink': BASIC_REQUEST['baseURL'] + hyperlink,
            'address': address,
            'price': get_price(
                search_result=property_list[i]),
            'county': county
        })
    return dataset
    

def scrape_ireland_dataset(area, property_type, sort_by, 
                     page_limit=False, first_only=False):
    first_page = get_property_page(
        area=area,
        offset=0,
        property_type=property_type,
        sort_by=sort_by)
    if first_only:
        final_page_number = 20
    elif page_limit:
        final_page_number = 300
    else:
        final_page_number = get_number_of_properties(
            first_page=first_page)
    print('Parsing page 1 of {}...'.format(final_page_number/20))
    property_data = property_dataset(first_page)
    for offset in range(20, final_page_number, 20):
        try:
            print('Parsing page {} of {}...'.format(
                offset/20, final_page_number/20))
            property_page = get_property_page(
                    area=area,
                    offset=offset,
                    property_type=property_type,
                    sort_by=sort_by)
            property_data += property_dataset(property_page)
        except ValueError:
            print("Oops! Some parsing went wrong in page {}".format(
                    offset/20))
    return property_data


property_data = scrape_ireland_dataset(
        area='',
        property_type='sale',
        sort_by='recentlyAdded')
properties_json = json.dumps(property_data, default=json_util.default)
json_file = open(DIR_PATH + '/IrishPropertyData.json', 'w')
json_file.write(properties_json)
json_file.close()
