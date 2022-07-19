import base64

from flask_restx import Namespace, fields

from .address_dto import AddressDto
from .tenant_dto import TenantDto


class Base64Decoder(fields.Raw):
	def format(self, value):
		data_bytes = base64.b64encode(value)
		data = data_bytes.decode("utf-8")
		return data


class PropertyDto:
	api = Namespace('property', description='property related operations')

	property_pictures = api.model('PropertyImages', {
		'id': fields.String(required=True, description='id'),
		'created_date': fields.DateTime(required=False, description='date created'),
		'updated_date': fields.DateTime(required=False, description='date last updated'),
		'file_name': fields.String(required=True, description='file name of image'),
		'image_base_64': Base64Decoder(attribute="image"),
	})

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
		'property_pics': fields.List(fields.Nested(property_pictures), required=False, description='images')
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
		'address': fields.Nested(AddressDto.address_create, required=True, description='address'),
	})
