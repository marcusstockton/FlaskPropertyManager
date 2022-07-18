from http import HTTPStatus

from app.main.service import user_service
from app.test.base import BaseTestCase


class TestUserService(BaseTestCase):
    def test_new_user_created_with_owner_role(self):
        json_user = {"email": "test@test.com", "username": "testUser", "password": "abc123", "first_name": "Foo",
                     "last_name": "Bar", "date_of_birth": "1993-7-12"}
        result = user_service.save_new_user(json_user)
        (response, status_code) = result
        self.assertEqual(status_code, HTTPStatus.CREATED)
        self.assertEqual(response['status'], 'success')

        # get the user id that was created, and check role
        new_user = user_service.get_a_user(response['user_id'])
        self.assertEqual(len(new_user.roles), 1)
        self.assertEqual(new_user.roles[0].name, 'Owner')
