"""Config settings for the app."""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base Config"""

    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious_secret_key")
    DEBUG = False
    RESTX_MASK_SWAGGER = False


class LocalDev(Config):
    """Local Development Config.

    Used for local development without needing docker up and running etc.
    Requirements:
    Does need a local postgres database running on port 5432 with username:password of postgres:postgres
    """

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development Config"""

    DEBUG = True
    backupdb = "sqlite:///" + os.path.join(
        basedir, "flask_PropertyManager_main.db?check_same_thread=False"
    )
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or backupdb
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """Testing Config"""

    DEBUG = True
    TESTING = True
    #SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        basedir, "flask_PropertyManager_test.db?check_same_thread=False"
    )
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """Production Config"""

    DEBUG = False
    backupdb = "sqlite:///" + os.path.join(
        basedir, "flask_PropertyManager_main.db?check_same_thread=False"
    )
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or backupdb


config_by_name = dict(
    local=LocalDev, dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig
)

key = Config.SECRET_KEY
