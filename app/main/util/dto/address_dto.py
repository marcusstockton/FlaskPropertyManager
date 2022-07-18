from flask_restx import Namespace, fields


class AddressDto:
    api = Namespace('address', description='address related operations')

    address = api.model('Address', {
        'id': fields.String(required=True, description='id'),
        'line_1': fields.String(required=True, description='address line_1'),
        'line_2': fields.String(required=True, description='address line_2'),
        'line_3': fields.String(required=True, description='address line_3'),
        'post_code': fields.String(required=True, description='address post_code'),
        'town': fields.String(required=True, description='address town'),
        'city': fields.String(required=True, description='address city'),
        'property_id': fields.String(required=True, description='address property_id'),
        'created_date': fields.DateTime(required=False, description='date created'),
        'updated_date': fields.DateTime(required=False, description='date last updated'),
    })

    address_create = api.model('Address', {
        'line_1': fields.String(required=True, description='address line_1'),
        'line_2': fields.String(required=False, description='address line_2'),
        'line_3': fields.String(required=False, description='address line_3'),
        'post_code': fields.String(required=True, description='address post_code'),
        'town': fields.String(required=False, description='address town'),
        'city': fields.String(required=False, description='address city'),
    })