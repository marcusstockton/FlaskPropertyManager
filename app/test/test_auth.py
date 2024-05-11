import json
import unittest

from app.test.base import BaseTestCase
from werkzeug.exceptions import BadRequest


def register_admin_user(self, auth_token):
    """Regiater a new admin user"""
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json",
        "Authorization": auth_token,
    }

    return (
        self.client.post(
            "/user/",
            data=json.dumps(
                dict(
                    email="admin@user.com",
                    username="username",
                    firstname="test",
                    lastname="user",
                    password="test",
                )
            ),
            headers=headers,
        ),
    )


def register_user(self, auth_token):
    """Registers a new user. Only admin users can register new users"""
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json",
        "Authorization": auth_token,
    }

    return (
        self.client.post(
            "/user/",
            data=json.dumps(
                dict(
                    email="example@gmail.com",
                    username="username",
                    firstname="test",
                    lastname="user",
                    password="123456",
                )
            ),
            headers=headers,
        ),
    )


def login_user(self):
    """Logs in the user"""
    return self.client.post(
        "/Auth/login",
        data=json.dumps(dict(email="example@gmail.com", password="123456")),
        content_type="application/json",
    )


def login_auth_user(self):
    """Logs in the auth user"""
    return self.client.post(
        "/Auth/login",
        data=json.dumps(dict(email="admin@user.com", password="test")),
        content_type="application/json",
    )


class TestAuthBlueprint(BaseTestCase):
    """Registers the TestAuthBlueprint"""

    def test_registered_user_login(self):
        """Test for login of registered-user login"""
        with self.client:
            # user registration
            auth_login = login_auth_user(self)
            auth_header = json.loads(auth_login.text)["Authorization"]

            user_response = register_user(self, auth_header)
            if user_response is None:
                return BadRequest(user_response)

            response_data = json.loads(user_response.data.decode())
            self.assertTrue(response_data["Authorization"])
            self.assertEqual(user_response.status_code, 201)

            # registered user login
            login_response = login_user(self)
            data = json.loads(login_response.data.decode())
            self.assertTrue(data["Authorization"])
            self.assert200(login_response)

    def test_valid_logout(self):
        """Test for logout before token expires"""
        with self.client:
            # user registration
            auth_login = login_auth_user(self)
            auth_header = json.loads(auth_login.text)["Authorization"]

            user_response = register_user(self, auth_header)
            response_data = json.loads(user_response.data.decode())
            self.assertTrue(response_data["Authorization"])
            self.assertEqual(user_response.status_code, 201)

            # registered user login
            login_response = login_user(self)
            data = json.loads(login_response.data.decode())
            self.assertTrue(data["Authorization"])
            self.assertEqual(login_response.status_code, 200)

            # valid token logout
            response = self.client.post(
                "/Auth/logout",
                headers=dict(
                    Authorization="Bearer "
                    + json.loads(login_response.data.decode())["Authorization"]
                ),
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data["status"] == "success")
            self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
