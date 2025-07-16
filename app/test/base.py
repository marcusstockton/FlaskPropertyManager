from datetime import datetime
from uuid import uuid4
from flask_testing import TestCase
from flask_migrate import Migrate, upgrade
from sqlalchemy.exc import IntegrityError

# Import all models that need tables before calling db.create_all().
# This will ensure all tables, including blacklist_tokens, are created for your tests.
from app.main.model.user import User, Role
from app.main.model.portfolio import Portfolio
from app.main.model.property import Property
from app.main.model.address import Address
from app.main.model.tenant import Tenant
from app.main.model.blacklist import BlacklistToken

from app.main import create_app, db
from app.main.model import user
from app import blueprint


class BaseTestCase(TestCase):
    """Base Tests"""

    def create_app(self):
        return create_app("test")

    def setUp(self):
        self.app.register_blueprint(blueprint)

        self.app.logger.info("Setting up %s", db.engine.url)
        with self.app.app_context():
           # Initialize Flask-Migrate
            migrate = Migrate(self.app, db)
            # Run migrations to create all tables
            upgrade()
            self.seed_test_data()
            db.session.commit()

    def tearDown(self):
        self.app.logger.info("Tearing down db %s", db.engine.url)
        db.session.remove()
        db.drop_all()

    def seed_test_data(self):
        """Seeds the roles and a test admin user"""
        self.app.logger.info("Seeding test database %s", db.engine.url)
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
            self.app.logger.error(
                "Failed seeding test database: %s", e, exc_info=True)
