from datetime import datetime, timezone
from typing import List
import uuid

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
from unittest.mock import patch, MagicMock

from manage import app


def create_user(email: str, username: str, admin: bool = False, password: str = "test") -> None:
    """Creates a user with the given details."""
    datetime_now = datetime.now(timezone.utc)
    user = User(
        email=email,
        username=username,
        registered_on=datetime_now,
        admin=admin,
        public_id=str(uuid.uuid4()),
    )
    user.password = password
    db.session.add(user)
    db.session.commit()


def create_owner_user() -> None:
    """Creates a non-admin user with predefined details."""
    create_user(email="user@testing.com",
                username="user@testing.com", admin=False, password="test")


def create_portfolio(name: str, owner: User) -> None:
    """Helper function to create a portfolio for a given user."""
    db.session.add(Portfolio(name=name, owner=owner))
    db.session.commit()


class TestPortfolioServiceBlueprint(BaseTestCase):
    """Test class for Portfolio services"""

    def setUp(self):
        # Patch redis_client in the portfolio_service module
        patcher = patch(
            'app.main.service.portfolio_service.redis_client', autospec=True)
        self.mock_redis = patcher.start()
        self.addCleanup(patcher.stop)
        # Optionally, set up mock return values
        self.mock_redis.get.return_value = None
        self.mock_redis.setex.return_value = True

        # Create all tables before each test
        db.create_all()

        # Seed an admin user for tests
        from datetime import datetime, timezone
        import uuid
        admin_user = User(
            email="admin@user.com",
            username="admin@user.com",
            registered_on=datetime.now(timezone.utc),
            admin=True,
            public_id=str(uuid.uuid4()),
        )
        admin_user.password = "test"
        db.session.add(admin_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_all_portfolios_for_user_returns_all_portfolios_for_admin_user(
        self,
    ) -> None:
        """Tests that the admin user can see all portfolios"""

        admin_user = db.session.query(User).filter_by(
            email="admin@user.com").scalar()
        create_owner_user()

        owner_user = db.session.query(User).filter_by(
            email="user@testing.com").scalar()
        create_portfolio("Test Portfolio", admin_user)
        create_portfolio("Test Portfolio2", admin_user)
        create_portfolio("Test Portfolio 3", owner_user)

        results = get_all_portfolios_for_user(admin_user)
        self.assertEqual(
            3, len(results), "Admin user should see all portfolios")

    def test_get_all_portfolios_for_user_returns_portfolios_for_owner_user(
        self,
    ) -> None:
        """Tests that the portfolio service correctly returns data for the owner user"""

        admin_user = db.session.query(User).filter_by(
            email="admin@user.com").scalar()
        create_owner_user()

        owner_user = db.session.query(User).filter_by(
            email="user@testing.com").scalar()
        create_portfolio("Test Portfolio", admin_user)
        create_portfolio("Test Portfolio2", admin_user)
        create_portfolio("Test Portfolio 3", owner_user)

        results: List[Portfolio] = get_all_portfolios_for_user(owner_user)
        self.assertEqual(
            1, len(results), "Owner user should see only their portfolios")

    def test_get_portfolio_by_id_returns_correct_portfolio(self) -> None:
        """Tests that the get_portfolio_by_id service returns the correct portfolio."""
        create_owner_user()
        owner_user = db.session.query(User).filter_by(
            email="user@testing.com").scalar()

        create_portfolio("Portfolio One", owner_user)
        create_portfolio("Portfolio Two", owner_user)

        portfolio_1 = (
            db.session.query(Portfolio.id).filter_by(
                name="Portfolio One").scalar()
        )
        self.assertIsNotNone(portfolio_1, "Portfolio ID should not be None")

        result = get_portfolio_by_id(owner_user, portfolio_id=portfolio_1)
        self.assertEqual("Portfolio One", result.name,
                         "Portfolio name mismatch")
        self.assertEqual(owner_user.id, result.owner.id, "Owner ID mismatch")

    def test_get_portfolio_by_id_handles_incorrect_user(self) -> None:
        """Tests that the get_portfolio_by_id service raises NotFound for incorrect user."""
        create_owner_user()
        create_user(email="user2@testing.com", username="user2@testing.com")
        owner_user = db.session.query(User).filter_by(
            email="user@testing.com").scalar()
        owner_user_2 = db.session.query(User).filter_by(
            email="user2@testing.com").scalar()

        create_portfolio("Portfolio One", owner_user)
        create_portfolio("Portfolio Two", owner_user)

        portfolio_1 = (
            db.session.query(Portfolio.id).filter_by(
                name="Portfolio One").scalar()
        )
        self.assertIsNotNone(portfolio_1, "Portfolio ID should not be None")

        self.assertRaises(
            NotFound,
            get_portfolio_by_id,
            owner_user_2,
            portfolio_1,
        )
