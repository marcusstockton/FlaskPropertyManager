from flask_testing import TestCase
from app.main import db
from app.main.model.user import Role
from manage import app


class BaseTestCase(TestCase):
    """ Base Tests """
    def create_app(self):
        app.config.from_object('app.main.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        if Role.query.first() is None:
            owner_role = Role(name="Owner")
            admin_role = Role(name="Admin")
            db.session.add(owner_role)
            db.session.add(admin_role)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
