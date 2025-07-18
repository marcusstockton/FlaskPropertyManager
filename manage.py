"""Entry point for the flask app."""

import os
import unittest
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from app import blueprint
from app.main import create_app, db
from seeder import seed_data

app: Flask = create_app(os.getenv("PROPERTYMANAGER_ENV") or "local")
app.register_blueprint(blueprint)

with app.app_context():
    migrate = Migrate(app, db)
    ma = Marshmallow(app)


@app.cli.command()
def run() -> None:
    """Command to run the app."""
    app.logger.info("run called")
    app.run(debug=True)


@app.cli.command()
def test() -> int:
    """Runs the unit tests."""
    import sys
    tests: unittest.TestSuite = unittest.TestLoader().discover(
        "app/test", pattern="test*.py"
    )
    result = unittest.TextTestRunner(verbosity=0).run(tests)
    sys.exit(not result.wasSuccessful())


@app.cli.command()
def seed() -> None:
    """Reseeds the database with new data"""
    seed_data(db)


if __name__ == "__main__":
    app.logger.info("__main__ called")
    app.run(debug=True)