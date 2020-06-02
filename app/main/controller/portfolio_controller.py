from flask import request
from flask_restx import Resource
from ..service.portfolio_service import get_all_portfolios_for_user, save_new_portfolio
from ..service.auth_helper import Auth
from ..util.dto import PortfolioDto
from ..util.decorator import token_required


api = PortfolioDto.api
_portfolio = PortfolioDto.portfolio


@api.route('/')
class PortfolioList(Resource):
	@token_required
	@api.doc('list_of_portfolios',security='apikey', params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
	@api.marshal_list_with(_portfolio, envelope='data')
	def get(self):
		"""Get all portfolio's for the logged in user"""
		user = Auth.get_logged_in_user(request)
		return get_all_portfolios_for_user(user[0]['data']['user_id'])

	@token_required
	@api.response(201, 'Portfolio successfully created.')
	@api.doc('create a new portfolio')
	@api.expect(_portfolio, validate=True)
	def post(self):
		"""Creates a new Portfolio """
		data = request.json
		return save_new_portfolio(data=data)