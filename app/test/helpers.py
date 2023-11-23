########################
#### helper methods ####
########################

import json
from datetime import datetime, timedelta
from app.main.model.user import User


def mock_get_logged_in_user_success():
    mock_response_object = dict(
        status="success",
        data=dict(
            user_id=1, email="test@test.com", admin=0, registered_on=datetime.now()
        ),
    )
    return mock_response_object, 200


def mock_logged_in_user():
    """Mocks a logged in user"""
    date = datetime.now()
    date -= timedelta(6 * 30)  # date 6 months ago

    # usr = db.session.query(User).filter_by(User.username == "test@test.com").one()

    return User(
        email="test@test.com",
        first_name="Foo",
        last_name="Bar",
        username="test@test.com",
        admin=False,
    )


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
