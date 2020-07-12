from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'first_name': fields.String(required=False, description='user first name'),
        'last_name': fields.String(required=False, description='user last name'),
        'date_of_birth': fields.Date(required=False, description='user date of birth'),
        'public_id': fields.String(description='user Identifier')
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })



class PropertyDto:
    api = Namespace('property', description='property related operations')
    address = api.model('address', {
        'id': fields.String(required=True, description='id'),
        'line_1': fields.String(required=True, description='address line_1'),
        'line_2': fields.String(required=True, description='address line_2'),
        'line_3': fields.String(required=True, description='address line_3'),
        'post_code': fields.String(required=True, description='address post_code'),
        'town': fields.String(required=True, description='address town'),
        'city': fields.String(required=True, description='address city'),
        'property_id': fields.String(required=True, description='address property_id'),
    })

    property = api.model('property', {
        'id': fields.String(required=True, description='id'),
        'portfolio_id': fields.String(required=True, description='portfolio id'),
        'address_id': fields.String(required=True, description='address id'),
        'purchase_price': fields.Float(required=True, description='purchase price'),
        'purchase_date': fields.DateTime(required=True, description='purchase date'),
        'monthly_rental_price': fields.Float(required=True, description='monthly rental price'),
        'address':fields.List(fields.Nested(address),required=True, description='address'),
    })


class PortfolioDto:
    api = Namespace('portfolio', description='portfolio related operations')
    portfolio = api.model('portfolio', {
        'id': fields.String(required=True, description='id'),
        'name': fields.String(required=True, description='portfolio name'),
        'created_on': fields.DateTime(required=True, description='date created'),
        'owner': fields.String(required=True, description='owner'),
        'properties':fields.List(fields.Nested(PropertyDto.property),required=True, description='properties'),
    })