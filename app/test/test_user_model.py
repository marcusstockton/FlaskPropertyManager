from datetime import datetime, timezone
import unittest

from app.main import db
from app.main.model.user import User
from app.test.base import BaseTestCase


class TestUserModel(BaseTestCase):


    datetime_now = datetime.now(timezone.utc)

    def test_encode_auth_token(self):
        user = User(
            email="testFoo@FooFighters.com",
            registered_on=self.datetime_now
        )
        user.password = "test"
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, str))

    def test_decode_auth_token(self):
        user = User(
            email="testFoo@FooFighters.com",
            admin=False,
            first_name="Dave",
            last_name="Grohl",
            username="testFoo@FooFighters.com",
            registered_on=self.datetime_now
        )
        user.password = "Test"
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, str))
        self.assertTrue(User.decode_auth_token(auth_token) == 4)


if __name__ == "__main__":
    unittest.main()
