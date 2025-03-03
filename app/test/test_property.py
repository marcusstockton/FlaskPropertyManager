from datetime import datetime, timedelta
import json
from unittest.mock import patch
import uuid
from app.main import db
from app.main.model import address, property
from app.main.model.portfolio import Portfolio
from app.main.model.user import User
from app.test.base import BaseTestCase
from manage import app


def create_owner_user() -> str:
    """Creates a non-admin user and returns the auth token"""
    user: User = db.session.query(User).filter_by(username="test@test.com").one()
    auth_token: str = user.encode_auth_token(user.id)
    if isinstance(auth_token, str):
        return auth_token
    return ""


class TestPropertyBlueprint(BaseTestCase):
    """Property Unit tests"""

    def test_correct_properties_are_loaded_for_portfolio(self):
        self.create_data()

        access_token: str = create_owner_user()
        headers: dict[str, str] = {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
            "Authorization": access_token,
        }
        with patch(
            "app.main.controller.property_controller.get_all_properties_for_portfolio"
        ) as mock_get_portfolio_by_id:
            mock_get_portfolio_by_id.return_value = property.Property.query.filter_by(portfolio_id=1).all()
            with app.test_client() as client:

                response = client.get("/portfolio/1/property/", headers=headers)
                print(response)
                self.assert200(response)
                data = json.loads(response.get_data(as_text=True))
                self.assertEqual(2, len(data))

                # response = client.get("/portfolio/2/property/", headers=headers)
                # print(response)
                # self.assert404(response)
                # data = json.loads(response.get_data(as_text=True))
                # self.assertEqual(0, len(data))

    #
    @staticmethod
    def create_data():
        """Creates some test data for these tests"""
        date: datetime = datetime.now()
        date -= timedelta(6 * 30)  # date 6 months ago.
        user_1 = User(
            email="test@test.com",
            public_id=str(uuid.uuid4()),
            first_name="Foo",
            registered_on=date,
            last_name="Bar",
            username="test@test.com",
            admin=False,
        )
        user_1.password = "test"
        db.session.add(user_1)

        user_2 = User(
            email="test2@test.com",
            public_id=str(uuid.uuid4()),
            first_name="Fizz",
            registered_on=date,
            last_name="Buzz",
            username="test1@test.com",
            admin=False,
        )
        user_2.password = "test2"
        db.session.add(user_2)

        portfolio1 = Portfolio(
            name="Test 1",
            owner=user_1,
            properties=[
                property.Property(
                    address=address.Address(
                        line_1="12",
                        line_2="Main Street",
                        line_3="",
                        post_code="EX11EX",
                        town="",
                        city="Exeter",
                    ),
                    purchase_price=123000,
                    purchase_date=datetime(2015, 4, 12),
                    monthly_rental_price=985,
                ),
                property.Property(
                    address=address.Address(
                        line_1="Flat 12",
                        line_2="The Mall",
                        line_3="",
                        post_code="TQ121RT",
                        town="",
                        city="Torquay",
                    ),
                    purchase_price=89000,
                    purchase_date=datetime(2012, 6, 24),
                    monthly_rental_price=785,
                ),
            ],
        )
        db.session.add(portfolio1)

        portfolio2 = Portfolio(
            name="Test 2",
            owner=user_2,
            properties=[
                property.Property(
                    address=address.Address(
                        line_1="189",
                        line_2="Mildew Avenue",
                        line_3="",
                        post_code="KA12KA",
                        town="",
                        city="Cambridge",
                    ),
                    purchase_price=2000000,
                    purchase_date=datetime(1999, 11, 23),
                    monthly_rental_price=1500,
                ),
            ],
        )
        db.session.add(portfolio2)
        db.session.commit()
