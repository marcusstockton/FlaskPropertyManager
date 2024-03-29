# app/__init__.py

from http import HTTPStatus

from flask import Blueprint, jsonify, json
from flask_restx import Api
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError

from .main.controller.address_controller import api as address_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.portfolio_controller import api as portfolio_ns
from .main.controller.property_controller import api as property_ns
from .main.controller.tenant_controller import api as tenant_ns
from .main.controller.user_controller import api as user_ns

blueprint = Blueprint("api", __name__)

authorizations = {
    "Bearer Auth": {"type": "apiKey", "in": "header", "name": "Authorization"},
}

api = Api(
    blueprint,
    title="Marcus's API Property Manager with JWT auth",
    version="1.0",
    description="A service to help manage properties and portfolios",
    security="Bearer Auth",
    authorizations=authorizations,
)

api.add_namespace(user_ns, path="/user")
api.add_namespace(portfolio_ns, path="/portfolio")
api.add_namespace(property_ns, path="/portfolio/<int:portfolio_id>/property")
api.add_namespace(address_ns, path="/address")
api.add_namespace(
    tenant_ns, path="/portfolio/<int:portfolio_id>/property/<int:property_id>/tenants"
)
api.add_namespace(auth_ns)


# Global Error Handlers:
@api.errorhandler(IntegrityError)
def integrety_exception_handler(error):
    """Default Integrity Error handler"""
    return {"message": error.args}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.errorhandler(NotFound)
def not_found_exception_handler(error):
    """Default Not Found error handler"""
    return {"message": str(error)}, getattr(error, "code", HTTPStatus.NOT_FOUND)


@api.errorhandler(BadRequest)
def bad_request_exception_handler(error):
    """Default Bad Request error handler"""
    return {"message": str(error)}, getattr(error, "code", HTTPStatus.BAD_REQUEST)


@api.errorhandler(InternalServerError)
def internal_server_error_exception_handler(error):
    """Default Not Found error handler"""
    return {"message": str(error)}, getattr(
        error, "code", HTTPStatus.INTERNAL_SERVER_ERROR
    )


@api.errorhandler(Exception)
def generic_exception_handler(error):
    """Default error handler"""
    return {"message": str(error)}, getattr(
        error, "code", HTTPStatus.INTERNAL_SERVER_ERROR
    )
