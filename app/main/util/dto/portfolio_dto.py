from flask_restx import Namespace, fields
from .property_dto import PropertyDto
from .user_dto import UserDto

class PortfolioDto:
    api = Namespace('portfolio', description='portfolio related operations')

    portfolio = api.model('Portfolio', {
        'id': fields.String(required=True, description='id'),
        'name': fields.String(required=True, description='portfolio name'),
        'created_on': fields.DateTime(required=True, description='date created', attribute="created_on", format='rfc822'),
        'owner':fields.Nested(UserDto.user, description='owner', attribute='owner'),
        'properties':fields.List(fields.Nested(PropertyDto.property),required=False, description='properties'),
    })

    portfolio_create = api.model('Portfolio', {
        'name': fields.String(required=True, description='portfolio name'),
    })

    portfolio_update = api.model('Portfolio', {
        'id': fields.String(required=True, description='id'),
        'name': fields.String(required=True, description='portfolio name'),
    })


