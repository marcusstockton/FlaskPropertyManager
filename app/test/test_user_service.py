# from http import HTTPStatus

# from app.main.service.user_service import save_new_user, get_a_user
# from app.test.base import BaseTestCase


# class TestUserService(BaseTestCase):
#     """Test User Service unit tests"""

#     def test_new_user_created_with_owner_role(self):
#         json_user = {
#             "email": "test3@test.com",
#             "username": "testUser3",
#             "password": "abc123",
#             "first_name": "Foo",
#             "last_name": "Bar",
#             "date_of_birth": "1993-7-12",
#         }
#         result = save_new_user(json_user)
#         (response, status_code) = result
#         self.assertEqual(status_code, HTTPStatus.CREATED)
#         self.assertEqual(response["status"], "success")

#         # get the user id that was created, and check role
#         new_user = get_a_user(response["user_id"])
# self.assertEqual(len(new_user.roles), 1)
# self.assertEqual(new_user.roles[0].name, "Owner")
