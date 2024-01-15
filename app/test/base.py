from datetime import datetime, timezone, timedelta
from uuid import uuid4
from flask_testing import TestCase
from app.main import db
from app.main.model.user import Role, User
from manage import app


class BaseTestCase(TestCase):
    """Base Tests"""

    def create_app(self):
        app.config.from_object("app.main.config.TestingConfig")
        return app

    def setUp(self):
        db.session.remove()  # blat the db
        db.drop_all()  # blat the db
        db.create_all()  # create all the tables
        if Role.query.first() is None:
            owner_role = Role(name="Owner")
            admin_role = Role(name="Admin")
            db.session.add(owner_role)
            db.session.add(admin_role)

            admin_user = User(
                email="admin@user.com",
                username="AdminUser",
                first_name="Admin",
                last_name="User",
                admin=True,
                registered_on=datetime.now(),
                public_id=str(uuid4()),
                date_of_birth=datetime(2001, 1, 1),
            )
            admin_user.password = "test"
            admin_user.roles.append(admin_role)
            db.session.add(admin_user)

            date = datetime.now(timezone.utc)
            date -= timedelta(6 * 30)  # date 6 months ago.

            user_1 = User(
                email="test@test.com",
                first_name="Foo",
                registered_on=date,
                last_name="Bar",
                username="test@test.com",
                admin=False,
            )
            db.session.add(user_1)
            user_1.roles.append(owner_role)
            db.session.add(user_1)

            user_2 = User(
                email="test2@test.com",
                first_name="Fizz",
                registered_on=date,
                last_name="Buzz",
                username="test2@test.com",
                admin=False,
            )
            db.session.add(user_2)
            user_2.roles.append(owner_role)
            db.session.add(user_2)


        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
