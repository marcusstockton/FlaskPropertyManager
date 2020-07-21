from flask import request
from flask_restx import Resource
from ..service.auth_helper import Auth
from ..util.decorator import token_required
from ..util.dto.tenant_dto import TenantDto
from ..service.tenant_service import get_all_tenants_for_property, save_new_tenant

api = TenantDto.api
_tenant = TenantDto.tenant
_tenant_create = TenantDto.tenant_create

@api.route('/')
class TenantList(Resource):
	@token_required
	@api.doc('list_of_tenants')
	@api.marshal_list_with(_tenant, envelope='data')
	def get(self, portfolio_id, property_id):
		"""Get all tenants for the property"""
		return get_all_tenants_for_property(property_id)

	@token_required
	@api.response(201, 'Tenant successfully created.')
	@api.doc('create a new tenant against a property')
	@api.expect(_tenant_create, validate=True)
	def post(self, portfolio_id, property_id):
		"""Creates a new Tenant """
		data = request.json
		return save_new_tenant(portfolio_id, property_id, data=data)