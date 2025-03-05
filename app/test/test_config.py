"""Config Tests"""

import os
import unittest

from flask import current_app
from flask_testing import TestCase
from manage import app
from app.main.config import basedir


class TestDevelopmentConfig(TestCase):
    """Test Development Config"""

    def create_app(self):
        app.config.from_object("app.main.config.DevelopmentConfig")
        return app

    def test_app_is_development(self) -> None:
        self.assertFalse(app.config["SECRET_KEY"] == "my_precious")
        self.assertTrue(app.config["DEBUG"] is True)
        self.assertFalse(current_app is None)


class TestTestingConfig(TestCase):
    """Test Testing Config"""

    def create_app(self):
        app.config.from_object("app.main.config.TestingConfig")
        return app

    def test_app_is_testing(self) -> None:
        self.assertFalse(app.config["SECRET_KEY"] == "my_precious")
        self.assertTrue(app.config["DEBUG"])
        self.assertTrue(app.config["TESTING"])
        self.assertTrue(app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:")


class TestProductionConfig(TestCase):
    """Test Prod Config"""

    def create_app(self):
        app.config.from_object("app.main.config.ProductionConfig")
        return app

    def test_app_is_production(self) -> None:
        self.assertTrue(app.config["DEBUG"] is False)


if __name__ == "__main__":
    unittest.main()
