from flask import request
from flask_restx import Resource
import base64
from werkzeug.datastructures import FileStorage

from ..service.tenant_service import get_all_tenants_for_property, save_new_tenant, get_tenant_by_id, delete_tenant, add_profile_to_tenant
from ..util.decorator import token_required
from ..util.dto.tenant_dto import TenantDto

api = TenantDto.api
_tenant = TenantDto.tenant
_tenant_list = TenantDto.tenant_list
_tenant_create_parser = TenantDto.tenant_create_parser
_tenant_create = TenantDto.tenant_create

upload_parser = api.parser()
upload_parser.add_argument('image', location='files', type=FileStorage, required=True)

@api.route('/')
class TenantList(Resource):
	@token_required
	@api.doc('list_of_tenants')
	@api.marshal_list_with(_tenant_list, envelope='data')
	def get(self, portfolio_id, property_id):
		"""Get all tenants for the property"""
		return get_all_tenants_for_property(property_id)


	@token_required
	# @api.response(201, 'Tenant successfully created.')
	@api.doc('create a new tenant against a property', responses={
		201: 'Tenant successfully created.',
		404: 'Property does not exist against this portfolio',
		409: 'Tenant already exists'
	})
	@api.expect(_tenant_create, validate=True)
	def post(self, portfolio_id, property_id):
		"""Creates a new Tenant """
		#import pdb; pdb.set_trace()
		data = request.json
		import pdb; pdb.set_trace()
		return save_new_tenant(portfolio_id, property_id, data)


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
	@api.doc('tenant delete')
	@api.marshal_with(_tenant)
	def delete(self, portfolio_id, property_id, tenant_id):
		""" Deletes a tenant. """
		return delete_tenant(portfolio_id, property_id, tenant_id)


@api.route('/<int:tenant_id>/images')
class TenantImage(Resource):
	#@token_required
	@api.doc('Add an image of the tenant')
	@api.expect(upload_parser)
	def post(self, portfolio_id, property_id, tenant_id):
		""" Adds a tenant profile pic. """
		args = upload_parser.parse_args()
		file = args['image']
		import pdb;pdb.set_trace()
		if file:
			# Save image as base64 string
			# verify user has permission to do this...?
			image_string = base64.b64encode(file.read())
			return add_profile_to_tenant(tenant_id, image_string)