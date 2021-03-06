from flask_restx import Namespace, fields

from ._helpers import ObjectCount, SumOfProperties


class PortfolioDto:
    api = Namespace('portfolio', description='portfolio related operations')

    portfolio_details = api.model('Portfolio', {
        'id': fields.String(required=True, description='id'),
        'name': fields.String(required=True, description='portfolio name'),
        'created_on': fields.DateTime(required=True, description='date created', attribute="created_on", format='rfc822'),
        # 'owner': fields.Nested(UserDto.user, description='owner', attribute='owner'),
        'property_count': ObjectCount(attribute='properties'),
        'total_income': SumOfProperties(attribute='properties')
    })

    portfolio_create = api.model('Portfolio', {
        'name': fields.String(required=True, description='portfolio name'),
    })

    portfolio_update = api.model('Portfolio', {
        'id': fields.String(required=True, description='id'),
        'name': fields.String(required=True, description='portfolio name'),
    })
    portfolio_update_parser = api.parser()
    portfolio_update_parser.add_argument('id', location='json', type=int, required=True, help="ID of portfolio")
    portfolio_update_parser.add_argument("name", location='json', type=str, required=True, help="Name of portfolio")
    # portfolio_update_parser.add_argument("created_on", location='json',
    #                                      type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f'), required=False)

    portfolio_create_parser = api.parser()
    portfolio_create_parser.add_argument('name', location='json', type=str, required=True, help="Name of portfolio")
