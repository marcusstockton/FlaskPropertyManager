# app/__init__.py

from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.portfolio_controller import api as portfolio_ns

blueprint = Blueprint('api', __name__)

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}

api = Api(blueprint,
          title='FLASK RESTX API PROPERTY MANAGER WITH JWT',
          version='1.0',
          description='a boilerplate for flask restx web service',
          security='Bearer Auth',
          authorizations=authorizations
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(portfolio_ns, path='/portfolio')
api.add_namespace(auth_ns)
