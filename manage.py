import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app.main import create_app, db
from app import blueprint
from app.main.model import user, blacklist, portfolio, property, address, tenant

app = create_app(os.getenv('PROPERTYMANAGER_ENV') or 'dev')
app.register_blueprint(blueprint)
app.app_context().push()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run(port=8089)


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def seed():
    from seeder import seed_data
    seed_data(db)


if __name__ == '__main__':
    manager.run()
