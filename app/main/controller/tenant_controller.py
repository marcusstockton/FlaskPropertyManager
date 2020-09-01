from flask import request
from flask_restx import Resource

from ..util.decorator import token_required
from ..util.dto.tenant_dto import TenantDto
from ..service.tenant_service import get_all_tenants_for_property, save_new_tenant

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
