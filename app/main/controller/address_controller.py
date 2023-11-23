import os

import requests
from flask import current_app
from flask import make_response
from flask_restx import Resource

from ..util.decorator import token_required
from ..util.dto.address_dto import AddressDto

api = AddressDto.api


@api.route('/get-auto-suggestion/<search>', methods=['GET'])
class AddressSearchList(Resource):
    '''Looks up address's from postcode'''
    @token_required
    @api.doc('search for address by postcode')
    def get(self, search):  #TODO - Move this into a service. Also, is this the best implementation?
        """Calls off to hereapi to get location details"""
        _apiKey = os.getenv('HERE_Maps_API_Key')
        _ukLatLong = "55.3781,3.4360"
        _countryCode = "GBP"

        url = f"https://autosuggest.search.hereapi.com/v1/autosuggest?at={_ukLatLong}&countryCode={_countryCode}" \
              f"&limit=50&lang=en&q={search}&apiKey={_apiKey}"
        current_app.logger.debug(f"{AddressSearchList.__name__} calling {url}")
        try:
            r = requests.get(url=url)
            data = r.json()
            return make_response(data, r.status_code)
        except requests.HTTPError as err:
            current_app.logger.error(f"{AddressSearchList.__name__} call failed {err}")
            return make_response(err, err.response.status_code)
