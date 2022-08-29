#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on  18/8/22 17:56

@author: Edward L. Campbell Hernández
contact: ecampbelldsp@gmail.com
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on  5/6/22 14:10

@author: Edward L. Campbell Hernández
contact: ecampbelldsp@gmail.com
"""

import requests
import json

code = "AdCUPSGNnaoo42D-DVRUGDGuwHxH_3P6Ehvpz4XB4C8"
redirect_uri = 'https://6fdb-5-224-24-2.eu.ngrok.io'
payload_token_access = {'client_id': 'live1_212599_hWCSK6qFsz2G5kTdPAxORe7c', 'client_secret': 'QjXqDKRZnpTxehV27I6a8vCS4UJcPYNM', 'redirect_uri':redirect_uri,'code':code, 'grant_type':'authorization_code'}

url_access_token = 'https://hotels.cloudbeds.com/api/v1.1/access_token'
# r = requests.post('https://hotels.cloudbeds.com/api/v1.1/access_token',params=payload_token_access)

r = requests.request("POST", url_access_token, data=payload_token_access)

response = json.loads(r.text)
# print(response)

with open("data/access_token.json", "w") as outfile:
    json.dump(response, outfile)


# access_token = response['access_token']
# refresh_token = response['refresh_token']


# payload_property_id = {'property_id': '212599', 'role_details':False, 'access_token':access_token}
# url_property_id = "https://hotels.cloudbeds.com/api/v1.1/userinfo"
# headers = {
#     'Authorization': 'Bearer '+access_token
# }
#
# r = requests.request("GET", url_property_id, data=payload_property_id, headers = headers)
# response = json.loads(r.text)
#
#
# #Get hotel details
#
# payload_hotel_details = {'property_id': '212599'}
# url_property_id = "https://hotels.cloudbeds.com/api/v1.1/getHotelDetails"
# headers = {
#     'Authorization': 'Bearer '+access_token
# }
#
# r = requests.request("GET", url_property_id, data=payload_hotel_details, headers = headers)
# response = json.loads(r.text)