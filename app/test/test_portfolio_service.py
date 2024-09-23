from datetime import datetime, timezone

from app.main import db
from app.main.model.portfolio import Portfolio
from app.main.model.user import User
from app.main.service.portfolio_service import (
    get_all_portfolios_for_user,
    get_portfolio_by_id,
    save_new_portfolio,
)
from app.test.base import BaseTestCase
from werkzeug.exceptions import NotFound


from manage import app


def create_owner_user() -> None:
    """Creates a non-admin user and returns the auth token"""
    datetime_now = datetime.now(timezone.utc)
    user = User(email="user@testing.com", registered_on=datetime_now, admin=False)
    user.password = "test"
    db.session.add(user)
    db.session.commit()


class TestPortfolioServiceBlueprint(BaseTestCase):
    """Test class for Portfolio services"""

    def test_get_all_portfolios_for_user_returns_all_portfolios_for_admin_user(self):
        """Tests that the admin user can see all portfolios"""

        admin_user = db.session.query(User).filter_by(email="admin@user.com").scalar()
        create_owner_user()

        owner_user = db.session.query(User).filter_by(email="user@testing.com").scalar()
        db.session.add(Portfolio(name="Test Portfolio", owner=admin_user))
        db.session.add(Portfolio(name="Test Portfolio2", owner=admin_user))
        db.session.add(Portfolio(name="Test Portfolio 3", owner=owner_user))
        db.session.commit()

        results = get_all_portfolios_for_user(admin_user)
        self.assertEqual(3, len(results))

    def test_get_all_portfolios_for_user_returns_portfolios_for_owner_user(self):
        """Tests that the portfolio service correctly returns data for the owner user"""

        admin_user = db.session.query(User).filter_by(email="admin@user.com").scalar()
        create_owner_user()

        owner_user = db.session.query(User).filter_by(email="user@testing.com").scalar()
        db.session.add(Portfolio(name="Test Portfolio", owner=admin_user))
        db.session.add(Portfolio(name="Test Portfolio2", owner=admin_user))
        db.session.add(Portfolio(name="Test Portfolio 3", owner=owner_user))
        db.session.commit()

        results = get_all_portfolios_for_user(owner_user)
        self.assertEqual(1, len(results))

    def test_get_portfolio_by_id_returns_correct_portfolio(self):
        """Tests that the get_portfolio_by_id service returns the correct porfolio"""
        create_owner_user()
        owner_user = db.session.query(User).filter_by(email="user@testing.com").scalar()

        db.session.add(Portfolio(name="Portfolio One", owner=owner_user))
        db.session.add(Portfolio(name="Portfolio Two", owner=owner_user))
        db.session.commit()

        portfolio_1 = (
            db.session.query(Portfolio.id).filter_by(name="Portfolio One").scalar()
        )

        result = get_portfolio_by_id(owner_user.id, portfolio_id=portfolio_1)
        self.assertEqual("Portfolio One", result.name)

    def test_get_portfolio_by_id_handles_incorrect_user(self):
        """Tests that the get_portfolio_by_id service returns the correct porfolio"""
        create_owner_user()
        owner_user = db.session.query(User).filter_by(email="user@testing.com").scalar()
        admin_user = db.session.query(User).filter_by(email="admin@user.com").scalar()

        db.session.add(Portfolio(name="Portfolio One", owner=owner_user))
        db.session.add(Portfolio(name="Portfolio Two", owner=owner_user))
        db.session.commit()

        portfolio_1 = (
            db.session.query(Portfolio.id).filter_by(name="Portfolio One").scalar()
        )

        self.assertRaises(NotFound, get_portfolio_by_id, admin_user.id, portfolio_1)
