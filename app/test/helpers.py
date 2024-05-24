########################
#### helper methods ####
########################

import json
from datetime import datetime
from typing import List

from app.main.model.address import Address
from app.main.model.portfolio import Portfolio
from app.main.model.property import Property
from app.main.model.user import User


def mock_get_logged_in_user_success():
    """Mocks an @token_required"""
    mock_response_object = dict(
        status="success",
        data=dict(
            user_id=1,
            email="test@test.com",
            username="test@test.com",
            admin=0,
            registered_on=str(datetime.now()),
        ),
    )
    return mock_response_object, 200


def mock_logged_in_user():
    """Mocks a logged in user"""
    user = User(
        email="test@test.com",
        first_name="Foo",
        last_name="Bar",
        username="test@test.com",
        registered_on=datetime.now(),
        admin=False,
    )
    user.id = 1
    return user


def register(self, email, username, password):
    return self.client.post(
        "/user/",
        data=json.dumps(dict(email=email, username=username, password=password)),
        content_type="application/json",
    )


def login(self, email, password):
    return self.client.post(
        "/auth/login",
        data=json.dumps(dict(email=email, password=password)),
        content_type="application/json",
    )


def logout(self):
    return self.client.get("/logout", follow_redirects=True)


def mock_get_all_portfolios_for_user() -> List[Portfolio]:
    """Creates a list of portfolios to mock get_all_portfolios_for_user function"""
    new_list = []
    user = User(
        email="test@test.com",
        first_name="Foo",
        last_name="Bar",
        username="test@test.com",
        registered_on=datetime.now(),
        admin=False,
    )
    user.id = 1
    user.created_date = datetime.now()
    user.updated_date = datetime.now()

    address = Address(
        line_1="Line 1",
        line_2="Line 2",
        line_3="Line 3",
        city="Exeter",
        post_code="EX11EX",
        town="Pinhow",
    )
    address.id = 1
    address.created_date = datetime.now()
    address.updated_date = datetime.now()

    prop_list = []

    property1 = Property(
        address=address,
        monthly_rental_price=1000,
        purchase_date=datetime(2012, 3, 12),
        purchase_price=213000,
    )
    property1.id = 1
    property1.portfolio_id = 1

    property1.created_date = datetime.now()
    property1.updated_date = datetime.now()
    prop_list.append(property1)

    portfolio = Portfolio(
        name="Test Portfolio One",
        owner_id=user.id,
        owner=user,
        properties=prop_list,
    )
    portfolio.created_date = datetime(2011, 2, 5, 12, 12, 12)
    portfolio.updated_date = datetime(2022, 5, 8, 12, 12, 12)
    portfolio.id = 1
    new_list.append(portfolio)

    return new_list
