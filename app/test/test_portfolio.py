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

    @patch.object(Auth, 'get_logged_in_user', return_value=mock_get_logged_in_user_success())
    @patch.object(Auth, 'get_logged_in_user_object', return_value=mock_logged_in_user())
    def test_correct_portfolio_is_returned_for_id(self, mock_user, mock_auth):
        self.create_data()

        with app.test_client() as client:
            response = client.get('/portfolio/1')
            data = response.get_json()
            self.assertEqual('Test 1', data.get('data').get('name'))
            self.assertEqual('1', data.get('data').get('id'))
        #import pdb; pdb.set_trace()

    @patch.object(Auth, 'get_logged_in_user', return_value=mock_get_logged_in_user_success())
    @patch.object(Auth, 'get_logged_in_user_object', return_value=mock_logged_in_user())
    def test_portfolio_is_not_returned_for_non_owner_user_id(self, mock_user, mock_auth):
        self.create_data()

        with app.test_client() as client:
            response = client.get('/portfolio/2')
            self.assert404(response)
        #import pdb; pdb.set_trace()

    @patch.object(Auth, 'get_logged_in_user', return_value=mock_get_logged_in_user_success())
    @patch.object(Auth, 'get_logged_in_user_object', return_value=mock_logged_in_user())
    def test_update_portfolio_works_with_correct_data_and_user(self, mock_user, mock_auth):
        self.create_data()
        dict_data = {'id': '1', 'name': 'Updated Test 1', 'created_on': '2020-08-21T11:43:06.006284'}
        with app.test_client() as client:
            response = client.put('/portfolio/1', data=json.dumps(dict_data), headers={'Content-Type': 'application/json'},)
            self.assertIsNot(400, response.status_code)
            self.assertEqual(response.status_code, 204)
            
            response = client.get('/portfolio/1')
            data = json.loads(response.get_data(as_text=True))

            self.assertEqual('Updated Test 1', data.get('data').get('name'))
            

    @staticmethod
    def create_data():
        date = datetime.datetime.now()
        date -= datetime.timedelta(6 * 30) # date 6 months ago.
        user_1 = User(email="test@test.com", first_name="Foo", registered_on=date,
                last_name="Bar", username="test@test.com", admin=0)
        db.session.add(user_1)

        user_2 = User(email="test2@test.com", first_name="Fizz", registered_on=date,
                last_name="Buzz", username="test1@test.com", admin=0)
        db.session.add(user_2)

        portfolio1 = Portfolio(
            id=1,
            name='Test 1',
            created_on=datetime.datetime.now(),
            owner=user_1,
            properties=[],
        )
        db.session.add(portfolio1)

        portfolio2 = Portfolio(
            id=2,
            name='Test 2',
            created_on=datetime.datetime.now(),
            owner=user_2,
            properties=[],
        )
        db.session.add(portfolio2)

        db.session.commit()


