import json
import os.path
import requests
import re


class Request:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, api_code: str, path_tokens: str):
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

    @staticmethod
    def write_json(response: dict, path_to_write: str = "data/json_test.json"):
        try:
            with open(f"{path_to_write}", "w") as outfile:
                json_str = json.dumps(response, indent=len(response))
                outfile.write(json_str)
        except IOError:
            raise "Error writing JSON"

    @staticmethod
    def read_json(path_to_json: str):
        try:
            with open(path_to_json, 'r') as file:
                json_data = json.load(file)
        except IOError:
            raise "Error read JSON"

        return json_data

    @staticmethod
    def response_is_success(response: requests.request):
        if response.status_code == 200:
            return True

        else:
            raise ConnectionError(f"Status code: {response.status_code}.\n"
                                  f"{response.text}")

    @staticmethod
    def access_token_is_valid(access_token):
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

    def get_access_token_from_code(self):
        url = 'https://hotels.cloudbeds.com/api/v1.1/access_token'
        payload = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'code': self.api_code}

        r = requests.request("POST", url, data=payload)
        response = json.loads(r.text)
        print(response)

        if r.status_code == 200:
            self.write_json(response, self.TOKENS_PATH)
            return response['access_token'], response['refresh_token']

        else:
            raise ConnectionError(f"Status code: {r.status_code}.\n"
                                  f"{response}")

    def get_access_token_from_refresh_token(self, refresh_token):

        url = 'https://hotels.cloudbeds.com/api/v1.1/access_token'
        payload = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'refresh_token': refresh_token}

        r = requests.request("POST", url, data=payload)
        if self.response_is_success(r):
            response = json.loads(r.text)
            print(response)
            self.write_json(response, self.TOKENS_PATH)
            return response['access_token'], response['refresh_token']

    def update_tokens(self):
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

    def get_reservation(self, reservation_id):

        if not self.access_token_is_valid(self.access_token):
            self.update_tokens()

        url = f"https://hotels.cloudbeds.com/api/v1.1/getReservation?reservationID={reservation_id}"
        header = {'Authorization': 'Bearer ' + self.access_token}

        r = requests.request("GET", url, headers=header)

        if self.response_is_success(r):
            response_in_str = re.sub('true', '"true"', r.text)
            # response_in_str = re.sub('\[' + '\]', '""', r.text)
            response_in_str = re.sub('false', '"false"', response_in_str)
            # response_in_str = re.sub('\n', '', response_in_str)

            response_in_json = json.loads(response_in_str, parse_int=str, parse_float=str, parse_constant=str)

            return response_in_json

    def put_reservation(self, reservation_id: str, status: str):
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

        if not self.access_token_is_valid(self.access_token):
            self.update_tokens()

        if status not in self.valid_reservation_status:
            raise ValueError("Reservation Status isn't a valid status. Please check the value")

        url = f"https://hotels.cloudbeds.com/api/v1.1/putReservation"
        header = {'Authorization': 'Bearer ' + self.access_token}
        payload = {'reservationID': reservation_id,
                   'status': status}

        r = requests.request("PUT", url, headers=header, data=payload)

        if self.response_is_success(r):
            response = json.loads(r.text)
            print(response)
            if response['success']:
                return True
            else:
                raise AttributeError(response['message'])

    def get_reservation_invoice_information(self, reservation_id):

        if not self.access_token_is_valid(self.access_token):
            self.update_tokens()

        url = f"https://hotels.cloudbeds.com/api/v1.1/getReservationInvoiceInformation?reservationID={reservation_id}"
        header = {'Authorization': 'Bearer ' + self.access_token}

        r = requests.request("GET", url, headers=header)

        if self.response_is_success(r):
            response = json.loads(r.text)
            return response

    def reservation_is_paid(self, reservation_id):
        all_invoice_data = self.get_reservation_invoice_information(reservation_id)['data']
        balance = all_invoice_data['balance']

        if balance == 0:
            return True
        else:
            return False

    def how_much_to_paid(self, reservation_id):
        all_invoice_data = self.get_reservation_invoice_information(reservation_id)['data']
        balance = all_invoice_data['balance']

        return balance

    def invoice_detailed(self, reservation_id):
        all_invoice_data = self.get_reservation_invoice_information(reservation_id)['data']
        balance_detailed = all_invoice_data['balanceDetailed']

        return balance_detailed

    def post_payment(self, reservation_id: str, amount: float, payment_type: str, card_type: str):

        if not self.access_token_is_valid(self.access_token):
            self.update_tokens()

        url = f"https://hotels.cloudbeds.com/api/v1.1/postPayment"
        header = {'Authorization': 'Bearer ' + self.access_token}
        payload = {'reservationID': reservation_id,
                   'amount': str(amount),
                   'type': payment_type,
                   'cardType': card_type
                   }

        r = requests.request("POST", url, headers=header, data=payload)

        if self.response_is_success(r):
            response = json.loads(r.text)
            print(response)
            return response
