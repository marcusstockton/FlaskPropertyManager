from flask import request
from flask_restx import Resource
import json
from ..service.portfolio_service import get_all_portfolios_for_user, save_new_portfolio, update_portfolio
from ..service.auth_helper import Auth
from ..util.dto.portfolio_dto import PortfolioDto
from ..util.decorator import token_required

api = PortfolioDto.api
_portfolio = PortfolioDto.portfolio


@api.route('/')
class PortfolioList(Resource):
	@token_required
	@api.doc('list_of_portfolios')
	@api.marshal_list_with(_portfolio, envelope='data')
	def get(self):
		"""Get all portfolio's for the logged in user"""
		user = Auth.get_logged_in_user_object(request)
		return get_all_portfolios_for_user(user.id)

	@token_required
	@api.response(201, 'Portfolio successfully created.')
	@api.doc('create a new portfolio')
	@api.expect(PortfolioDto.portfolio_create, validate=True)
	def post(self):
		"""Creates a new Portfolio """
		data = request.json
		user = Auth.get_logged_in_user_object(request)
		return save_new_portfolio(data=data, user=user)


@api.route('/<int:id>')
class PortfolioItem(Resource):
	@token_required
	@api.doc('single portfolio')
	@api.marshal_list_with(_portfolio, envelope='data')
	def get(self, id):
		""" Displays a portfolio's details """
		data = request.json
		breakpoint()

	@token_required
	@api.doc('update a portfolio')
	@api.marshal_list_with(_portfolio, envelope='data')
	@api.response(201, 'Portfolio updated created.')
	@api.expect(PortfolioDto.portfolio_create, validate=True)
	def put(self, id):
		""" Edits a selected conference """
		data = request.json
		import pdb; pdb.set_trace()
		return update_portfolio(id, data)