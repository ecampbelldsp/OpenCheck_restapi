#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on  19/8/22 14:17

@author: Edward L. Campbell Hernández & José M. Ramírez
contact: ecampbelldsp@gmail.com & ramirezsanchezjosem@gmail.com
"""
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

from datetime import datetime
from hd.cam import take_picture
from src.config import request_guest_and_reservation, request_payment_and_room

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ping')
def ping():
    return jsonify({"success": "True", "message": "pong"})


@app.route('/getReservation')
def get_reservation():
    """
    Get the reservation information. It is necessary a reservation_id.
    :return: a json with the reservation information.
    """

    reservation_id = request.args.get('reservationID', None)
    if reservation_id is None:
        return jsonify({"success": "false", "message": "Missing the reservation identifier."})
    else:
        return jsonify({"data":
                            {"adults": "1",
                             "balance": "1125.0",
                             "children": "0",
                             "endDate": "05-10-2022",
                             "guestAddress": "Rue da Torre 1",
                             "guestAddress1": "Rue da Torre 1, Piso 1ro, Puerta 1",
                             "guestBirthDate": "17-12-1990",
                             "guestCellPhone": "+346854589",
                             "guestCity": "Vigo",
                             "guestCountry": "ES",
                             "guestDocumentExpirationDate": "1-01-2029",
                             "guestDocumentIssueDate": "1-01-2019",
                             "guestDocumentIssuingCountry": "ES",
                             "guestDocumentNumber": "K81231",
                             "guestDocumentType": "Passport",
                             "guestEmail": "eduardog90@gmail.com",
                             "guestFirstName": "Eduardo",
                             "guestGender": "M",
                             "guestID": "58817062",
                             "guestLastName": "García",
                             "guestName": "Eduardo García",
                             "guestPhone": "+346854589",
                             "guestState": "Pontevedra",
                             "guestZip": "36001",
                             "paid": "0",
                             "paidStatus": "false",
                             "reservationID": "4442365621388",
                             "roomID": "409037",
                             "roomTypeID": "",
                             "roomTypeName": "Deluxe King",
                             "startDate": "01-10-2022",
                             "total": "1125"
                             },
                        "success": "true"})


@app.route('/putReservation', methods=['PUT'])
def put_reservation():
    """
    Updates a reservation, such as custom fields, estimated arrival time, room configuration and reservation status.
    It is necessary: a reservation_id and the reservation status.
    :return: Returns the reservation data as defined by getReservation call or an error with details in 'message'.
    """
    reservation_id = request.args.get('reservationID', None)
    status = request.args.get('status', None)

    if reservation_id is None:
        return jsonify({"success": "false", "message": "Missing reservationID"})
    elif status not in ['confirmed', 'not_confirmed', 'canceled', 'checked_in', 'checked_out', 'no_show']:
        return jsonify({'success': 'False',
                        'message': 'Reservation Status is not a valid status. Please check the value'})
    else:
        return jsonify({"data": {
            "adults": "1",
            "balance": "1125.0",
            "children": "0",
            "endDate": "05-10-2022",
            "guestAddress": "Rue da Torre 1",
            "guestAddress1": "Rue da Torre 1, Piso 1ro, Puerta 1",
            "guestBirthDate": "17-12-1990",
            "guestCellPhone": "+346854589",
            "guestCity": "Vigo",
            "guestCountry": "ES",
            "guestDocumentExpirationDate": "1-01-2029",
            "guestDocumentIssueDate": "1-01-2019",
            "guestDocumentIssuingCountry": "ES",
            "guestDocumentNumber": "K81231",
            "guestDocumentType": "Passport",
            "guestEmail": "eduardog90@gmail.com",
            "guestFirstName": "Eduardo",
            "guestGender": "M",
            "guestID": "58817062",
            "guestLastName": "García",
            "guestName": "Eduardo García",
            "guestPhone": "+346854589",
            "guestState": "Pontevedra",
            "guestZip": "36001",
            "paid": "0",
            "paidStatus": "false",
            "reservationID": "4442365621388",
            "roomID": "409037",
            "roomTypeID": "",
            "roomTypeName": "Deluxe King",
            "startDate": "01-10-2022",
            "total": "1125"
        }, "success": "true"})


@app.route('/postReservation', methods=['POST'])
def post_reservation():
    """
    Creates a new reservation. It is necessary a JSON with the reservation data.
    :return: The reservationId of the reservation created.
    """
    return {'success': True, 'reservationID': '4442365621388'}


@app.route('/getReservationInvoiceInformation')
def get_reservation_invoice_information():
    """
    Given a reservation id it gets the invoice information of a reservation (payments, balance, total, taxes)
    :return: The invoice information of a reservation.
    """
    reservation_id = request.args.get('reservationID', None)
    if reservation_id is None:
        return jsonify({"success": "false", "message": "Missing the reservation identifier."})
    else:
        return jsonify({"data": {
            "balance": "1125",
            "balanceDetailed": {
                "additionalItems": "0",
                "grandTotal": "1125",
                "paid": "0",
                "subTotal": "1125",
                "suggestedDeposit": "225",
                "taxesFees": "0"
            },
            "customFields": [],
            "mainGuestDetails": {
                "companyName": "",
                "companyTaxID": "",
                "guestAddress": "",
                "guestAddress2": "",
                "guestCellPhone": "",
                "guestCity": "",
                "guestCountry": "ES",
                "guestEmail": "ecampbelldsp@gmail.com",
                "guestFirstName": "Edward L.",
                "guestGender": "M",
                "guestLastName": "Campbell",
                "guestPhone": "",
                "guestState": "",
                "guestZip": "",
                "isAnonymized": "false",
                "taxID": ""
            },
            "reservationAddOnProducts": [],
            "reservationAddOnProductsTotal": "0",
            "reservationAdditionalProducts": [],
            "reservationAdditionalProductsTotal": "0",
            "reservationAdjustments": [],
            "reservationAdjustmentsTotal": "0",
            "reservationFees": [],
            "reservationFeesTotal": "0",
            "reservationPayments": [],
            "reservationPaymentsTotal": "0",
            "reservationRooms": [{
                "adults": "1",
                "children": "0",
                "endDate": "2022-10-06",
                "guestName": "Edward L. Campbell",
                "isAnonymized": "false",
                "nights": "5",
                "roomID": 'null',
                "roomName": "N/A",
                "roomTotal": "1125",
                "roomTypeID": "409037",
                "roomTypeName": "DLK",
                "startDate": "2022-10-01"
            }],
            "reservationRoomsTotal": "1125",
            "reservationTaxes": [],
            "reservationTaxesTotal": "0",
            "status": "no_show"
        },
            "success": "true"})


@app.route('/getGuestsInformation')
def get_guests_info():
    """
    Given a reservation id it gets all the guest in the reservation and they data.
    :return: The guests data in a reservation
    """
    reservation_id = request.args.get('reservationID', None)
    if reservation_id is None:
        return jsonify({"success": "false", "message": "Missing the reservation identifier."})
    else:
        return jsonify([{
            "guestAddress": "",
            "guestBirthdate": "",
            "guestCellPhone": "",
            "guestCity": "",
            "guestCountry": "ES",
            "guestDocumentExpirationDate": "",
            "guestDocumentIssueDate": "",
            "guestDocumentIssuingCountry": "",
            "guestDocumentNumber": "",
            "guestDocumentType": "",
            "guestEmail": "ecampbelldsp@gmail.com",
            "guestFirstName": "Edward L.",
            "guestGender": "M",
            "guestID": "58817062",
            "guestLastName": "Campbell",
            "guestPhone": "",
            "guestState": "",
            "guestZip": ""
        }])


@app.route('/getNumberOfGuests')
def how_many_guests():
    """
    Given a reservation id it gets the total of getss in the reservation
    :return: Total of guests in the reservation
    """
    reservation_id = request.args.get('reservationID', None)
    if reservation_id is None:
        return jsonify({"success": "false", "message": "Missing the reservation identifier."})
    else:
        return jsonify({"success": "true", "numberOfGuests": 1})


@app.route('/getAvailableRooms')
def get_available_rooms():
    """
    It gets the available rooms given a startDate, endDate, and the number of guests.
    :return: A list with the room types that are available
    """
    start_date = request.args.get('startDate', None)
    end_date = request.args.get('endDate', None)

    rooms = request.args.get('rooms', 1)
    adults = request.args.get('adults', None)
    children = request.args.get('children', None)

    if start_date is None or end_date is None or rooms is None or adults is None or children is None:
        return jsonify({"success": "false", "message": "Missing reservation data."})
    if not datetime.strptime(start_date, '%Y-%m-%d').date() > datetime.today().date():
        return jsonify({"success": "false", "message": "The start date must be greater than today."})
    elif not datetime.strptime(end_date, '%Y-%m-%d').date() > datetime.strptime(start_date, '%Y-%m-%d').date():
        return jsonify({"success": "false", "message": "The end date must be greater than the start date."})
    elif int(rooms) < 1:
        return jsonify({"success": "false", "message": "The number of rooms must be greater than 0."})
    elif int(adults) < 1:
        return jsonify({"success": "false", "message": "The number of adults must be greater than 0."})
    elif int(children) < 0:
        return jsonify({"success": "false", "message": "The number of children must be greater or equal than 0."})
    else:
        return jsonify({
            "availableRooms": [
                "Deluxe Queen",
                "Deluxe King",
                "Standard"
            ],
            "rooms": [{
                "adultsIncluded": "2",
                "childrenExtraCharge": {
                    "2": "15",
                    "3": "215"
                },
                "childrenIncluded": "1",
                "maxGuests": "4",
                "roomRate": "5",
                "roomRateID": "1185538",
                "roomTypeDescription": "Deluxe Queen room.",
                "roomTypeFeatures": [
                    "Batas de Baño",
                    "Televisión por cable (cargo)",
                    "Microondas"
                ],
                "roomTypeID": "409036",
                "roomTypeName": "Deluxe Queen",
                "roomTypeNameShort": "DLQ",
                "roomsAvailable": "1"
            }, {
                "adultsIncluded": "2",
                "childrenExtraCharge": {
                    "1": "100"
                },
                "childrenIncluded": "0",
                "maxGuests": "2",
                "roomRate": "5",
                "roomRateID": "1185539",
                "roomTypeDescription": "Deluxe King room",
                "roomTypeFeatures": [
                    "Batas de Baño",
                    "Televisión por cable (cargo)",
                    "Microondas",
                    "Minibar"
                ],
                "roomTypeID": "409037",
                "roomTypeName": "Deluxe King",
                "roomTypeNameShort": "DLK",
                "roomsAvailable": "1"
            }, {
                "adultsIncluded": "1",
                "childrenExtraCharge": {
                    "1": "100",
                    "10": "715",
                    "11": "715",
                    "12": "715",
                    "13": "715",
                    "14": "715",
                    "15": "715",
                    "16": "715",
                    "17": "715",
                    "18": "715",
                    "19": "715",
                    "2": "115",
                    "3": "315",
                    "4": "365",
                    "5": "465",
                    "6": "715",
                    "7": "715",
                    "8": "715",
                    "9": "715"
                },
                "childrenIncluded": "0",
                "maxGuests": "20",
                "roomRate": "5",
                "roomRateID": "1300448",
                "roomTypeDescription": "Disfrute su estancia",
                "roomTypeFeatures": [
                    "Batas de Baño",
                    "Cunas (previa solicitud)",
                    "Zapatillas",
                    "Tensión 110-127 voltios",
                    "Tensión 220-240 voltios",
                    "Aire Condicionado",
                    "Televisión por cable",
                    "Televisión por cable (cargo)",
                    "Ventiladores de Techo",
                    "Cafetera",
                    "Secador de Cabello",
                    "Sonido para iPod",
                    "Internet por cable",
                    "Internet por cable (cargo)",
                    "Microondas",
                    "Minibar",
                    "Rádio AM / FM",
                    "Internet inalámbrico (WiFi)",
                    "Internet inalámbrico (WiFi) - cargo"
                ],
                "roomTypeID": "438571",
                "roomTypeName": "Standard",
                "roomTypeNameShort": "DEL",
                "roomsAvailable": "1"
            }],
            "success": "true"
        })


@app.route('/postGuestDocument')
def post_guest_document():
    """
    Upload a guest document using the guest id.
    :return: a confirmation message and the document id assigned by the PMS
    """
    guest_id = request.args.get('guestID', None)
    path_to_document = request.args.get('pathDocument', None)

    if guest_id is None or path_to_document is None:
        return jsonify({"success": "false", "message": "Missing the guest identifier or the path to the doc."})
    else:
        return jsonify({
            "data": {
                "fileID": "23706119"
            },
            "success": 'true'
        })


@app.route('/postReservationDocument')
def post_reservation_document():
    """
    Upload a guest document using the reservation id.
    :return: a confirmation message and the document id assigned by the PMS
    """
    reservation_id = request.args.get('reservationID', None)
    path_to_document = request.args.get('pathDocument', None)

    if reservation_id is None or path_to_document is None:
        return jsonify({"success": "false", "message": "Missing the reservation identifier or the path to the doc."})
    else:
        return jsonify({
            "data": {
                "fileID": "23706119"
            },
            "success": 'true'
        })


@app.route('/reservationIsPaid')
def reservation_is_paid():
    """
    Given a reservation id it checks if the reservation is paid.
    :return: a message with a boolean variable paidStatus.
    """
    reservation_id = request.args.get('reservationID', None)
    if reservation_id is None:
        return jsonify({"success": "false", "message": "Missing the reservation identifier."})
    else:
        return jsonify({"success": "true", "paidStatus": "false"})


@app.route('/postPayment')
def post_payment():
    """
    Upload a payment into a reservation given the reservation id, the amount, and the card type
    :return: a confirmation message.
    """
    reservation_id = request.args.get('reservationID', None)
    amount = request.args.get('amount', None)
    payment_type = request.args.get('type', 'card')
    card_type: str = request.args.get('cardType', None)

    return request_payment_and_room.post_payment(reservation_id, amount, payment_type, card_type)


@app.route("/cam")
def picture():
    """
    Take a picture using the webcam.
    :return:
    """
    response = take_picture()
    return jsonify(response)


if __name__ == '__main__':
    # Flask app
    app.run(debug=True)
