from flask import request
from flask_restx import Resource
from ..service.property_service import get_all_properties_for_portfolio, save_new_property, get_property_by_id
from ..util.dto.property_dto import PropertyDto
from ..util.decorator import token_required

api = PropertyDto.api
_property = PropertyDto.property
_property_list = PropertyDto.property_list
_property_create = PropertyDto.property_create


@api.route('/')
class PropertyList(Resource):
	@token_required
	@api.doc('list_of_properties')
	@api.marshal_list_with(_property_list, envelope='data')
	def get(self, portfolio_id):
		"""Get all properties for the portfolio"""
		return get_all_properties_for_portfolio(portfolio_id)

	@token_required
	@api.response(201, 'Property successfully created.')
	@api.doc('create a new property')
	@api.expect(_property_create, validate=True)
	def post(self, portfolio_id):
		"""Creates a new Property """
		data = request.json
		return save_new_property(portfolio_id, data=data)
	

@api.route('/<int:property_id>')
class PropertyItem(Resource):
	@token_required
	@api.doc('property details')
	@api.marshal_list_with(_property, envelope='data')
	def get(self, portfolio_id, property_id):
		""" Gets the property by id. """
		return get_property_by_id(portfolio_id, property_id)
		
	@token_required
	@api.doc('update property')
	@api.marshal_list_with(_property, envelope='data')	
	def put(self, portfolio_id, property_id):
		"""Updates the property""" 
		data = request.json
		pass