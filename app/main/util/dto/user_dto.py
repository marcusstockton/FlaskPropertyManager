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
        'created_date': fields.DateTime(required=False, description='date created'),
        'updated_date': fields.DateTime(required=False, description='date last updated'),
        'public_id': fields.String(description='user Identifier')
    })

    user_create = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'first_name': fields.String(required=False, description='user first name'),
        'last_name': fields.String(required=False, description='user last name'),
        'date_of_birth': fields.Date(required=False, description='user date of birth')
    })

    user_details = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'first_name': fields.String(required=False, description='user first name'),
        'last_name': fields.String(required=False, description='user last name'),
        'date_of_birth': fields.Date(required=False, description='user date of birth'),
        'public_id': fields.String(description='user Identifier')
    })
