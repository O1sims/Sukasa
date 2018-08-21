#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 15:43:31 2018

@author: owen
"""



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

    
    
    
import csv

with open('/home/owen/Desktop/AEO-GB.csv', 'wb') as f:  # Just use 'w' mode in 3.x
    w = csv.writer(f, t.keys())
    w.writeheader()
    w.writerow(t)
    

import csv

from collections import namedtuple
Submission = namedtuple('Submission', ['holder', 'issuingCompany', 'competentCustomsAuthority', 'authorisationType', 'effDate'])

with open('/home/owen/Desktop/AEO-GB.csv', 'w') as f:
    w = csv.writer(f)
    w.writerow(['holder', 'issuingCompany', 'competentCustomsAuthority', 'authorisationType', 'effDate']) # we are being naughty here and using a private attribute
    w.writerows(t)

    
    
properties_json = json.dumps(
    obj=t,
    default=json_util.default)
json_file = open('/home/owen/Desktop/AEO-GB.json', 'w')
json_file.write(properties_json)
json_file.close()





