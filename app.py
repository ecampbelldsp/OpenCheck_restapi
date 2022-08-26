#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on  19/8/22 14:17

@author: Edward L. Campbell Hernández
contact: ecampbelldsp@gmail.com
"""

from src.call import Request
from flask import Flask

from hd.cam import take_picture

app = Flask(__name__)






property_id = '212599'
client_id = "live1_212599_hWCSK6qFsz2G5kTdPAxORe7c"
redirect_uri = "https://3cdd-5-224-24-2.eu.ngrok.io"
scope = "write:guest read:guest write:reservation read:reservation"
client_secret = 'QjXqDKRZnpTxehV27I6a8vCS4UJcPYNM'
path_tokens = "data/tokens.json"


code = "B4y9y-324-spCnTq-sYobT8OGN_PV5YDYaWBXsUt7BY"
state = "fb08f0d2ff44e959fcd83dc20e58a8c0d729cf6f62fe32ab49ecf"

# reservation_id = "3468462393326"
@app.route("/")
def Hello():
    return "Welcome to my API-restful functionality"

@app.route("/getReservation/<reservation_id>")
def getReservation(reservation_id):
    request = Request(client_id, client_secret, redirect_uri, code, path_tokens)
    # print(request.get_reservation(reservation_id))
    response = request.get_reservation(reservation_id)

    if response["success"]:
        return str(response["data"])
    else:
        return "error"


@app.route("/cam")
def picture():
    return take_picture()


# if request.reservation_is_paid(reservation_id):
#     print("Reservation paid")
# else:
#     balance = request.how_much_to_paid(reservation_id)
#     print(f"You need to pay: {balance}")
#     print(request.post_payment(reservation_id, balance, 'credit', 'master'))
#
# print(request.put_reservation(reservation_id, "checked_in"))
