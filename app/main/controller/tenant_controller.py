import base64
import os
import imghdr
from flask import current_app as app
from flask import request
from flask_restx import Resource, abort
from werkzeug.datastructures import FileStorage

from ..service.tenant_service import get_all_tenants_for_property, save_new_tenant, get_tenant_by_id, delete_tenant, \
	add_profile_to_tenant, update_tenant
from ..util.decorator import token_required
from ..util.dto.tenant_dto import TenantDto

api = TenantDto.api
_tenant = TenantDto.tenant
_tenant_list = TenantDto.tenant_list
_tenant_create = TenantDto.tenant_create
_tenant_update = TenantDto.tenant_update

upload_parser = api.parser()
upload_parser.add_argument('image', location='files', type=FileStorage, required=True, help='Image file cannot empty')


@api.route('/')
class TenantList(Resource):
	@token_required
	@api.doc('list_of_tenants')
	@api.marshal_list_with(_tenant_list)
	def get(self, portfolio_id, property_id):
		"""Get all tenants for the property"""
		app.logger.info(f"Getting all tenants for propertyId {property_id}")
		return get_all_tenants_for_property(property_id)

	@token_required
	@api.response(201, 'Tenant successfully created.')
	@api.doc('create a new tenant against a property', responses={
		201: 'Tenant successfully created.',
		404: 'Property does not exist against this portfolio',
		409: 'Tenant already exists'
	})
	@api.expect(_tenant_create, validate=True)
	def post(self, portfolio_id, property_id):
		"""Creates a new Tenant """
		data = request.json
		app.logger.info(f"Adding new tenant {data.email_address} to {property_id}")
		return save_new_tenant(portfolio_id, property_id, data)


@api.route('/<int:tenant_id>')
class TenantItem(Resource):
	@token_required
	@api.doc('tenant details', responses={403: 'Not Authorized', 400: 'Bad Request', 200: 'Ok'})
	@api.marshal_with(_tenant)
	def get(self, portfolio_id, property_id, tenant_id):
		""" Gets a tenant by Id """
		app.logger.info(f"Finding tenant by id {tenant_id}")
		return get_tenant_by_id(portfolio_id, property_id, tenant_id)

	@token_required
	@api.doc('tenant delete', responses={403: 'Not Authorized', 400: 'Bad Request', 204: 'No Content'})
	@api.marshal_with(_tenant)
	def delete(self, portfolio_id, property_id, tenant_id):
		""" Deletes a tenant. """
		app.logger.info(f"Deleting tenant id {tenant_id} for property {property_id}")
		return delete_tenant(property_id, tenant_id)

	@token_required
	@api.doc('tenant update', responses={403: 'Not Authorized', 400: 'Bad Request', 204: 'Updated'})
	@api.expect(_tenant_update, validate=True)
	def put(self, portfolio_id, property_id, tenant_id):
		"""Update a tenant details"""
		data = request.json
		app.logger.info(f"Updating tenant id {tenant_id} for property {property_id}")
		return update_tenant(property_id, tenant_id, data)


@api.route('/<int:tenant_id>/images')
class TenantImage(Resource):
	@token_required
	@api.doc('Add an image of the tenant', responses={403: 'Not Authorized', 400: 'Bad Request', 201: 'Created'})
	@api.expect(upload_parser)
	def post(self, portfolio_id, property_id, tenant_id):
		""" Adds a tenant profile pic. """
		args = upload_parser.parse_args()
		file = args['image']
		if file:
			# The imghdr module determines the type of image contained in a file or byte stream.
			if imghdr.what(file) not in app.config['UPLOAD_EXTENSIONS']:
				abort(400, message="Invalid image type")

			# Save image as base64 string
			# verify user has permission to do this...?
			app.logger.info(f"Adding a tenant profile image {file.filename} for tenant id {tenant_id}")
			image_string = base64.b64encode(file.read())
			return add_profile_to_tenant(tenant_id, image_string)
