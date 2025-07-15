from datetime import datetime, timezone
import json
from unittest.mock import patch
import uuid
from werkzeug.exceptions import NotFound
from werkzeug.test import TestResponse
from app.main.schemas.portfolio import PortfolioSchema

from app.main import db
from app.main.model.portfolio import Portfolio
from app.main.model.user import User
from app.test.base import BaseTestCase
from app.test.helpers import mock_get_all_portfolios_for_user, mock_portfolio_by_id


from manage import app


def create_admin_user() -> str:
    """Creates an admin user and returns the auth token"""
    datetime_now: datetime = datetime.now(timezone.utc)
    user = User(
        email="admin@testing.com",
        username="admin@testing.com", 
        registered_on=datetime_now, 
        public_id=str(uuid.uuid4()),
        admin=True)
    user.password = "test"
    db.session.add(user)
    db.session.commit()
    auth_token = user.encode_auth_token(user.id)
    if isinstance(auth_token, str):
        return auth_token
    return ""


def create_owner_user() -> str:
    """Creates a non-admin user and returns the auth token"""
    datetime_now: datetime = datetime.now(timezone.utc)
    user = User(
        email="user@testing.com", 
        username="user@testing.com",
        registered_on=datetime_now, 
        admin=False,
        public_id=str(uuid.uuid4()))
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
    def test_users_can_only_see_their_own_portfolios(self, mock_portfolios) -> None:
        """Checks that users can only see their own portfolios"""
        access_token: str = create_admin_user()
        headers: dict[str, str] = {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
            "Authorization": access_token,
        }

        mock_portfolios.return_value = [
            portfolio for portfolio in mock_get_all_portfolios_for_user()
        ]

        with app.test_client() as client:
            response: TestResponse = client.get("/portfolio/", headers=headers)
            self.assert200(response)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(1, len(data))

    @patch("app.main.controller.portfolio_controller.get_portfolio_by_id")
    def test_correct_portfolio_is_returned_for_id(self, mock_portfolios) -> None:
        """Tests that the correct portfolio is returned"""
        access_token: str = create_admin_user()
        headers: dict[str, str] = {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
            "Authorization": access_token,
        }

        # Filter and select the first portfolio with id == 1
        portfolio: Portfolio | None = next(
            (p for p in mock_get_all_portfolios_for_user() if p.id == 1),
            None
        )
        app.logger.info(f"Filtered portfolio object: {portfolio}")
        app.logger.info(f"Serialized portfolio: {PortfolioSchema().dump(portfolio)}")
        
        assert portfolio is not None, "No portfolio with id == 1 found in mock data"
        
        mock_portfolios.return_value = PortfolioSchema().dump(portfolio)

        with app.test_client() as client:
            response: TestResponse = client.get("/portfolio/1", headers=headers)
            data = response.get_json()
            app.logger.info(f"Response data: {data}")
            self.assertEqual("Test Portfolio One", data.get("name"))
            self.assertEqual(1, data.get("id"))

    def test_portfolio_is_not_returned_for_non_owner_user_id(self) -> None:
        """Unit test to test that users cannot access other user records"""
        access_token: str = create_owner_user()
        headers: dict[str, str] = {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
            "Authorization": access_token,
        }
        with patch(
            "app.main.controller.portfolio_controller.get_portfolio_by_id"
        ) as mock_get_portfolio_by_id:
            mock_get_portfolio_by_id.side_effect = NotFound()
            with app.test_client() as client:
                response: TestResponse = client.get("/portfolio/2", headers=headers)
                self.assert404(response)

    def test_update_portfolio_works_with_correct_data_and_user(self) -> None:
        """Unit test to made sure correct user returns correct data"""
        access_token: str = create_owner_user()
        headers: dict[str, str] = {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
            "Authorization": access_token,
        }

        dict_data: dict[str, str] = {"id": "1", "name": "Updated Test 1"}
        with patch(
            "app.main.controller.portfolio_controller.update_portfolio"
        ) as update_patch:
            update_patch.return_value = Portfolio(name=dict_data["name"])
            with app.test_client() as client:
                response: TestResponse = client.put(
                    "/portfolio/1",
                    data=json.dumps(dict_data),
                    headers=headers,
                )
                self.assert200(response)
                data = json.loads(response.get_data(as_text=True))

                self.assertEqual("Updated Test 1", data.get("name"))

    def test_update_portfolio_fails_if_incorrect_data_used(self) -> None:
        """Handle invalid user updating portfolio"""
        access_token: str = create_owner_user()
        headers: dict[str, str] = {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
            "Authorization": access_token,
        }
        with patch(
            "app.main.controller.portfolio_controller.update_portfolio"
        ) as update_patch:
            update_patch.side_effect = NotFound()
            dict_data: dict[str, str] = {"id": "2", "name": "Updated Test 1"}
            with app.test_client() as client:
                response: TestResponse = client.put(
                    "/portfolio/2",
                    data=json.dumps(dict_data),
                    headers=headers,
                )
                self.assertEqual(response.status_code, 404)

    def test_get_portfolio_returns_correct_property_count_with_correct_data_and_user(
        self,
    ) -> None:
        """Tests that get portfolio by id returns portfolio and properties"""
        access_token: str = create_owner_user()
        headers: dict[str, str] = {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
            "Authorization": access_token,
        }

        # Do the test:
        with patch(
            "app.main.controller.portfolio_controller.get_portfolio_by_id"
        ) as mock_get_portfolio_by_id:
            mock_get_portfolio_by_id.return_value = mock_portfolio_by_id()
            with app.test_client() as client:
                response: TestResponse = client.get("/portfolio/1", headers=headers)
                self.assert200(response)
                data = json.loads(response.get_data(as_text=True))

                self.assertEqual(1, data.get("property_count"))

    def test_create_portfolio_with_xss_input_is_sanitized(self) -> None:
        """Tests that adding potenially dangerous xss script into the name will get sanitised"""
        new_portfolio: dict[str, str] = {"name": "<script>alert();</script>"}

        access_token: str = create_owner_user()
        headers: dict[str, str] = {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
            "Authorization": access_token,
        }
        with patch(
            "app.main.controller.portfolio_controller.save_new_portfolio"
        ) as mock_save_new_portfolio:
            mock_save_new_portfolio.return_value = Portfolio(
                name="&lt;script&gt;alert();&lt;/script&gt;"
            )
            # Do the test:
            with app.test_client() as client:
                response: TestResponse = client.post(
                    "/portfolio/",
                    data=json.dumps(new_portfolio),
                    headers=headers,
                )
                self.assert200(response)
                data = json.loads(response.get_data(as_text=True))
                self.assertEqual(
                    "&lt;script&gt;alert();&lt;/script&gt;", data.get("name")
                )

    def test_create_portfolio_with_normal_input_is_saved_correctly(self) -> None:
        """Tests that adding non xss text into the name will work"""
        new_portfolio: dict[str, str] = {"name": "Testing Portfolio Name"}

        access_token: str = create_owner_user()
        headers: dict[str, str] = {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
            "Authorization": access_token,
        }
        with patch(
            "app.main.controller.portfolio_controller.save_new_portfolio"
        ) as mock_save_new_portfolio:
            mock_save_new_portfolio.return_value = Portfolio(
                name="Testing Portfolio Name"
            )
            # Do the test:
            with app.test_client() as client:
                response: TestResponse = client.post(
                    "/portfolio/",
                    data=json.dumps(new_portfolio),
                    headers=headers,
                )
                self.assert200(response)
                data = json.loads(response.get_data(as_text=True))
                self.assertEqual("Testing Portfolio Name", data.get("name"))
