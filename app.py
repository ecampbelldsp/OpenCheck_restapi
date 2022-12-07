#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on  19/8/22 14:17

@author: Edward L. Campbell Hernández & José M. Ramírez
contact: ecampbelldsp@gmail.com & ramirezsanchezjosem@gmail.com
"""

from flask import Flask, render_template, jsonify, request
from src.config import request_guest_and_reservation, request_payment_and_room, property_id
from flask_cors import CORS, cross_origin
from hd.cam import take_picture

app = Flask(__name__)

# app.config['CORS_HEADERS'] = 'Content-Type'

# CORS(app)
CORS(app)


# CORS(app, resources=r'/api/*')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ping')
def ping():
    return jsonify({"success": "True", "message": "pong"})


@app.route('/getReservation')
def get_reservation():
    def post_processing_reservation(json: dict):

        reservation_out = {
            "reservationID": json.get("reservationID"),
            "guestName": json.get("guestName"),
            "guestEmail": json.get("guestEmail"),
            "guestID": "",
            "guestFirstName": "",
            "guestLastName": "",
            "guestCellPhone": "",
            "guestAddress1": "",
            "guestCity": "",
            "guestCountry": "",
            "guestState": "",
            "guestZip": "",
            "guestBirthDate": "",
            "guestDocumentType": "",
            "guestDocumentNumber": "",
            "guestDocumentIssueDate": "",
            "guestDocumentIssuingCountry": "",
            "guestDocumentExpirationDate": "",
            "roomTypeID": [],
            "roomTypeName": [],
            "roomID": [],
            "startDate": [],
            "endDate": [],
            "adults": [],
            "children": [],
            "paid": "",
            "balance": "",
            "paidStatus": "",
        }

        # Guests reservation info
        guests_info = json['guestList']
        for guest_id in guests_info.keys():
            guest_data = guests_info[guest_id]

            if guest_data['guestFirstName'] in reservation_out['guestName'] and \
                    guest_data['guestLastName'] in reservation_out['guestName']:
                reservation_out['guestID'] = guest_data['guestID']
                reservation_out['guestFirstName'] = guest_data['guestFirstName']
                reservation_out['guestLastName'] = guest_data['guestLastName']
                reservation_out['guestGender'] = guest_data['guestGender']
                reservation_out['guestEmail'] = guest_data['guestEmail']
                reservation_out['guestPhone'] = guest_data['guestPhone']
                reservation_out['guestCellPhone'] = guest_data['guestCellPhone']
                reservation_out['guestCountry'] = guest_data['guestCountry']
                reservation_out['guestAddress'] = guest_data['guestAddress']
                reservation_out['guestCity'] = guest_data['guestCity']
                reservation_out['guestZip'] = guest_data['guestZip']
                reservation_out['guestState'] = guest_data['guestState']
                reservation_out['guestBirthdate'] = guest_data['guestBirthdate']
                reservation_out['guestDocumentType'] = guest_data['guestDocumentType']
                reservation_out['guestDocumentNumber'] = guest_data['guestDocumentNumber']
                reservation_out['guestDocumentIssueDate'] = guest_data['guestDocumentIssueDate']
                reservation_out['guestDocumentExpirationDate'] = guest_data['guestDocumentExpirationDate']
                reservation_out['guestDocumentIssuingCountry'] = guest_data['guestDocumentIssuingCountry']

        # Room reservation info
        for room in json['unassigned']:
            # reservation_out['roomID'].append(room.get('roomID'))
            reservation_out['roomID'].append(room.get('roomTypeID'))
            reservation_out['roomTypeName'].append(room.get('roomTypeName'))
            # reservation_out['roomID'].append(room.get('roomID'))
            reservation_out['startDate'].append(room.get('dailyRates')[0]['date'])  # room.get('startDate')
            reservation_out['endDate'].append(room.get('dailyRates')[-1]['date'])
            reservation_out['adults'].append(room.get('adults'))
            reservation_out['children'].append(room.get('children'))

        for room in json['assigned']:
            # reservation_out['roomID'].append(room.get('roomID'))
            reservation_out['roomID'].append(room.get('roomTypeID'))
            reservation_out['roomTypeName'].append(room.get('roomTypeName'))
            # reservation_out['roomID'].append(room.get('roomID'))
            reservation_out['startDate'].append(room.get('dailyRates')[0]['date'])
            reservation_out['endDate'].append(room.get('dailyRates')[-1]['date'])
            reservation_out['adults'].append(room.get('adults'))
            reservation_out['children'].append(room.get('children'))

        # Pre-processing stage for Frontend
        for key in reservation_out.keys():
            data = reservation_out[key]
            if isinstance(data, list):
                # data = ['' for d in data if d is None]
                data_set = set(data)
                reservation_out[key] = " _ ".join(data_set)

        # Invoice reservation info
        total = json['balanceDetailed']['grandTotal']
        paid = json['balanceDetailed']['paid']
        balance = float(total) - float(paid)

        reservation_out["paid"] = paid
        reservation_out["total"] = total
        reservation_out["balance"] = "0" if balance < 0 else f"{balance}"

        reservation_out["paidStatus"] = "false" if balance > 0 else "true"

        return {"success": "true", "data": reservation_out}

    reservation_id = request.args.get('reservationID', None)
    response_in_json = request_guest_and_reservation.get_reservation(reservation_id)

    open_check_reservation = post_processing_reservation(response_in_json['data'])
    return open_check_reservation


@app.route('/putReservation', methods=['PUT'])
def put_reservation():
    reservation_id = request.args.get('reservationID', None)
    status = request.args.get('status', None)
    return request_guest_and_reservation.put_reservation(reservation_id, status)


@app.route('/postReservation', methods=['POST'])
def post_reservation():
    data = request.get_json()
    guest_info = data.get('guestInfo')
    room = data.get('room')

    guest_info.update({'propertyID': property_id, 'paymentMethod': 'card'})
    room_info = {'rooms': [{"roomTypeID": room.get('roomTypeID'), "roomRateID": room.get('roomRateID'), "quantity": 1}]}
    adults = {'adults': [{"roomTypeID": room.get('roomTypeID'), "quantity": guest_info.get('adults'), "roomID": ""}]}
    children = {'children': [{"roomTypeID": room.get('roomTypeID'), "quantity": guest_info.get('children'),
                              "roomID": ""}]}

    guest_info.update(room_info)
    guest_info.update(adults)
    guest_info.update(children)

    return request_guest_and_reservation.post_reservation(guest_info)


@app.route('/getReservationInvoiceInformation')
def get_reservation_invoice_information():
    reservation_id = request.args.get('reservationID', None)
    return request_guest_and_reservation.get_reservation_invoice_information(reservation_id)


@app.route('/getGuestsInformation')
def get_guests_info():
    reservation_id = request.args.get('reservationID', None)
    return request_guest_and_reservation.get_guest_info_in_reservation(reservation_id)


@app.route('/getNumberOfGuests')
def how_many_guests():
    reservation_id = request.args.get('reservationID', None)
    return request_guest_and_reservation.get_number_of_guests(reservation_id)


@app.route('/getAvailableRooms')
def get_available_rooms():
    start_date = request.args.get('startDate', None)
    end_date = request.args.get('endDate', None)

    rooms = request.args.get('rooms', 1)
    adults = request.args.get('adults', None)
    children = request.args.get('children', None)

    return request_payment_and_room.get_available_room_types(start_date, end_date, rooms, adults, children)


@app.route('/postGuestDocument')
def post_guest_document():
    guest_id = request.args.get('guestID', None)
    path_to_document = request.args.get('pathDocument', None)
    return request_guest_and_reservation.post_guest_document(guest_id, path_to_document)


@app.route('/postReservationDocument')
def post_reservation_document():
    reservation_id = request.args.get('reservationID', None)
    path_to_document = request.args.get('pathDocument', None)
    return request_guest_and_reservation.post_guest_document(reservation_id, path_to_document)


@app.route('/reservationIsPaid')
def reservation_is_paid():
    reservation_id = request.args.get('reservationID', None)
    return request_guest_and_reservation.reservation_is_paid(reservation_id)


@app.route('/postPayment')
def post_payment():
    reservation_id = request.args.get('reservationID', None)
    amount = request.args.get('amount', None)
    payment_type = request.args.get('type', 'card')
    card_type: str = request.args.get('cardType', None)

    return request_payment_and_room.post_payment(reservation_id, amount, payment_type, card_type)


@app.route("/cam")
def picture():
    flag = take_picture()
    return flag


if __name__ == '__main__':
    # Flask app
    app.run(debug=True)
