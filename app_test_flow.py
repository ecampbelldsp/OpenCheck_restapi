#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on  19/8/22 14:17

@author: Edward L. Campbell Hernández
contact: ecampbelldsp@gmail.com
"""

from src.call import Request
from hd.cam import take_picture
import re



property_id = '212599'
client_id = "live1_212599_hWCSK6qFsz2G5kTdPAxORe7c"
redirect_uri = 'https://6fdb-5-224-24-2.eu.ngrok.io'
scope = "write:guest read:guest write:reservation read:reservation"
client_secret = 'QjXqDKRZnpTxehV27I6a8vCS4UJcPYNM'
path_tokens = "data/access_token.json"


code = "ZyVD5vGIlv2m9CJtNEBl3PSIFNfViJaDiMfvOINf7Pw"
state = "fb08f0d2ff44e959fcd83dc20e58a8c0d729cf6f62fe32ab49ecf"

# reservation_id = "4442365621388"
def Hello():
    return "Welcome to my API-restful functionality"

def getReservation(reservation_id):
    request = Request(client_id, client_secret, redirect_uri, code, path_tokens)
    # print(request.get_reservation(reservation_id))
    response = request.get_reservation(reservation_id)

    if response["success"]:

        tmp = str(response["data"]) #str(response["data"])
        response_2 = re.sub("'", '"', tmp)
        # response_2[0]="'"
        # response_2[-1] = "'"
        return response_2#response["data"] #str(response["data"])

        new_response = {"reservationID":"", "guestFirstName":"","guestLastName":"","guestEmail":"",
                        "guestCellPhone":"","guestAddress1":"","guestCity":"","guestCountry":"",
                        "guestState":"","guestZip":"","guestBirthDate":"","guestDocumentType":"",
                        "guestDocumentNumber":"","guestDocumentIssueDate":"","guestDocumentIssuingCountry":"",
                        "guestDocumentExpirationDate":"","roomType":"","startDate":"","endDate": "",
                        "adults": "","children": "","paid": "","balance": "","paidStatus": "","success":""};

    else:
        return "error"


def picture():
    return take_picture()


data = getReservation("4442365621388")

print(1)
# if request.reservation_is_paid(reservation_id):
#     print("Reservation paid")
# else:
#     balance = request.how_much_to_paid(reservation_id)
#     print(f"You need to pay: {balance}")
#     print(request.post_payment(reservation_id, balance, 'credit', 'master'))
#
# print(request.put_reservation(reservation_id, "checked_in"))
