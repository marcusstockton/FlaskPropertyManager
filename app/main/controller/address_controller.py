import os

import requests
from flask import make_response
from flask_restx import Resource

from ..util.decorator import token_required
from ..util.dto.address_dto import AddressDto

api = AddressDto.api


@api.route('/get-auto-suggestion/<search>', methods=['GET'])
class AddressSearchList(Resource):
    @token_required
    @api.doc('search for address by postcode')
    def get(self, search):
        # Go get data...
        _apiKey = os.getenv('HERE_Maps_API_Key')
        _ukLatLong = "55.3781,3.4360"
        _countryCode = "GBP"
        url = f"https://autosuggest.search.hereapi.com/v1/autosuggest?at={_ukLatLong}&countryCode={_countryCode}" \
              f"&limit=50&lang=en&q={search}&apiKey={_apiKey}"
        r = requests.get(url=url)
        data = r.json()
        return make_response(data, 200)
