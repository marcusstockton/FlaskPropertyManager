import datetime
import json
from unittest.mock import patch

from app.main import db
from app.main.model.address import Address
from app.main.model.portfolio import Portfolio
from app.main.model.property import Property
from app.main.model.user import User, Role, UserRoles
from app.main.service.auth_helper import Auth
from app.test.base import BaseTestCase
from app.test.helpers import mock_get_logged_in_user_success, mock_logged_in_user
from manage import app
from sqlalchemy import delete


class TestPortfolioBlueprint(BaseTestCase):
    """Test class for Portfolio endpoints"""

    # def setUp(self):
    #     self.create_data()

    # def tearDown(self):
    #     self.remove_data()

    @patch.object(
        Auth, "get_logged_in_user", return_value=mock_get_logged_in_user_success()
    )
    @patch.object(Auth, "get_logged_in_user_object", return_value=mock_logged_in_user())
    def test_users_can_only_see_their_own_portfolios(self, mock_user, mock_auth):
        self.create_data()

        with app.test_client() as client:
            response = client.get("/portfolio/")
            self.assert200(response)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(1, len(data))

    @patch.object(
        Auth, "get_logged_in_user", return_value=mock_get_logged_in_user_success()
    )
    @patch.object(Auth, "get_logged_in_user_object", return_value=mock_logged_in_user())
    def test_correct_portfolio_is_returned_for_id(self, mock_user, mock_auth):
        self.create_data()

        with app.test_client() as client:
            response = client.get("/portfolio/1")
            data = response.get_json()
            self.assertEqual("Test 1", data.get("name"))
            self.assertEqual("1", data.get("id"))

    @patch.object(
        Auth, "get_logged_in_user", return_value=mock_get_logged_in_user_success()
    )
    @patch.object(Auth, "get_logged_in_user_object", return_value=mock_logged_in_user())
    def test_portfolio_is_not_returned_for_non_owner_user_id(
        self, mock_user, mock_auth
    ):
        self.create_data()

        with app.test_client() as client:
            response = client.get("/portfolio/2")
            self.assert404(response)

    @patch.object(
        Auth, "get_logged_in_user", return_value=mock_get_logged_in_user_success()
    )
    @patch.object(Auth, "get_logged_in_user_object", return_value=mock_logged_in_user())
    def test_update_portfolio_works_with_correct_data_and_user(
        self, mock_user, mock_auth
    ):
        self.create_data()
        dict_data = {"id": "1", "name": "Updated Test 1"}
        with app.test_client() as client:
            response = client.put(
                "/portfolio/1",
                data=json.dumps(dict_data),
                headers={"Content-Type": "application/json"},
            )
            self.assert200(response)
            data = json.loads(response.get_data(as_text=True))

            self.assertEqual("Updated Test 1", data.get("name"))

    @patch.object(
        Auth, "get_logged_in_user", return_value=mock_get_logged_in_user_success()
    )
    @patch.object(Auth, "get_logged_in_user_object", return_value=mock_logged_in_user())
    def test_update_portfolio_fails_if_incorrect_data_used(self, mock_user, mock_auth):
        self.create_data()
        dict_data = {"id": "2", "name": "Updated Test 1"}
        with app.test_client() as client:
            response = client.put(
                "/portfolio/1",
                data=json.dumps(dict_data),
                headers={"Content-Type": "application/json"},
            )
            self.assertEqual(response.status_code, 500)

    @patch.object(
        Auth, "get_logged_in_user", return_value=mock_get_logged_in_user_success()
    )
    @patch.object(Auth, "get_logged_in_user_object", return_value=mock_logged_in_user())
    def test_get_portfolio_returns_correct_property_count_with_correct_data_and_user(
        self, mock_user, mock_auth
    ):
        self.create_data()
        # get portfolio to append a property or two to it
        portfolio = db.session.query(Portfolio).filter(Portfolio.id == 1).one()
        property1 = Property(
            portfolio_id=portfolio.id,
            owner_id=1,
            purchase_price=32000,
            purchase_date=datetime.datetime(2020, 5, 17),
            monthly_rental_price=670,
            address=Address(
                line_1="Test Line 1",
                line_2="Test Line 2",
                post_code="EX11EX",
                city="Exeter",
            ),
        )
        portfolio.properties.append(property1)
        db.session.commit()

        # Do the test:
        with app.test_client() as client:
            response = client.get("/portfolio/1")
            self.assert200(response)
            data = json.loads(response.get_data(as_text=True))

            self.assertEqual(1, data.get("property_count"))

    @patch.object(
        Auth, "get_logged_in_user", return_value=mock_get_logged_in_user_success()
    )
    @patch.object(Auth, "get_logged_in_user_object", return_value=mock_logged_in_user())
    def test_create_portfolio_with_xss_input_is_sanitized(self, mock_user, mock_auth):
        new_portfolio = {"name": "<script>alert();</script>"}
        # Do the test:
        with app.test_client() as client:
            response = client.post(
                "/portfolio/",
                data=json.dumps(new_portfolio),
                headers={"Content-Type": "application/json"},
            )
            self.assert200(response)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual("&lt;script&gt;alert();&lt;/script&gt;", data.get("name"))

    @patch.object(
        Auth, "get_logged_in_user", return_value=mock_get_logged_in_user_success()
    )
    @patch.object(Auth, "get_logged_in_user_object", return_value=mock_logged_in_user())
    def test_create_portfolio_with_normal_input_is_saved_correctly(
        self, mock_user, mock_auth
    ):
        new_portfolio = {"name": "Testing Portfolio Name"}
        # Do the test:
        with app.test_client() as client:
            response = client.post(
                "/portfolio/",
                data=json.dumps(new_portfolio),
                headers={"Content-Type": "application/json"},
            )
            self.assert200(response)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual("Testing Portfolio Name", data.get("name"))

    @staticmethod
    def create_data():
        with app.test_client():
            date = datetime.datetime.now()
            date -= datetime.timedelta(6 * 30)  # date 6 months ago.
            admin_role = db.session.query(Role).filter(Role.name == "Admin").one()
            owner_role = db.session.query(Role).filter(Role.name == "Owner").one()

            user_1 = User(
                email="test@test.com",
                first_name="Foo",
                registered_on=date,
                last_name="Bar",
                username="test@test.com",
                admin=False,
            )
            db.session.add(user_1)
            user_1_role = UserRoles(user_id=user_1.id, role_id=owner_role.id)
            db.session.add(user_1_role)

            user_2 = User(
                email="test2@test.com",
                first_name="Fizz",
                registered_on=date,
                last_name="Buzz",
                username="test2@test.com",
                admin=False,
            )
            db.session.add(user_2)
            user_2_role = UserRoles(user_id=user_2.id, role_id=owner_role.id)
            db.session.add(user_2_role)

            portfolio1 = Portfolio(
                name="Test 1",
                owner=user_1,
                properties=[],
            )
            db.session.add(portfolio1)

            portfolio2 = Portfolio(
                name="Test 2",
                owner=user_2,
                properties=[],
            )
            db.session.add(portfolio2)

            db.session.commit()

            portfolios = db.session.query(Portfolio).all()
            print()

    @staticmethod
    def remove_data():
        user1 = delete(User).where(User.username == "test@test.com")
        db.session.execute(user1)

        user2 = delete(User).where(User.username == "test2@test.com")
        db.session.execute(user2)

        p1 = delete(Portfolio).where(Portfolio.name == "Test 1")
        db.session.execute(p1)

        p1 = delete(Portfolio).where(Portfolio.name == "Test 2")
        db.session.execute(p1)

        db.session.commit()
