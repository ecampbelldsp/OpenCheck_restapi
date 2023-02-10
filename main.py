from src.config import *

r_rooms = [{"roomTypeID": "409036", "quantity": "1", "roomRateID": "1185538"}]
r_adults = [{"roomTypeID": "409036", "quantity": "1"}]
r_children = [{"roomTypeID": "409036", "quantity": "1"}]

reservation = {"propertyID": "212599",
               "startDate": "2023-02-24",
               "endDate": "2023-02-27",
               "guestFirstName": "John",
               "guestLastName": "Doe",
               "guestCountry": "US",
               "guestZip": "1234",
               "guestEmail": "me@example.com",
               "guestPhone": "4567",
               "paymentMethod": "cash",
               "rooms": r_rooms,
               "adults": r_adults,
               "children": r_children
               }

# Create the request scope objects
request_guest_and_reservation = requestVersion2(client_id, client_secret, redirect_uri,
                                                code_4_scope_guest_and_reservation, path_tokens)

request_payment_and_room = requestVersion2(client_id, client_secret, redirect_uri,
                                           code_4_scope_payment_and_room, path_tokens_payment_and_room)


# Playground

#
def get_guest_info_in_reservation(_reservation):
    """
    Get the information of all the guests in a reservation.
    :param _reservation:
    :return: List with all the guests' information.
    """

    def filter_guest_info(guest_data):
        guest_info = {'guestID': guest_data['guestID'],
                      'guestFirstName': guest_data['guestFirstName'],
                      'guestLastName': guest_data['guestLastName'],
                      'guestGender': guest_data['guestGender'],
                      'guestEmail': guest_data['guestEmail'],
                      'guestPhone': guest_data['guestPhone'],
                      'guestCellPhone': guest_data['guestCellPhone'],
                      'guestCountry': guest_data['guestCountry'],
                      'guestAddress': guest_data['guestAddress'],
                      'guestCity': guest_data['guestCity'],
                      'guestZip': guest_data['guestZip'],
                      'guestState': guest_data['guestState'],
                      'guestBirthdate': guest_data['guestBirthdate'],
                      'guestDocumentType': guest_data['guestDocumentType'],
                      'guestDocumentNumber': guest_data['guestDocumentNumber'],
                      'guestDocumentIssueDate': guest_data['guestDocumentIssueDate'],
                      'guestDocumentExpirationDate': guest_data['guestDocumentExpirationDate'],
                      'guestDocumentIssuingCountry': guest_data['guestDocumentIssuingCountry']
                      }
        return guest_info

    guest = []
    guests_dict = _reservation['data']['guestList']
    for _guest_id in guests_dict.keys():
        guest_all_data = guests_dict[_guest_id]
        guest.append(filter_guest_info(guest_all_data))

    return guest


# Methods
def check_in_with_reservation(_reservation_id, _request_guest_and_reservation, _request_payment_and_room,
                              _guest_travel_form_path, _reservation_docu_path):
    """
    Flow Check-In with reservation ID.

    :param _reservation_docu_path: List with the reservation documents to upload.
    :param _guest_travel_form_path: List with the travels forms of guests.
    :param _reservation_id: The Reservation ID for the check-in process.
    :param _request_guest_and_reservation: a request object to communicate with CloudBed's scopes guest and reservation.
    :param _request_payment_and_room: a request object to communicate with CloudBed's scopes payment and room.
    :return: True if the check-in processes was done or False for other cases.
    """

    r = request_guest_and_reservation.get_reservation(reservation_id)
    check_in_guests_info = get_guest_info_in_reservation(r)

    for ind, guest in enumerate(check_in_guests_info):
        check_in_guest_id = guest['guestID']
        request_guest_and_reservation.post_guest_document(check_in_guest_id, guest_docu_path[ind])

    for reservation_document in reservation_docu_path:
        request_guest_and_reservation.post_reservation_document(reservation_id, reservation_document)

    if _request_guest_and_reservation.reservation_is_paid(reservation_id):
        print("Reservation paid")
    else:
        balance = _request_guest_and_reservation.how_much_left_to_paid(r['data'])
        print(f"You need to pay: {balance}")
        print(_request_payment_and_room.post_payment(_reservation_id, balance, 'credit', 'master'))

    if not r['data']['assigned']:
        unassigned_rooms = r['data']['unassigned']
        for room in unassigned_rooms:
            room_type_name = room['roomTypeName']
            _request_payment_and_room.post_room_assign(reservation_id, room_type_name)

    print(_request_guest_and_reservation.put_reservation(_reservation_id, "checked_in"))


def check_in_without_reservation(guest_info):
    guest_info.update({'propertyID': property_id, 'paymentMethod': 'card'})

    available_rooms = request_payment_and_room.get_available_room_types(guest_info['startDate'], guest_info['endDate'],
                                                                        guest_info['rooms'], guest_info['adults'],
                                                                        guest_info['children'])

    if available_rooms['success']:

        rooms = available_rooms['rooms']

        print(f"Tenemos disponibles {len(rooms)} tipos de habitaciones:\n")
        for ind, room in enumerate(rooms):
            print(f"\t{ind + 1}. {room['roomTypeName']}")
        print("\nPor favor, introduzca el número correspondiente al tipo de habitación q desea")

        room_info = {'rooms': [{"roomTypeID": room.get('roomTypeID'), "roomRateID": room.get('roomRateID'), "quantity": 1}]}
        adults = {'adults': [{"roomTypeID": room.get('roomTypeID'), "quantity": guest_info.get('adults'), "roomID": ""}]}
        children = {'children': [{"roomTypeID": room.get('roomTypeID'), "quantity": guest_info.get('children'), "roomID": ""}]}

        guest_info.update(room_info)
        guest_info.update(adults)
        guest_info.update(children)

        reservation_respond = request_guest_and_reservation.post_reservation(guest_info)
        if reservation_respond['success']:
            r_id = reservation_respond['reservationID']
            check_in_with_reservation(r_id, request_guest_and_reservation, request_payment_and_room, guest_docu_path,
                                      reservation_docu_path)
        else:
            return reservation_respond
    else:
        return available_rooms


def check_out(_reservation_id: str, _request_guest_and_reservation: requestVersion2, _request_payment_and_room: requestVersion2):
    r = request_guest_and_reservation.get_reservation(reservation_id)

    if _request_guest_and_reservation.reservation_is_paid(reservation_id):
        print("Reservation paid")
        print(_request_guest_and_reservation.put_reservation(_reservation_id, "checked_out"))
    else:
        balance = _request_guest_and_reservation.how_much_left_to_paid(r['data'])
        print(f"You need to pay: {balance}")
        print(_request_payment_and_room.post_payment(_reservation_id, balance, 'credit', 'master'))


request_guest_and_reservation.invoice_detailed(reservation_id)

# Flow Check-In with reservation ID.
check_in_with_reservation(reservation_id, request_guest_and_reservation, request_payment_and_room, guest_docu_path,
                          reservation_docu_path)

# Flow Check-In without reservation ID.
guest_information = {
    "startDate": "2022-12-08",
    "endDate": "2022-12-10",
    "guestFirstName": "Jose",
    "guestLastName": "Manuel",
    "guestCountry": "US",
    "guestZip": "1234",
    "guestEmail": "me@example.com",
    "guestPhone": "4567",
    "rooms": 1,
    "adults": 1,
    "children": 0
}
print(check_in_without_reservation(guest_information))

# Flow Check-Out
print(check_out(reservation_id, request_guest_and_reservation, request_payment_and_room))
