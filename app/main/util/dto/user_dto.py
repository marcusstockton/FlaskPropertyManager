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
