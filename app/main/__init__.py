import logging

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from .config import config_by_name

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
flask_bcrypt = Bcrypt()


def create_app(config_name: str) -> Flask:
    """Creates the application"""
    app = Flask(__name__)
    CORS(app)
    app.logger.setLevel(logging.DEBUG)
    app.logger.debug("Calling create_app(%s)", config_name)

    app.config.from_object(config_by_name[config_name])
    app.config["ERROR_404_HELP"] = False
    app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2MB limit
    app.config["UPLOAD_EXTENSIONS"] = ["jpg", "jpeg", "png", "gif", "tif"]
    db.init_app(app)

    flask_bcrypt.init_app(app)

    return app
