from ..service.portfolio_service import get_all_portfolios, save_new_portfolio
from ..util.dto import PortfolioDto
from flask_restx import Resource
from ..util.decorator import token_required


api = PortfolioDto.api
_portfolio = PortfolioDto.portfolio


@api.route('/')
class PortfolioList(Resource):
	@token_required
	@api.doc('list_of_portfolios')
	@api.marshal_list_with(_portfolio, envelope='data')
	def get(self):
		"""List all registered users"""
		breakpoint() # Try and get logged in user here...
		return get_all_portfolios()

	@token_required
	@api.response(201, 'Portfolio successfully created.')
	@api.doc('create a new portfolio')
	@api.expect(_portfolio, validate=True)
	def post(self):
		"""Creates a new Portfolio """
		data = request.json
		return save_new_portfolio(data=data)