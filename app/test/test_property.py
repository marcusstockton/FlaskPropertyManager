# import datetime
# import json
# from unittest.mock import patch
#
# from app.main import db
# from app.main.model import address, property
# from app.main.model.portfolio import Portfolio
# from app.main.model.user import User
# from app.main.service.auth_helper import Auth
# from app.test.base import BaseTestCase
# from app.test.helpers import mock_get_logged_in_user_success, mock_logged_in_user
# from manage import app
#
#
# class TestPropertyBlueprint(BaseTestCase):
#     @patch.object(
#         Auth, "get_logged_in_user", return_value=mock_get_logged_in_user_success()
#     )
#     @patch.object(Auth, "get_logged_in_user_object", return_value=mock_logged_in_user())
#     def test_correct_properties_are_loaded_for_portfolio(self, mock_user, mock_auth):
#         self.create_data()
#
#         with app.test_client() as client:
#             response = client.get("/portfolio/1/property/")
#             self.assert200(response)
#             data = json.loads(response.get_data(as_text=True))
#             self.assertEqual(2, len(data))
#
#             response = client.get("/portfolio/2/property/")
#             self.assert200(response)
#             data = json.loads(response.get_data(as_text=True))
#             self.assertEqual(1, len(data))
#
#     @staticmethod
#     def create_data():
#         date = datetime.datetime.now()
#         date -= datetime.timedelta(6 * 30)  # date 6 months ago.
#         user_1 = User(
#             email="test@test.com",
#             first_name="Foo",
#             registered_on=date,
#             last_name="Bar",
#             username="test@test.com",
#             admin=False,
#         )
#         db.session.add(user_1)
#
#         user_2 = User(
#             email="test2@test.com",
#             first_name="Fizz",
#             registered_on=date,
#             last_name="Buzz",
#             username="test1@test.com",
#             admin=False,
#         )
#         db.session.add(user_2)
#
#         portfolio1 = Portfolio(
#             name="Test 1",
#             owner=user_1,
#             properties=[
#                 property.Property(
#                     address=address.Address(
#                         line_1="12",
#                         line_2="Main Street",
#                         line_3="",
#                         post_code="EX11EX",
#                         town="",
#                         city="Exeter",
#                     ),
#                     owner_id=user_1.id,
#                     purchase_price=123000,
#                     purchase_date=datetime.datetime(2015, 4, 12),
#                     monthly_rental_price=985,
#                 ),
#                 property.Property(
#                     address=address.Address(
#                         line_1="Flat 12",
#                         line_2="The Mall",
#                         line_3="",
#                         post_code="TQ121RT",
#                         town="",
#                         city="Torquay",
#                     ),
#                     owner_id=user_1.id,
#                     purchase_price=89000,
#                     purchase_date=datetime.datetime(2012, 6, 24),
#                     monthly_rental_price=785,
#                 ),
#             ],
#         )
#         db.session.add(portfolio1)
#
#         portfolio2 = Portfolio(
#             name="Test 2",
#             owner=user_2,
#             properties=[
#                 property.Property(
#                     address=address.Address(
#                         line_1="189",
#                         line_2="Mildew Avenue",
#                         line_3="",
#                         post_code="KA12KA",
#                         town="",
#                         city="Cambridge",
#                     ),
#                     owner_id=user_2.id,
#                     purchase_price=2000000,
#                     purchase_date=datetime.datetime(1999, 11, 23),
#                     monthly_rental_price=1500,
#                 ),
#             ],
#         )
#         db.session.add(portfolio2)
#         db.session.commit()
