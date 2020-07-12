from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import logging

from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)

    app.logger.setLevel(logging.DEBUG)
    app.logger.debug('Calling create_app(%s)', config_name)

    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    CORS(app, resources={r'/*': {'origins': '*'}})
    flask_bcrypt.init_app(app)

    return app
