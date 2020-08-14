import flask
import unittest
import datetime
from unittest.mock import MagicMock, patch, PropertyMock
from app.main import db
from app.test.base import BaseTestCase
from app.main.model.portfolio import Portfolio
from app.main.service.auth_helper import Auth
from app.main.model.user import User
import json

from manage import app


def mock_get_logged_in_user_success():
    mock_response_object = dict(status='success', data=dict(user_id=1, email='test@test.com', admin=0,
                                                            registered_on=datetime.datetime.now()))
    return mock_response_object, 200


def mock_user_logged_in():
    return dict(status='success', data=dict(user_id=1, email='test@test.com', admin=0,
                                            registered_on=datetime.datetime.now()))


def mock_logged_in_user():
    return User(id=1, email="test@test.com", first_name="Foo",
                last_name="Bar", username="test@test.com", admin=0)


class TestPortfolioBlueprint(BaseTestCase):
    @patch.object(Auth, 'get_logged_in_user', return_value=mock_get_logged_in_user_success())
    @patch.object(Auth, 'get_logged_in_user_object', return_value=mock_logged_in_user())
    def test_users_can_only_see_their_own_portfolios(self, mock_user, mock_auth):
        self.create_data()

        with app.test_client() as client:
            response = client.get('/portfolio/')
            self.assertIsNot(401, response.status_code)
            self.assert200(response)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(1, len(data))

    @staticmethod
    def create_data():
        portfolio1 = Portfolio(
            id=1,
            name='Test 1',
            created_on=datetime.datetime.now(),
            owner_id=1,
            properties=[],
        )
        db.session.add(portfolio1)
        portfolio2 = Portfolio(
            id=2,
            name='Test 2',
            created_on=datetime.datetime.now(),
            owner_id=2,
            properties=[],
        )
        db.session.add(portfolio2)
        db.session.commit()


