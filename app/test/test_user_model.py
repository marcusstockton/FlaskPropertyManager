import datetime
import unittest

from app.main import db
from app.main.model.user import User
from app.test.base import BaseTestCase


class TestUserModel(BaseTestCase):
    def test_encode_auth_token(self):
        user = User(
            email="test@test.com",
            registered_on=datetime.datetime.utcnow(),
        )
        user.password = "test"
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, str))

    def test_decode_auth_token(self):
        user = User(
            email="test@test.com",
            admin=False,
            first_name="Dave",
            last_name="Grohl",
            username="test@test.com",
            registered_on=datetime.datetime.now(),
        )
        user.password = "Test"
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, str))
        self.assertTrue(User.decode_auth_token(auth_token) == 2)


if __name__ == "__main__":
    unittest.main()
