import os
import unittest

from flask_migrate import Migrate

from app import blueprint
from app.main import create_app, db

app = create_app(os.getenv('PROPERTYMANAGER_ENV') or 'dev')
app.register_blueprint(blueprint)
app.app_context().push()
migrate = Migrate(app, db)


@app.cli.command()
def run():
    app.logger.info("run called")
    app.run(debug=True)


@app.cli.command()
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=1).run(tests) # 0 (quiet), 1 (default), 2 (verbose)
    if result.wasSuccessful():
        return 0
    return 1


@app.cli.command()
def seed():
    from seeder import seed_data
    seed_data(db)


if __name__ == '__main__':
    app.logger.info("__main__ called")
    app.run(debug=True)
