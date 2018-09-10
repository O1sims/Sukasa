#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 15:43:31 2018

@author: owen
"""


import ast
import json
import requests

from bson import json_util
from bs4 import BeautifulSoup



t = []
for page in range(1, 26):
    page_url = 'http://ec.europa.eu/taxation_customs/dds2/eos/certificates.jsp?Lang=en&offset={}&aeoCountry=GB&showRecordsCount=0&certificatesTypes=AEOC&certificatesTypes=AEOF&certificatesTypes=AEOS'.format(
            page)
    request_page = requests.get(url=page_url)
    page_soup = BeautifulSoup(request_page.content, "lxml")
    for row in page_soup.find_all('tr'):
        a = row.find_all('td')
        if len(a) > 4:
            t.append({
                    'holder': a[1].get_text(),
                    'issuingCompany': a[2].get_text(),
                    'competentCustomsAuthority': a[3].get_text(),
                    'authorisationType': a[4].get_text(),
                    'effDate': a[5].get_text()
            })

    
properties_json = json.dumps(
    obj=t,
    default=json_util.default)
json_file = open('/home/owen/Desktop/AEO-GB.json', 'w')
json_file.write(properties_json)
json_file.close()

    
# Fiddle around with R

# Load JSON back up

json_file = open('/home/owen/Desktop/AEO-GB.json', 'r')
b = ast.literal_eval(json_file.read())

business_info_url = "https://www.nibusinessinfo.co.uk/ni-resources/company-data-search?field_description_value=&title={}&field_town_value=&field_postcode_value="

results = []
for company in b:
    holder = b["holder"]
    first_word = holder.partition(" ")[0]
    
    # Make URL request
    page_url = business_info_url.format(first_word)
    request_page = requests.get(
        url=page_url,
        headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"})
    page_soup = BeautifulSoup(request_page.content, "lxml")
    table = page_soup.find("table", {"class", "views-table cols-3"})
    rows = table.find_all("tr")
    results.append({"company": holder, "number": len(rows) - 1})
    

    
    





