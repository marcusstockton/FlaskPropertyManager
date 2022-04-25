from flask import request
from flask_restx import Resource
import base64

from ..service.tenant_service import get_all_tenants_for_property, save_new_tenant, get_tenant_by_id, delete_tenant, add_profile_to_tenant
from ..util.decorator import token_required
from ..util.dto.tenant_dto import TenantDto

api = TenantDto.api
_tenant = TenantDto.tenant
_tenant_create_parser = TenantDto.tenant_create_parser


@api.route('/')
class TenantList(Resource):
	@token_required
	@api.doc('list_of_tenants')
	@api.marshal_list_with(_tenant, envelope='data')
	def get(self, portfolio_id, property_id):
		"""Get all tenants for the property"""
		return get_all_tenants_for_property(portfolio_id, property_id)

	@token_required
	# @api.response(201, 'Tenant successfully created.')
	@api.doc('create a new tenant against a property', responses={
		201: 'Tenant successfully created.',
		404: 'Property does not exist against this portfolio',
		409: 'Tenant already exists'
	})
	@api.expect(_tenant_create_parser, validate=True)
	def post(self, portfolio_id, property_id):
		"""Creates a new Tenant """
		data = _tenant_create_parser.parse_args()
		profile = request.files['profile']
		
		return save_new_tenant(portfolio_id, property_id, data, profile)


@api.route('/<int:tenant_id>')
class TenantItem(Resource):
	@token_required
	@api.doc('tenant details')
	@api.marshal_with(_tenant)
	def get(self, portfolio_id, property_id, tenant_id):
		""" Gets a tenant by Id """
		tenant = get_tenant_by_id(portfolio_id, property_id, tenant_id)
		return tenant

	@token_required
	@api.doc('Add an image of the tenant')
	def add_profile_pic(self, tenant_id):
		""" Adds a tenant profile pic. """
		file = request.files['file']
		if file:
			# Save image as base64 string
			image_string = base64.b64encode(file.read())
			return add_profile_to_tenant(tenant_id, image_string)

		

	@token_required
	@api.doc('tenant delete')
	@api.marshal_with(_tenant)
	def delete(self, portfolio_id, property_id, tenant_id):
		""" Deletes a tenant. """
		return delete_tenant(portfolio_id, property_id, tenant_id)


