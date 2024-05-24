from datetime import datetime, timezone
import json

from unittest.mock import patch
from app.main import db
from app.main.model.portfolio import Portfolio
from app.main.model.user import User
from app.test.base import BaseTestCase
from app.test.helpers import mock_get_all_portfolios_for_user
from werkzeug.exceptions import NotFound

from manage import app


def create_admin_user() -> str:
    """Creates an admin user and returns the auth token"""
    datetime_now = datetime.now(timezone.utc)
    user = User(email="admin@testing.com", registered_on=datetime_now, admin=True)
    user.password = "test"
    db.session.add(user)
    db.session.commit()
    auth_token = user.encode_auth_token(user.id)
    if isinstance(auth_token, str):
        return auth_token
    return ""


def create_owner_user() -> str:
    """Creates a non-admin user and returns the auth token"""
    datetime_now = datetime.now(timezone.utc)
    user = User(email="user@testing.com", registered_on=datetime_now, admin=False)
    user.password = "test"
    db.session.add(user)
    db.session.commit()
    auth_token = user.encode_auth_token(user.id)
    if isinstance(auth_token, str):
        return auth_token
    return ""


class TestPortfolioBlueprint(BaseTestCase):
    """Test class for Portfolio endpoints"""

    @patch("app.main.controller.portfolio_controller.get_all_portfolios_for_user")
    def test_users_can_only_see_their_own_portfolios(self, mock_portfolios):
        """Checks that users can only see their own portfolios"""
        access_token = create_admin_user()
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
            "Authorization": access_token,
        }

        mock_portfolios.return_value = [
            portfolio for portfolio in mock_get_all_portfolios_for_user()
        ]

        with app.test_client() as client:
            response = client.get("/portfolio/", headers=headers)
            self.assert200(response)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(1, len(data))

    @patch("app.main.controller.portfolio_controller.get_portfolio_by_id")
    def test_correct_portfolio_is_returned_for_id(self, mock_portfolios):
        """Tests that the correct portfolio is returned"""
        access_token = create_admin_user()
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
            "Authorization": access_token,
        }

        mock_portfolios.return_value = [
            portfolio for portfolio in mock_get_all_portfolios_for_user()
        ]

        with app.test_client() as client:
            response = client.get("/portfolio/1", headers=headers)
            data = response.get_json()
            self.assertEqual("Test Portfolio One", data[0].get("name"))
            self.assertEqual("1", data[0].get("id"))

    def test_portfolio_is_not_returned_for_non_owner_user_id(self):
        """Unit test to test that users cannot access other user records"""
        access_token = create_owner_user()
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
            "Authorization": access_token,
        }
        with patch(
            "app.main.controller.portfolio_controller.get_portfolio_by_id"
        ) as mock_get_portfolio_by_id:
            mock_get_portfolio_by_id.side_effect = NotFound()
            with app.test_client() as client:
                response = client.get("/portfolio/2", headers=headers)
                self.assert404(response)

    def test_update_portfolio_works_with_correct_data_and_user(self):
        access_token = create_owner_user()
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
            "Authorization": access_token,
        }

        dict_data = {"id": "1", "name": "Updated Test 1"}
        with patch(
            "app.main.controller.portfolio_controller.update_portfolio"
        ) as update_patch:
            update_patch.return_value = Portfolio(name=dict_data["name"])
            with app.test_client() as client:
                response = client.put(
                    "/portfolio/1",
                    data=json.dumps(dict_data),
                    headers=headers,
                )
                self.assert200(response)
                data = json.loads(response.get_data(as_text=True))

                self.assertEqual("Updated Test 1", data.get("name"))


