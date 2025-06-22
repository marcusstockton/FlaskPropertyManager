"""Test User Model"""
from datetime import datetime, timezone
import uuid
from app.main import db
from app.main.model.user import User
from app.test.base import BaseTestCase


class TestUserModel(BaseTestCase):
    """Tests for the User model"""

    datetime_now: datetime = datetime.now(timezone.utc)

    def test_encode_auth_token(self) -> None:
        """Tests encode auth token works"""
        user = User(
            email="testFoo@FooFighters.com",
            username="testFoo@FooFighters.com",
            registered_on=self.datetime_now,
            public_id=str(uuid.uuid4()))
        user.password = "test"
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, str))

    def test_decode_auth_token(self) -> None:
        """Tests decode auth token works"""
        user = User(
            public_id=str(uuid.uuid4()),
            email="testFoo@FooFighters.com",
            admin=False,
            first_name="Dave",
            last_name="Grohl",
            username="testFoo@FooFighters.com",
            registered_on=self.datetime_now,
        )
        user.password = "Test"
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, str))

        payload = User.decode_auth_token(auth_token)
        self.assertIsInstance(payload, dict)
        if isinstance(payload, dict):
            self.assertEqual(str(user.id), payload.get("sub"))


# if __name__ == "__main__":
#     unittest.main()
