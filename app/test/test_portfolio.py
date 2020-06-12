import unittest
import datetime
from unittest.mock import MagicMock, patch, PropertyMock
import json
from functools import wraps
from app.main import db
from app.test.base import BaseTestCase
from app.main.controller.portfolio_controller import PortfolioList
from app.main.model.portfolio import Portfolio
from app.main.service.auth_helper import Auth


def mock_get_logged_in_user_success():
    mock_response_object = dict(status='success', data=dict(user_id=1, email='test@test.com', admin=0,
                                                            registered_on=datetime.datetime.now()))
    return mock_response_object, 200


class TestPortfolioBlueprint(BaseTestCase):
    @patch('app.main.util.decorator.token_required')
    @patch('app.main.service.auth_helper.Auth.get_logged_in_user')
    def test_users_can_only_see_their_own_portfolios(self, mock_decorator, mock_auth):
        mock_decorator.return_value = mock_get_logged_in_user_success()

        portfolio1 = Portfolio(
            id = 1,
            name = 'Test 1',
            created_on = datetime.datetime.now(),
            owner = 1,
            properties = [],
        )
        db.session.add(portfolio1)
        portfolio2 = Portfolio(
            id = 2,
            name = 'Test 2',
            created_on = datetime.datetime.now(),
            owner = 2,
            properties = [],
        )
        db.session.add(portfolio2)
        db.session.commit()

        what_the_fuck_am_i_testing = PortfolioList.get(self)
        data_list = what_the_fuck_am_i_testing.get('data')
        data_dict = data_list[0]
        self.assertTrue(data_dict.get('name'), 'Test 1')
       