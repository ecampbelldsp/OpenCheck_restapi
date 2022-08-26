#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on  5/6/22 14:10

@author: Edward L. Campbell Hernández
contact: ecampbelldsp@gmail.com
"""

import requests
import json

code = "Gkn1ANNsFs_xAQw2m9QmdOj0ndwwCKaptn8F0uwdtk4"
payload_token_access = {'client_id': 'live1_212599_hWCSK6qFsz2G5kTdPAxORe7c', 'client_secret': 'QjXqDKRZnpTxehV27I6a8vCS4UJcPYNM', 'redirect_uri':'https://e87c-5-224-24-2.eu.ngrok.io','code':code, 'grant_type':'authorization_code'}

url_access_token = 'https://hotels.cloudbeds.com/api/v1.1/access_token'
# r = requests.post('https://hotels.cloudbeds.com/api/v1.1/access_token',params=payload_token_access)

r = requests.request("POST", url_access_token, data=payload_token_access)

response = json.loads(r.text)
# print(response)


access_token = response['access_token']
refresh_token = response['refresh_token']


payload_property_id = {'property_id': '212599', 'role_details':False, 'access_token':access_token}
url_property_id = "https://hotels.cloudbeds.com/api/v1.1/userinfo"
headers = {
    'Authorization': 'Bearer '+access_token
}

r = requests.request("GET", url_property_id, data=payload_property_id, headers = headers)
response = json.loads(r.text)


#Get hotel details

payload_hotel_details = {'property_id': '212599'}
url_property_id = "https://hotels.cloudbeds.com/api/v1.1/getHotelDetails"
headers = {
    'Authorization': 'Bearer '+access_token
}

r = requests.request("GET", url_property_id, data=payload_hotel_details, headers = headers)
response = json.loads(r.text)