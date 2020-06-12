import unittest
from unittest.mock import MagicMock, patch
import json
from app.test.base import BaseTestCase
from app.main.controller.portfolio_controller import PortfolioList


class TestPortfolioBlueprint(BaseTestCase):

    def mock_decorator(f):
        def decorated_function(g):
            return g
        if callable(f): # if no other parameter, just return the decorated function
            return decorated_function(f)
        return decorated_function # if there is a parametr (eg. string), ignore it and return the decorated function

    patch('../main/util/decorator', mock_decorator).start()
    def test_users_can_only_see_their_own_portfolios(self):
        portfolioList = PortfolioList()
        result = portfolioList.get()
        