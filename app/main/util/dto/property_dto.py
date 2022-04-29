from flask_restx import Namespace, fields

from .address_dto import AddressDto
from .tenant_dto import TenantDto


class PropertyDto:
    api = Namespace('property', description='property related operations')
    
    # address = api.model('Address', {
    #     'id': fields.String(required=True, description='id'),
    #     'line_1': fields.String(required=True, description='address line_1'),
    #     'line_2': fields.String(required=True, description='address line_2'),
    #     'line_3': fields.String(required=True, description='address line_3'),
    #     'post_code': fields.String(required=True, description='address post_code'),
    #     'town': fields.String(required=True, description='address town'),
    #     'city': fields.String(required=True, description='address city'),
    #     'property_id': fields.String(required=True, description='address property_id'),
    # })

    # address_create = api.model('Address', {
    #     'line_1': fields.String(required=True, description='address line_1'),
    #     'line_2': fields.String(required=False, description='address line_2'),
    #     'line_3': fields.String(required=False, description='address line_3'),
    #     'post_code': fields.String(required=True, description='address post_code'),
    #     'town': fields.String(required=False, description='address town'),
    #     'city': fields.String(required=False, description='address city'),
    # })

    property = api.model('Property', {
        'id': fields.String(required=True, description='id'),
        'portfolio_id': fields.String(required=True, description='portfolio id'),
        'address_id': fields.String(required=True, description='address id'),
        'purchase_price': fields.Float(required=True, description='purchase price'),
        'purchase_date': fields.DateTime(required=True, description='purchase date'),
        'monthly_rental_price': fields.Float(required=True, description='monthly rental price'),
        'address': fields.Nested(AddressDto.address, required=True, description='address'),
        'tenants': fields.List(fields.Nested(TenantDto.tenant), required=False, description='tenants'),
        'created_date': fields.DateTime(required=False, description='date created'),
        'updated_date': fields.DateTime(required=False, description='date last updated'),
    })

    property_list = api.model('Property', {
        'id': fields.String(required=True, description='id'),
        'portfolio_id': fields.String(required=True, description='portfolio id'),
        'address_id': fields.String(required=True, description='address id'),
        'purchase_price': fields.Float(required=True, description='purchase price'),
        'purchase_date': fields.DateTime(required=True, description='purchase date'),
        'monthly_rental_price': fields.Float(required=True, description='monthly rental price'),
        'address': fields.Nested(AddressDto.address, required=True, description='address'),
        'created_date': fields.DateTime(required=False, description='date created'),
        'updated_date': fields.DateTime(required=False, description='date last updated'),
    })

    property_create = api.model('Property', {
        'purchase_price': fields.Float(required=True, description='purchase price'),
        'purchase_date': fields.Date(required=True, description='purchase date'),
        'monthly_rental_price': fields.Float(required=True, description='monthly rental price'),
        'address':fields.Nested(AddressDto.address_create,required=True, description='address'),
    })
