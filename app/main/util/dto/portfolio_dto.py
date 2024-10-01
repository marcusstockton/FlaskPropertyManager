from flask_restx import Namespace, fields

from ._helpers import ObjectCount, SumOfProperties


class PortfolioDto:
    """Portfolio DTO"""

    api = Namespace("Portfolio", description="Portfolio related operations")

    portfolio_details = api.model(
        "Portfolio",
        {
            "id": fields.Integer(required=True, description="id"),
            "name": fields.String(required=True, description="portfolio name"),
            "created_date": fields.DateTime(
                required=True,
                description="date created",
                attribute="created_date",
                format="rfc822",
            ),
            "updated_date": fields.DateTime(
                required=True,
                description="date updated",
                attribute="updated_date",
                format="rfc822",
            ),
            # 'owner': fields.Nested(UserDto.user, description='owner', attribute='owner'),
            "property_count": ObjectCount(attribute="properties"),
            "total_income": SumOfProperties(attribute="properties"),
        },
    )

    # portfolio_create = api.model('Portfolio', {
    #     'name': fields.String(required=True, description='portfolio name'),
    # })

    portfolio_update = api.model(
        "Portfolio",
        {
            "id": fields.Integer(required=True, description="id"),
            "name": fields.String(required=True, description="portfolio name"),
        },
    )
    portfolio_update_parser = api.parser()
    portfolio_update_parser.add_argument(
        "id", location="json", type=int, required=True, help="ID of portfolio"
    )
    portfolio_update_parser.add_argument(
        "name", location="json", type=str, required=True, help="Name of portfolio"
    )
    # portfolio_update_parser.add_argument("created_date", location='json',
    #                                      type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f'), required=False)

    portfolio_create_parser = api.parser()
    portfolio_create_parser.add_argument(
        "name",
        location="json",
        type=str,
        required=True,
        nullable=False,
        help="Name of Portfolio",
    )
