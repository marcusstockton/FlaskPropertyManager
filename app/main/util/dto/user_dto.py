from flask_restx import Namespace, fields

class UserDto:
    '''User DTO'''
    api = Namespace('User', description='User related operations')

    user = api.model('User', {
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

    user_create = api.model('User', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'first_name': fields.String(required=False, description='user first name'),
        'last_name': fields.String(required=False, description='user last name'),
        'date_of_birth': fields.Date(required=False, description='user date of birth')
    })

    user_details = api.model('User', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'first_name': fields.String(required=False, description='user first name'),
        'last_name': fields.String(required=False, description='user last name'),
        'date_of_birth': fields.Date(dt_format='rfc822', required=False, description='user date of birth'),
        'public_id': fields.String(description='user Identifier')
    })
