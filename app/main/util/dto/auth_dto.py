from flask_restx import Namespace, fields


class AuthDto:
    '''Auth DTO'''
    api = Namespace('Auth', description='Authentication related operations')
    
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })
