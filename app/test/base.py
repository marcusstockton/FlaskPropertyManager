from datetime import datetime
from uuid import uuid4
from flask_testing import TestCase
from sqlalchemy.exc import IntegrityError

from app.main import create_app, db
from app.main.model import user
from manage import app


class BaseTestCase(TestCase):
    """Base Tests"""

    def create_app(self):
        app.config.from_object("app.main.config.TestingConfig")
        return create_app("test")

    def setUp(self):
        # if "_test.db" not in str(db.engine.url):
        #     raise ValueError("Not using test database!")
        # print("Engine URL: %s", db.engine.url)
        app.logger.info("Setting up %s", db.engine.url)
        db.session.remove()
        db.drop_all()
        db.create_all()  # create all the tables
        self.seed_test_data()
        db.session.commit()

    def tearDown(self):
        app.logger.info("Tearing down db %s", db.engine.url)
        db.session.remove()
        db.drop_all()

    def seed_test_data(self):
        """Seeds the roles and a test admin user"""
        app.logger.info("Seeding test database %s", db.engine.url)
        q = db.session.query(user.Role).filter_by(name="Admin")
        admin_role_exists = db.session.query(
            q.exists()
        ).scalar()  # returns True or False
        if not admin_role_exists:
            admin_role = user.Role(name="Admin")
            owner_role = user.Role(name="Owner")
            db.session.add_all([owner_role, admin_role])

        q = db.session.query(user.User).filter_by(email="admin@user.com")
        admin_user_exists = db.session.query(q.exists()).scalar()
        if not admin_user_exists:
            admin_user = user.User(
                email="admin@user.com",
                username="AdminUser",
                first_name="Marcus",
                last_name="Stockton",
                registered_on=datetime.now(),
                public_id=str(uuid4()),
                date_of_birth=datetime(2002, 3, 31),
                admin=True,
            )
            admin_user.password = "test"
            admin_user.roles.append(admin_role)
            db.session.add_all([admin_user])
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            app.logger.error("Failed seeding test database: %s", e, exc_info=True)
