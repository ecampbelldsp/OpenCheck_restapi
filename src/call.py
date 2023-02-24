import json
import os.path
from typing import Tuple

import requests
import re


class requestVersion2:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, api_code: str, path_tokens: str):
        """
        Constructor of the class requestVersion2 that will be used to make the requests to the API.
        :param client_id: hotel client id
        :param client_secret: hotel secret id
        :param redirect_uri: uri to redirect the user after the authorization
        :param api_code: hotel code to make the requests
        :param path_tokens: path to the tokens.json file
        """
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.redirect_uri: str = redirect_uri
        self.api_code: str = api_code

        self.TOKENS_PATH: str = path_tokens
        self.access_token: str = ""
        self.refresh_token: str = ""
        self.update_tokens()

        self.valid_reservation_status = ('confirmed', 'not_confirmed', 'canceled', 'checked_in', 'checked_out',
                                         'no_show')
        self.valid_guest_document_type = ('dni', 'driver_license', 'na', 'nie', 'passport', 'social_security_card',
                                          'student_id')
        self.allowed_file_types = ['pdf', 'rtf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'gif', 'csv', 'txt', 'xls',
                                   'xlsx']

        self.allowed_payment_method = ["cash", "credit", "ebanking", "pay_pal"]

    @staticmethod
    def write_json(response: dict, path_to_write: str = "data/json_test.json") -> bool:
        """
        Write a json file in a specific path with the response of the API response.
        :param response: API response
        :param path_to_write: path to write the json file
        :return: True if the file is written correctly or raise an error in case of failure
        """
        try:
            with open(f"{path_to_write}", "w") as outfile:
                json_str = json.dumps(response, indent=len(response))
                outfile.write(json_str)
            return True
        except IOError:
            raise "Error writing JSON"

    @staticmethod
    def read_json(path_to_json: str) -> dict:
        """
        Read a json file from a specific path.
        :param path_to_json: path to the json file
        :return: A json object with the data of the json file or raise an error in case of failure
        """
        try:
            with open(path_to_json, 'r') as file:
                json_data = json.load(file)
            return json_data
        except IOError:
            raise "Error read JSON"

    def check_document(self, path, extension) -> bool:
        """
        Check if the document is valid.
        :param path: path to the document
        :param extension: extension of the document
        :return: True if the document is valid or raise an error in case of failure
        """

        if not (os.path.exists(path)):
            raise FileNotFoundError("Document not found")

        if extension not in self.allowed_file_types:
            raise IOError(f"Document type not valid.\n Allow file types are: {self.allowed_file_types}")

        document_size_bytes = os.path.getsize(path)
        if document_size_bytes > 1e+7:
            raise IOError(f"Allowed max file size: 10MB.\n Your document has {document_size_bytes} bytes")

        return True

    @staticmethod
    def connection_is_success(response: requests.request) -> bool:
        """
        Check if the connection is successful.
        :param response: API response
        :return: True if the connection is successful or raise an error in case of failure
        """

        if response.status_code == 200:
            return True
        else:
            raise ConnectionError(f"Status code: {response.status_code}.\n"
                                  f"{response.text}")

    @staticmethod
    def process_response(response_request: dict) -> dict:
        """
        Process the response of the API request in order to create compability with the frontend.
        :param response_request: response of the API request
        :return: A json object with the data of the response of the API request formatted
        """
        response_in_str = re.sub('true', '"true"', response_request.text)
        response_in_str = re.sub('false', '"false"', response_in_str)
        response_in_json = json.loads(response_in_str, parse_int=str, parse_float=str, parse_constant=str)

        return response_in_json

    def basic_request(self, r_type: str, url: str, header=None, payload=None, files=None) -> dict:
        """
        Make a basic http request to the API.
        :param r_type: Type of request (GET, POST, PUT, or DELETE)
        :param url: URL to make the request
        :param header: Header of the request
        :param payload: Payload with the data of the request
        :param files: Files to upload
        :return: a response in json format
        """
        if files is None:
            files = {}
        if payload is None:
            payload = {}
        if header is None:
            header = {}

        r = requests.request(r_type, url, headers=header, data=payload, files=files)

        if self.connection_is_success(r):
            response_in_json = self.process_response(r)
            return response_in_json

    @staticmethod
    def access_token_is_valid(access_token: str) -> bool:
        """A simple test method to determine if an access_token is valid. No request payload.
        :return: True if the access_token is valid. False otherwise.
        """
        if access_token:
            url = 'https://hotels.cloudbeds.com/api/v1.1/access_token_check'
            header = {'Authorization': 'Bearer ' + access_token}

            r = requests.request("POST", url, headers=header)
            if r.status_code == 200:
                return True
            else:
                return False
        else:
            raise ValueError("access_token is empty")

    def get_access_token_from_code(self) -> Tuple[str, str]:
        """
        Get the access token via OAuth from the code.
        :return: A tuple with the access token and the refresh token
        """

        url = 'https://hotels.cloudbeds.com/api/v1.1/access_token'
        payload = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'code': self.api_code}

        r = requests.request("POST", url, data=payload)
        response = json.loads(r.text)

        if r.status_code == 200:
            self.write_json(response, self.TOKENS_PATH)
            return response['access_token'], response['refresh_token']
        else:
            raise ConnectionError(f"Status code: {r.status_code}.\n"
                                  f"{response}")

    def get_access_token_from_refresh_token(self, refresh_token: str) -> Tuple[str, str]:
        """
        Get the access token via OAuth from the refresh token.
        :param refresh_token: Refresh token to get the access token
        :return: A tuple with the new access token and the new refresh token
        """

        url = 'https://hotels.cloudbeds.com/api/v1.1/access_token'
        payload = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'refresh_token': refresh_token}

        r = requests.request("POST", url, data=payload)
        if self.connection_is_success(r):
            response = json.loads(r.text)
            print(response)
            self.write_json(response, self.TOKENS_PATH)
            return response['access_token'], response['refresh_token']

    def update_tokens(self) -> Tuple[str, str]:
        """Update the access_token and the refresh_token. Then save the new values in the tokens.json
        :return: The new values of access_token and refresh_token
        """
        if os.path.exists(self.TOKENS_PATH):
            json_data = self.read_json(self.TOKENS_PATH)
            access_token = json_data['access_token']
            refresh_token = json_data['refresh_token']

            if not self.access_token_is_valid(access_token):
                access_token, refresh_token = self.get_access_token_from_refresh_token(refresh_token)
        else:
            access_token, refresh_token = self.get_access_token_from_code()

        self.access_token = access_token
        self.refresh_token = refresh_token
        return access_token, refresh_token

    def inner_tokens_check_and_update(self) -> Tuple[str, str]:
        """
        Check if the access token is valid. If not, update the tokens.
        :return: Return the new access token and the new refresh token
        """
        if not self.access_token_is_valid(self.access_token):
            return self.update_tokens()

    # Reservation
    def get_reservation(self, reservation_id: str) -> dict:
        """
        Get the reservation with its reservation_id.
        :param reservation_id: Reservation id to get the reservation
        :return: A json object with the reservation data
        """
        self.inner_tokens_check_and_update()

        r_type = 'GET'
        url = f"https://hotels.cloudbeds.com/api/v1.1/getReservation?reservationID={reservation_id}"
        header = {'Authorization': 'Bearer ' + self.access_token}

        response_json = self.basic_request(r_type, url, header)
        return response_json

    def put_reservation(self, reservation_id: str, status: str) -> dict:
        """
        Updates a reservation, such as custom fields, estimated arrival time, room configuration and reservation status.
        :param reservation_id: Reservation Unique Identifier, one reservation ID per call.
        :param status: Reservation status.
         Allowed values: 'confirmed', 'not_confirmed', 'canceled', 'checked_in', 'checked_out', 'no_show'
            'confirmed' - Reservation is confirmed
            'not_confirmed' - Reservation not passed confirmation
            'canceled' - Reservation is canceled
            'checked_in' - Guest is in hotel
            'checked_out' - Guest already left hotel
            'no_show' - Guest didn't show up on check-in date

        :return: Returns the reservation data as defined by getReservation call or an error with details in 'message'.
        """

        self.inner_tokens_check_and_update()

        if status not in self.valid_reservation_status:
            return {'success': 'False', 'message': 'Reservation Status is not a valid status. Please check the value'}
        else:

            r_type = 'PUT'
            url = f"https://hotels.cloudbeds.com/api/v1.1/putReservation"
            header = {'Authorization': 'Bearer ' + self.access_token}
            payload = {'reservationID': reservation_id,
                       'status': status}

            response_in_json = self.basic_request(r_type, url, header, payload)
            return response_in_json

    def post_reservation(self, reservation: str) -> dict:
        """
        Adds a reservation to the selected property.
        :param reservation: Reservation data in JSON format.
        :return: A reservation status and the reservation ID in JSON format.
        """

        def edit_reservation_for_api(reservation_json: dict) -> dict:
            """
            Useful function to transform the json form of a reservation to a valid format for CloudBeds API.
            The transformation consists makes a text plain entry of each index in the arrays: rooms, adults and children

            :param reservation_json:
            :return: reservation in the proper format of CloudBeds.
            """

            keys_to_remove = {'rooms', 'adults', 'children'}
            reservation_edited = {k: reservation_json[k] for k in reservation_json.keys() - keys_to_remove}

            for ind, room in enumerate(reservation_json["rooms"]):
                new_key = f"rooms[{ind}][roomTypeID]"
                new_data = room['roomTypeID']
                reservation_edited[new_key] = new_data

                new_key = f"rooms[{ind}][roomRateID]"
                new_data = room['roomRateID']
                reservation_edited[new_key] = new_data

                new_key = f"rooms[{ind}][quantity]"
                new_data = room['quantity']
                reservation_edited[new_key] = new_data

            for ind, adult in enumerate(reservation_json["adults"]):
                new_key = f"adults[{ind}][roomTypeID]"
                new_data = adult['roomTypeID']
                reservation_edited[new_key] = new_data

                new_key = f"adults[{ind}][quantity]"
                new_data = adult['quantity']
                reservation_edited[new_key] = new_data

            for ind, child in enumerate(reservation_json["children"]):
                new_key = f"children[{ind}][roomTypeID]"
                new_data = child['roomTypeID']
                reservation_edited[new_key] = new_data

                new_key = f"children[{ind}][quantity]"
                new_data = child['quantity']
                reservation_edited[new_key] = new_data

            return reservation_edited

        self.inner_tokens_check_and_update()

        r_type = 'POST'
        url = f"https://hotels.cloudbeds.com/api/v1.1/postReservation"
        header = {'Authorization': 'Bearer ' + self.access_token}
        reservation_transformed = edit_reservation_for_api(reservation)

        response_in_json = self.basic_request(r_type, url, header=header, payload=reservation_transformed)
        if response_in_json.get('success') == 'false':
            return response_in_json
        else:
            return {'success': True, 'reservationID': response_in_json.get('reservationID')}

    def post_reservation_document(self, reservation_id: str, document_path: str) -> dict:
        """
        Attaches a document to a reservation
        :param document_path: Form-based File Upload. Allowed file types in 'self.allowed_file_types'.
                              Allowed max file size: 10MB.
        :param reservation_id: Reservation Unique Identifier
        :return: A document ID or an error message.
        """

        self.inner_tokens_check_and_update()

        document_extension = document_path.split(".")[-1]
        self.check_document(document_path, document_extension)

        url = f"https://hotels.cloudbeds.com/api/v1.1/postReservationDocument"
        header = {'Authorization': 'Bearer ' + self.access_token,
                  'Accept': "multipart/form-data"}
        payload = {'reservationID': reservation_id}
        reservation_document = {'file': open(document_path, 'rb')}

        r = requests.post(url, headers=header, data=payload, files=reservation_document)
        response_in_json = self.process_response(r)

        return response_in_json

    def get_reservation_invoice_information(self, reservation_id: str) -> dict:
        """
        Returns the invoice information for a reservation.
        :param reservation_id: Reservation identifier (reservationID)
        :return: a JSON object with the invoice information.
        """

        self.inner_tokens_check_and_update()

        url = f"https://hotels.cloudbeds.com/api/v1.1/getReservationInvoiceInformation?reservationID={reservation_id}"
        header = {'Authorization': 'Bearer ' + self.access_token}

        r = requests.request("GET", url, headers=header)
        response_in_json = self.process_response(r)

        if self.connection_is_success(r):
            return response_in_json
        else:
            return {'success': False, 'message': response_in_json.get('message')}

    def reservation_is_paid(self, reservation_id: str) -> dict:
        """
        Checks if a reservation is paid.
        :param reservation_id: Reservation identifier (reservationID)
        :return: A boolean value indicating if the reservation is paid or not.
        """
        all_invoice_data = self.get_reservation_invoice_information(reservation_id)

        if 'data' in all_invoice_data.keys():
            payments_total = all_invoice_data['data']['reservationPaymentsTotal']
            paid = all_invoice_data['data']['balanceDetailed']['paid']

            if paid == payments_total:
                return {"success": "true", "paidStatus": "true"}
            else:
                return {"success": "true", "paidStatus": "false"}
        else:
            return {"success": "false", "message": all_invoice_data['message']}

    def how_much_left_to_paid(self, reservation_id: str) -> dict:
        """
        Returns the amount left to pay for a reservation.
        :param reservation_id: Reservation identifier (reservationID)
        :return: A JSON object with the amount left to pay.
        """
        all_invoice_data = self.get_reservation_invoice_information(reservation_id)

        if 'data' in all_invoice_data.keys():
            payments_total = all_invoice_data['data']['reservationPaymentsTotal']
            paid = all_invoice_data['data']['balanceDetailed']['paid']
            balance = payments_total - paid

            return {"success": "true", "balance": f"{balance}",
                    "paid": f"{paid}", "reservationPaymentsTotal": f"{payments_total}"}
        else:
            return {"success": "false", "message": all_invoice_data['message']}

    def invoice_detailed(self, reservation_id: str) -> dict:
        """
        Returns the detailed invoice information for a reservation.
        :param reservation_id: Reservation identifier (reservationID)
        :return: A JSON object with the detailed invoice information.
        """
        all_invoice_data = self.get_reservation_invoice_information(reservation_id)['data']
        balance_detailed = all_invoice_data['balanceDetailed']
        balance_detailed.update({"sucess": "true"})

        return balance_detailed

    def get_number_of_guests(self, reservation_id: str) -> dict:
        """
        Get the number of guests in a reservation.
        :param reservation_id:  The reservation ID of the reservation.
        :return: The number of guest in the reservation.
        """
        reservation = self.get_reservation(reservation_id)

        if reservation['success'] == 'true':
            return {'success': 'true', 'numberOfGuests': len(reservation['data']['guestList'])}
        else:
            return {'success': 'false', 'message': reservation['message']}

    def get_guest_info_in_reservation(self, reservation_id: str) -> dict:
        """
        Get the information of all the guests in a reservation.
        :param reservation_id:
        :return: List with all the guests' information.
        """

        def filter_guest_info(guest_data: dict) -> dict:
            """
            Filter the guest information to get only the necessary information.
            :param guest_data: Guest information as a JSON object.
            :return: A JSON object with the necessary information.
            """
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
        reservation = self.get_reservation(reservation_id)

        if reservation['success'] != 'false':
            guests_dict = reservation['data']['guestList']
            for guest_id in guests_dict.keys():
                guest_all_data = guests_dict[guest_id]
                guest.append(filter_guest_info(guest_all_data))

            return {"success": "true", "guest": guest}
        else:
            return {"success": "false", "message": reservation['message']}

    # Payment
    def get_payment_methods(self) -> dict:
        """
        Get the payment methods available in the account.
        :return: A JSON object with the payment methods.
        """

        self.inner_tokens_check_and_update()

        url = f"https://hotels.cloudbeds.com/api/v1.1/getPaymentMethods"
        header = {'Authorization': 'Bearer ' + self.access_token}

        r = requests.request("GET", url, headers=header)
        response = json.loads(r.text, parse_int=str)

        if self.connection_is_success(r) and response['success']:
            payment_methods = response['data']['methods']
            return payment_methods
        elif not response['success']:
            return response

    def post_payment(self, reservation_id: str, amount: float, payment_type: str, card_type: str) -> dict:
        """
        Post a payment to a reservation.
        :param reservation_id: Reservation identifier (reservationID)
        :param amount: Amount to pay
        :param payment_type: Payment type (cash, credit, or debit)
        :param card_type: Card type (Visa, MasterCard, etc.)
        :return: A JSON object with the payment information.
        """

        self.inner_tokens_check_and_update()

        url = f"https://hotels.cloudbeds.com/api/v1.1/postPayment"
        header = {'Authorization': 'Bearer ' + self.access_token}
        payload = {'reservationID': reservation_id,
                   'amount': str(amount),
                   'type': payment_type,
                   'cardType': card_type
                   }

        r = requests.request("POST", url, headers=header, data=payload)
        response = json.loads(r.text, parse_int=str)

        if self.connection_is_success(r):
            return response
        else:
            return {'success': 'false', 'message': response['message']}

    # Guest
    def get_guest(self, reservation_id: str = '', guest_id: str = '') -> dict:
        """
        Returns information on a guest specified by the Reservation ID parameter or by Guest ID
        :param reservation_id: Reservation ID used as query in the search.
        :param guest_id: Guest ID used as query in the search.
        :return: A JSON object with the guest information.
        """
        self.inner_tokens_check_and_update()

        if reservation_id == '':
            url = f"https://hotels.cloudbeds.com/api/v1.1/getGuest?guestID={guest_id}"
        else:
            url = f"https://hotels.cloudbeds.com/api/v1.1/getGuest?reservationID={reservation_id}"
        header = {'Authorization': 'Bearer ' + self.access_token}

        r = requests.request("GET", url, headers=header)
        response = json.loads(r.text, parse_int=str)

        if self.connection_is_success(r) and response['success']:
            return response['data']
        elif not response['success']:
            return response

    def update_guest_info(self, reservation_id: str, guest_id: str, guest_info: dict) -> dict:
        """
        Updates an existing guest with information provided. At least one information field is required for this call.
        :param reservation_id: Reservation identifier (reservationID)
        :param guest_id: Guest identifier (guestID)
        :param guest_info: A JSON object with the guest information to update
        :return: True if the info was update or a response in other cases.
        """

        self.inner_tokens_check_and_update()

        url = f"https://hotels.cloudbeds.com/api/v1.1/putGuest"
        header = {'Authorization': 'Bearer ' + self.access_token}
        payload = {'reservationID': reservation_id,
                   'guestID': guest_id} | guest_info

        r = requests.request("POST", url, headers=header, data=payload)
        response = json.loads(r.text, parse_int=str)

        if self.connection_is_success(r) and response['success']:
            return {'success': 'true'}
        elif not response['success']:
            return response

    def post_guest(self, reservation_id: str, guest_info: dict) -> dict:
        """
        Adds a guest to reservation as an additional guest.
        :param reservation_id: Reservation id where the guest is added.
        :param guest_info: dict with all the guest information.
        :return: True if the guest was added and a response in other cases.
        """

        self.inner_tokens_check_and_update()

        url = f"https://hotels.cloudbeds.com/api/v1.1/postGuest"
        header = {'Authorization': 'Bearer ' + self.access_token}
        payload = {'reservationID': reservation_id}
        payload = payload | guest_info

        r = requests.request("POST", url, headers=header, data=payload)
        response = json.loads(r.text, parse_int=str)

        if self.connection_is_success(r) and response['success']:
            return {'success': 'true'}
        elif not response['success']:
            return response

    def post_guest_document(self, guest_id: str, document_path: str) -> dict:
        """
        Attaches a document to a guest.
        :param document_path: Path to the guest document to upload.
        :param guest_id: Guest ID of the target guest.
        :return: A file ID if the request was valid or an error message.
        """

        self.inner_tokens_check_and_update()

        document_extension = document_path.split(".")[-1]
        self.check_document(document_path, document_extension)

        url = f"https://hotels.cloudbeds.com/api/v1.1/postGuestDocument"
        header = {'Authorization': 'Bearer ' + self.access_token,
                  'Accept': "multipart/form-data"}
        payload = {'guestID': guest_id}
        guest_document = {'file': open(document_path, 'rb')}

        r = requests.post(url, headers=header, data=payload, files=guest_document)
        response = json.loads(r.text, parse_int=str)

        if self.connection_is_success(r):
            return response
        else:
            return {'success': 'false', 'message': response['message']}

    # Rooms
    def get_available_room_types(self, start_date, end_date, rooms: int = 1, adults: int = 1, children: int = 0):
        """

        :param start_date:
        :param end_date:
        :param rooms:
        :param adults:
        :param children:
        :return: List with the available rooms.
        """

        def filter_rooms_available(response_data):
            filter_rooms, name_rooms = [], []

            request_info_room = {}
            for room in response_data['propertyRooms']:
                request_info_room['roomTypeID'] = room['roomTypeID']
                request_info_room['roomTypeName'] = room['roomTypeName']
                request_info_room['roomTypeNameShort'] = room['roomTypeNameShort']
                request_info_room['roomTypeDescription'] = room['roomTypeDescription']
                request_info_room['maxGuests'] = room['maxGuests']
                request_info_room['adultsIncluded'] = room['adultsIncluded']
                request_info_room['childrenIncluded'] = room['childrenIncluded']
                request_info_room['roomTypeFeatures'] = room['roomTypeFeatures']
                request_info_room['roomRateID'] = room['roomRateID']
                request_info_room['roomRate'] = room['roomRate']
                request_info_room['roomsAvailable'] = room['roomsAvailable']
                request_info_room['childrenExtraCharge'] = room.get('childrenExtraCharge', 0)
                name_rooms.append(room['roomTypeName'])

                filter_rooms.append(request_info_room.copy())

            return {'success': True, 'availableRooms': name_rooms, 'rooms': filter_rooms}

        self.inner_tokens_check_and_update()

        header = {'Authorization': 'Bearer ' + self.access_token}
        url = 'https://hotels.cloudbeds.com/api/v1.1/getAvailableRoomTypes'
        payload = f'?startDate={start_date}&endDate={end_date}&rooms={rooms}&adults={adults}&children={children}'

        r = requests.get(url + payload, headers=header)
        response = json.loads(r.text, parse_int=str)

        if self.connection_is_success(r) and response['success'] and response['roomCount'] == '0':
            return {'success': False, 'availableRooms': None, 'rooms': None, 'message': 'There is no rooms available.'}

        elif self.connection_is_success(r) and response['success'] and response['roomCount'] != 0:
            rooms_available = filter_rooms_available(response['data'][0])
            return rooms_available
        elif not response['success']:
            return response

    def get_rooms_unassigned(self):
        """
        Returns a list of unassigned rooms in the property.
        :return:
        """

        self.inner_tokens_check_and_update()

        url = 'https://hotels.cloudbeds.com/api/v1.1/getRoomsUnassigned'
        header = {'Authorization': 'Bearer ' + self.access_token}

        r = requests.get(url, headers=header)
        response = json.loads(r.text, parse_int=str)

        if self.connection_is_success(r):
            return response

    def post_room_assign(self, reservation_id: str, room_type_name: str):
        """
        Assign a room on a guest reservation.
        :param room_type_name:
        :param reservation_id:
        :return:
        """

        self.inner_tokens_check_and_update()

        rooms_unassigned = self.get_rooms_unassigned()['data'][0]['rooms']

        room_id = ''
        room_type_id = ''
        for room in rooms_unassigned:
            if room['roomTypeName'] == room_type_name:
                room_id = room['roomID']
                room_type_id = room['roomTypeID']
                break

        if not room_id:
            return {'success': False, 'message': 'All room of this type are assigned'}
        else:
            url = f"https://hotels.cloudbeds.com/api/v1.1/postRoomAssign"
            header = {'Authorization': 'Bearer ' + self.access_token}
            payload = {'reservationID': reservation_id,
                       'newRoomID': room_id,
                       'roomTypeID': room_type_id
                       }

            r = requests.request("POST", url, headers=header, data=payload)
            response = json.loads(r.text, parse_int=str)

            if self.connection_is_success(r):
                return response
