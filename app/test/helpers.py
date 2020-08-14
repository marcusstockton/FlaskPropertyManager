########################
#### helper methods ####
########################

from manage import app
import json


def register(self, email, username, password):
    return self.client.post(
        '/user/',
        data=json.dumps(dict(
            email=email,
            username=username,
            password=password
        )),
        content_type='application/json'
    )


def login(self, email, password):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            email=email,
            password=password
        )),
        content_type='application/json'
    )


def logout(self):
    return self.client.get(
        '/logout',
        follow_redirects=True
    )
