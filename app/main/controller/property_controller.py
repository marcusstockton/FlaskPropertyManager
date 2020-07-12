from flask import request
from flask_restx import Resource
from ..service.property_service import get_all_properties_for_portfolio, save_new_property
from ..service.auth_helper import Auth
from ..util.dto import PropertyDto
from ..util.decorator import token_required

api = PropertyDto.api
_property = PropertyDto.property

@api.route('/')
class PropertyList(Resource):
	@token_required
	@api.doc('list_of_properties')
	@api.marshal_list_with(_property, envelope='data')
	def get(self, portfolio_id):
		"""Get all properties for the portfolio"""
		return get_all_properties_for_portfolio(portfolio_id)

	@token_required
	@api.response(201, 'Property successfully created.')
	@api.doc('create a new property')
	@api.expect(_property, validate=True)
	def post(self, portfolio_id):
		"""Creates a new Portfolio """
		data = request.json
		return save_new_property(portfolio_id, data=data)