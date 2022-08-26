#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on  18/8/22 18:07

@author: Edward L. Campbell Hernández
contact: ecampbelldsp@gmail.com
"""
import json
import requests

with open('data/access_token.json', 'r') as openfile:
    # Reading from json file
    json_object = json.load(openfile)

access_token = json_object['access_token']
refresh_token = json_object['refresh_token']


#Get reservation info
payload_hotel_details = {'property_id': '212599', 'reservationID' : '3468462393326'}
url_property_id = "https://hotels.cloudbeds.com/api/v1.1/getReservation"
headers = {
    'Authorization': 'Bearer '+access_token
    # 'Scope': 'read:reservation'
}

r = requests.request("GET", url_property_id, data=payload_hotel_details, headers = headers)
response = json.loads(r.text)

print(response)
