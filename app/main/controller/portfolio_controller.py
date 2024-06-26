"""Portfolio Controller API Endpoints"""

from flask import current_app as app
from flask import request
from flask_restx import Resource
from werkzeug.exceptions import NotFound

from ..service.auth_helper import Auth
from ..service.portfolio_service import (
    get_all_portfolios_for_user,
    save_new_portfolio,
    update_portfolio,
    get_portfolio_by_id,
    delete_portfolio_by_id,
)
from ..util.decorator import token_required
from ..util.dto.portfolio_dto import PortfolioDto

api = PortfolioDto.api
_portfolio_details = PortfolioDto.portfolio_details
_portfolio_update_parser = PortfolioDto.portfolio_update_parser
_portfolio_create_parser = PortfolioDto.portfolio_create_parser


@api.route("/")
class PortfolioList(Resource):
    """Portfolio List endpoints"""

    @token_required
    @api.doc("list_of_portfolios")
    @api.marshal_list_with(_portfolio_details)
    def get(self):
        """Get all portfolio's for the logged-in user"""
        user = Auth.get_logged_in_user_object(request)
        if user is not None:
            app.logger.info(f"Getting all portfolios' for {user.username}")
            portfolios = get_all_portfolios_for_user(user)
            return portfolios
        raise NotFound(user)

    @token_required
    @api.response(201, "Portfolio successfully created.")
    @api.doc("create a new portfolio")
    @api.marshal_with(_portfolio_details)
    @api.expect(_portfolio_create_parser, validate=True)
    def post(self):
        """Creates a new Portfolio"""
        data = _portfolio_create_parser.parse_args()
        user = Auth.get_logged_in_user_object(request)
        if user is None:
            raise NotFound(user)
        app.logger.info(f"Creating a new portfolio for {user.username}")
        return save_new_portfolio(data=data, user_id=user.id)


@api.route("/<int:portfolio_id>")
class PortfolioItem(Resource):
    """Singular Portfolio endpoints"""

    @token_required
    @api.doc("single portfolio")
    @api.marshal_with(_portfolio_details)
    def get(self, portfolio_id):
        """Displays a portfolio's details"""
        user = Auth.get_logged_in_user_object(request)
        if user is None:
            raise NotFound(user)
        app.logger.info(f"Finding Portfolio by Id {portfolio_id} for {user.username}")
        return get_portfolio_by_id(user.id, portfolio_id)

    @token_required
    @api.doc("update a portfolio")
    @api.marshal_with(_portfolio_details)
    @api.response(200, "Portfolio updated created.")
    @api.response(500, "Internal Server Error")
    @api.response(404, "Portfolio Not found")
    @api.expect(_portfolio_update_parser, validate=True)
    def put(self, portfolio_id):
        """Edits a portfolio"""
        data = _portfolio_update_parser.parse_args()
        return update_portfolio(portfolio_id, data)

    @token_required
    @api.response(204, "Portfolio and related data deleted.")
    @api.response(404, "Portfolio Not found")
    def delete(self, portfolio_id):
        """Deletes a portfolio"""
        user = Auth.get_logged_in_user_object(request)
        return delete_portfolio_by_id(user, portfolio_id)