#     #
#     # @patch.object(
#     #     Auth, "get_logged_in_user", return_value=mock_get_logged_in_user_success()
#     # )
#     # @patch.object(Auth, "get_logged_in_user_object", return_value=mock_logged_in_user())
#     # def test_update_portfolio_fails_if_incorrect_data_used(self, mock_user, mock_auth):
#     #     self.create_data()
#     #     dict_data = {"id": "2", "name": "Updated Test 1"}
#     #     with app.test_client() as client:
#     #         response = client.put(
#     #             "/portfolio/1",
#     #             data=json.dumps(dict_data),
#     #             headers={"Content-Type": "application/json"},
#     #         )
#     #         self.assertEqual(response.status_code, 500)
#     #
#     # @patch.object(
#     #     Auth, "get_logged_in_user", return_value=mock_get_logged_in_user_success()
#     # )
#     # @patch.object(Auth, "get_logged_in_user_object", return_value=mock_logged_in_user())
#     # def test_get_portfolio_returns_correct_property_count_with_correct_data_and_user(
#     #     self, mock_user, mock_auth
#     # ):
#     #     self.create_data()
#     #     # get portfolio to append a property or two to it
#     #     portfolio = db.session.query(Portfolio).filter(Portfolio.id == 1).one()
#     #     property1 = Property(
#     #         portfolio_id=portfolio.id,
#     #         owner_id=1,
#     #         purchase_price=32000,
#     #         purchase_date=datetime.datetime(2020, 5, 17),
#     #         monthly_rental_price=670,
#     #         address=Address(
#     #             line_1="Test Line 1",
#     #             line_2="Test Line 2",
#     #             post_code="EX11EX",
#     #             city="Exeter",
#     #         ),
#     #     )
#     #     portfolio.properties.append(property1)
#     #     db.session.commit()
#     #
#     #     # Do the test:
#     #     with app.test_client() as client:
#     #         response = client.get("/portfolio/1")
#     #         self.assert200(response)
#     #         data = json.loads(response.get_data(as_text=True))
#     #
#     #         self.assertEqual(1, data.get("property_count"))
#     #
#     # @patch.object(
#     #     Auth, "get_logged_in_user", return_value=mock_get_logged_in_user_success()
#     # )
#     # @patch.object(Auth, "get_logged_in_user_object", return_value=mock_logged_in_user())
#     # def test_create_portfolio_with_xss_input_is_sanitized(self, mock_user, mock_auth):
#     #     new_portfolio = {"name": "<script>alert();</script>"}
#     #     # Do the test:
#     #     with app.test_client() as client:
#     #         response = client.post(
#     #             "/portfolio/",
#     #             data=json.dumps(new_portfolio),
#     #             headers={"Content-Type": "application/json"},
#     #         )
#     #         self.assert200(response)
#     #         data = json.loads(response.get_data(as_text=True))
#     #         self.assertEqual("&lt;script&gt;alert();&lt;/script&gt;", data.get("name"))
#     #
#     # @patch.object(
#     #     Auth, "get_logged_in_user", return_value=mock_get_logged_in_user_success()
#     # )
#     # @patch.object(Auth, "get_logged_in_user_object", return_value=mock_logged_in_user())
#     # def test_create_portfolio_with_normal_input_is_saved_correctly(
#     #     self, mock_user, mock_auth
#     # ):
#     #     new_portfolio = {"name": "Testing Portfolio Name"}
#     #     # Do the test:
#     #     with app.test_client() as client:
#     #         response = client.post(
#     #             "/portfolio/",
#     #             data=json.dumps(new_portfolio),
#     #             headers={"Content-Type": "application/json"},
#     #         )
#     #         self.assert200(response)
#     #         data = json.loads(response.get_data(as_text=True))
#     #         self.assertEqual("Testing Portfolio Name", data.get("name"))
#     #
#     @staticmethod
#     def create_data():
#         user_1 = db.session.query(User).filter(User.username == "test@test.com").one()
#         user_2 = db.session.query(User).filter(User.username == "test2@test.com").one()

#         portfolio1 = Portfolio(
#             name="Test 1",
#             owner=user_1,
#             properties=[],
#         )
#         db.session.add(portfolio1)

#         portfolio2 = Portfolio(
#             name="Test 2",
#             owner=user_2,
#             properties=[],
#         )
#         db.session.add(portfolio2)

#         db.session.commit()

#         portfolios = db.session.query(Portfolio).all()
#         print()
#     #
#     # @staticmethod
#     # def remove_data():
#     #     user1 = delete(User).where(User.username == "test@test.com")
#     #     db.session.execute(user1)
#     #
#     #     user2 = delete(User).where(User.username == "test2@test.com")
#     #     db.session.execute(user2)
#     #
#     #     p1 = delete(Portfolio).where(Portfolio.name == "Test 1")
#     #     db.session.execute(p1)
#     #
#     #     p1 = delete(Portfolio).where(Portfolio.name == "Test 2")
#     #     db.session.execute(p1)
#     #
#     #     db.session.commit()

# if __name__ == "__main__":
#     unittest.main()
