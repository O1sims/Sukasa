#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 11:06:05 2018

@author: owen
"""

import re
import requests
import datetime

from string import punctuation
from bs4 import BeautifulSoup

from analytics import config
from api.services.ElasticService import ElasticService


def get_property_page(area, page_number, property_type, sort_by):
    type_url = 'forSalePath' if property_type == 'sale' else 'forRentPath'
    url = '{}{}'.format(
        config.BASIC_REQUEST['baseURL'],
        config.BASIC_REQUEST[type_url])
    if area:
        url += '/{}'.format(area)
    if sort_by is not None:
        url += config.BASIC_REQUEST['sortOptions'][sort_by]
    if page_number > 1:
        url += '/page-{}'.format(page_number)
    request_page = requests.get(
        url=url,
        headers={'User-Agent': config.BASIC_REQUEST['userAgent']})
    if request_page.status_code == 200:
        return BeautifulSoup(request_page.content, "lxml")
    else:
        raise ValueError(
            'Page not found: The request received a {} status code'.format(
                request_page.status_code))


def get_final_page_number(first_page_soup):
    raw_page_number = first_page_soup.find("li", {"class", "paging-last"}).get_text()
    clean_page_number = raw_page_number.encode('ascii', 'ignore').strip().replace(',', '')
    return int(clean_page_number)


def get_all_main_images(page_soup):
    property_images = []
    all_images = page_soup.findAll("div", {"class": "propbox-img"})
    for image in all_images:
        string_image = str(image)
        if 'is-no-photo' in string_image:
            property_images.append(None)
        elif 'propbox-time' in string_image or 'openviewing' in string_image:
            property_images.append(
                image.find("img").attrs['data-lazy-src'])
    return property_images


def strip_punctuation(string):
    prep_string = string.replace('-', ' ')
    return ''.join(char for char in prep_string if char not in punctuation)


def clean_price(price):
    if price is None:
        end_price = price
    else:
        raw_price = price.get_text()
        cleaned_price = raw_price.encode('ascii', 'ignore').strip().replace(',', '')
        try:
            end_price = int(cleaned_price)
        except ValueError:
            end_price = cleaned_price
    return end_price


def get_currency(raw_price):
    currencies = {
        '£': 'pound',
        '€': 'euro',
        '$': 'dollar'
    }
    string_price = str(raw_price)
    for c, v in currencies.iteritems():
        if c in string_price:
            return v
    return 'unknown'


def get_price(page_soup):
    offer = page_soup.find("span", {"class": "price-offers"})
    if offer is not None:
        offer = offer.get_text().strip()
    price = page_soup.find("span", {"class": "price-value "})
    min_price = page_soup.find("span", {"class": "price-min"})
    max_price = page_soup.find("span", {"class": "price-max"})
    currency = 'unknown'
    if price is not None:
        currency = get_currency(price)
    elif min_price is not None:
        currency = get_currency(price)
    return {
        'offer': offer,
        'price': clean_price(price),
        'minPrice': clean_price(min_price),
        'maxPrice': clean_price(max_price),
        'currency': currency
    }
    

def get_property_id(html_string, clean_address, id_length=10):
    property_id = ''
    start_string = html_string.find(clean_address)
    for i in range(id_length):
        new_char = html_string[start_string + len(clean_address) + i]
        if new_char is not '"':
            property_id += html_string[start_string + len(clean_address) + i]
        else:
            break
    return property_id


def get_clean_address(address, town):
    trans_address = strip_punctuation(address).lower().replace(' ', '-')
    return str('/{}-{}/'.format(
        trans_address, 
        town.lower()))


def get_hyperlink(page_soup, address, town):
    if town is None or address is None:
        return None

    clean_address = get_clean_address(
        address=address,
        town=town)
    property_id = get_property_id(
        html_string=str(page_soup),
        clean_address=clean_address)
    return clean_address + property_id


def get_address(page_soup):
    raw_address = page_soup.find("span", {"class": "propbox-addr"}).get_text()
    clean_address = str(raw_address.rstrip(', '))
    return clean_address


def get_postcode(page_soup):
    raw_postcode = page_soup.find("span", {"class": "propbox-town"})
    clean_postcode = str(raw_postcode.get_text())
    return clean_postcode


def get_brief(page_soup):
    raw_brief = page_soup.find("p", {"class": "propbox-brief"})
    if raw_brief is None:
        return None
    else:
        clean_brief = str(raw_brief.get_text().strip())
        return clean_brief


def get_estate_agent(page_soup):
    agent = page_soup.find("p", {"class": "propbox-account"})
    agent_data = {'name': None, 'branch': None}
    if agent is not None:
        rep = {
            'Marketed by ': '',
            'Developed by ': ''
        }
        rep = dict((re.escape(k), v) for k, v in rep.iteritems())
        pattern = re.compile("|".join(rep.keys()))
        agent = pattern.sub(
            lambda m: rep[re.escape(m.group(0))],
            agent.get_text().strip())
        if '(' in agent:
            agent_data['name'] = str(agent.split(' (')[0])
            agent_data['branch'] = str(agent[agent.find("(") + 1:agent.find(")")])
        else:
            agent_data['name'] = str(agent)
    return agent_data


def property_location(detail_soup):
    map_data = detail_soup.find('div', {'class': 'prop-map-canvas'}).attrs
    return {
        'latitude': float(map_data['data-lat']),
        'longitude': float(map_data['data-lng'])
    }


def amenity_present(detail_page, amenity):
    return amenity in detail_page.lower()


def parse_epc_rating(epc_rating_list):
    parsed_epc_values = []
    for epc in epc_rating_list:
        match = re.match(
            pattern=r"([a-z]+)([0-9]+)",
            string=epc,
            flags=re.I)
        if match:
            items = match.groups()
            for item in items:
                parsed_epc_values.append(item)
    parsed_epc = {
        'actual': {
            'band': parsed_epc_values[0],
            'rating': int(parsed_epc_values[1])
        },
        'potential': {
            'band': parsed_epc_values[2],
            'rating': int(parsed_epc_values[3])
        }
    }
    return parsed_epc


def get_property_details(hyperlink):
    if hyperlink is None:
        return None

    data = {}
    page_response = requests.get(
        url='{}{}'.format(
            config.BASIC_REQUEST['baseURL'],
            hyperlink),
        headers={'User-Agent': config.BASIC_REQUEST['userAgent']})
    if page_response.status_code == 200:
        detail_page = page_response.content
        detail_soup = BeautifulSoup(detail_page, "lxml")
        key_info_table = detail_soup.find("table", {"id": "key-info-table"})
        key_info_rows = key_info_table.find_all('tr')
        for row in key_info_rows:
            row_title = str(row.findAll('th')[0].get_text().lower())
            if row_title != 'stamp duty' and row_title != 'price':
                cols = row.findAll('td')
                cols = [ele.text.strip() for ele in cols]
                info = [ele for ele in cols if ele][0].encode('ascii', 'ignore').strip()
                if row_title == 'rates':
                    info = float(info.replace(' pa*', '').replace(',', ''))
                elif 'epc' in row_title:
                    info = info.split('\n', 1)[0]
                    info = parse_epc_rating(
                        epc_rating_list=info.split('/'))
                elif row_title in ['bathrooms', 'bedrooms', 'receptions']:
                    info = int(info)
                else:
                    info = str(info)
                data[to_camel_case(string=row_title)] = info
        data['amenities'] = {}
        for amenity in ['garden', 'garage', 'driveway', 'parking', 'bay window']:
            data['amenities'][to_camel_case(string=amenity)] = amenity_present(
                detail_page=detail_page,
                amenity=amenity)
        data['location'] = property_location(
            detail_soup=detail_soup)
        return data
    else:
        return None


def to_camel_case(string):
    humped_camel = ''.join(x for x in string.title() if not x.isspace())
    return humped_camel[0].lower() + humped_camel[1:]


def property_dataset(page_soup):
    dataset = []
    property_details = page_soup.findAll("div", {"class": "propbox-details"})
    property_images = get_all_main_images(page_soup)
    number_of_properties = len(property_details)
    number_of_images = len(property_images)
    if number_of_properties != number_of_images:
        raise ValueError(
            'Mis-match: We collected {} properties and {} images'.format(
                number_of_properties,
                number_of_images))
    for i in range(number_of_properties):
        address = get_address(property_details[i])
        postcode_split = get_postcode(property_details[i]).split()
        if len(postcode_split) > 1:
            town = postcode_split[0]
            postcode = postcode_split[1]
            hyperlink = get_hyperlink(
                page_soup=page_soup,
                address=address,
                town=town)
            property_id = get_property_id(
                html_string=str(page_soup),
                clean_address=get_clean_address(
                    address=address,
                    town=town))
        else:
            town = None
            postcode = None
            hyperlink = None
            property_id = None
        dataset.append({
            'timestamp': datetime.datetime.now(),
            'property_id': property_id,
            'address': address,
            'town': town,
            'postcode': postcode,
            'priceInfo': get_price(property_details[i]),
            'brief': get_brief(property_details[i]),
            'estateAgent': get_estate_agent(property_details[i]),
            'hyperlink': '{}{}'.format(
                config.BASIC_REQUEST['baseURL'],
                hyperlink),
            'details': get_property_details(hyperlink),
            'image': property_images[i]
        })
    return dataset


def get_property_dataset(area, property_type, sort_by,
                         update_only=False):
    first_page = get_property_page(
        area=area,
        page_number=0,
        property_type=property_type,
        sort_by=sort_by)
    final_page_number = get_final_page_number(
        first_page)
    property_data = property_dataset(first_page)
    if not config.DEVELOPMENT:
        for page_number in range(2, final_page_number):
            property_page = get_property_page(
                area=area,
                page_number=page_number,
                property_type=property_type,
                sort_by=sort_by)
            new_property_data = property_dataset(property_page)
            if update_only:
                new_property_ids = []
                for prop in new_property_data:
                    new_property_ids.append(prop['id'])
                count = ElasticService().count_database(
                        index=config.ELASTICSEARCH_QUERY_INFO['propertyIndex'],
                        query_string={"ids": {"values": new_property_ids}})
                if count > 0:
                    break
            property_data += new_property_data
    return property_data


def send_property_dataset(property_type, area=None, sort_by=None):
    property_data = get_property_dataset(
        area=area,
        property_type=property_type,
        sort_by=sort_by)
    ElasticService().save_to_database(
        index=config.ELASTICSEARCH_QUERY_INFO['propertyIndex'],
        doc_type=config.ELASTICSEARCH_QUERY_INFO['propertyDocType'],
        data=property_data)


if __name__ == '__main__':
    properties = get_property_dataset(
        area='belfast',
        property_type='sale',
        sort_by='recentlyAdded')
    print properties
