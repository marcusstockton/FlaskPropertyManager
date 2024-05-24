"""Portfolio Service for interacting with portfolios"""

from typing import List


from flask import current_app
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError, NoResultFound, MultipleResultsFound
from sqlalchemy.orm import lazyload
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError
from bleach import clean

from app.main import db
from app.main.model.portfolio import Portfolio
from app.main.model.user import User


def get_all_portfolios_for_user(user: User) -> List[Portfolio]:
    """Gets all Portfolios for the logged in user"""
    if user.admin:
        return Portfolio.query.all()
    else:
        portfolios: List[Portfolio] = (
            Portfolio.query.filter_by(owner_id=user.id)
            .options(lazyload(Portfolio.owner), lazyload(Portfolio.properties))
            .all()
        )
        return portfolios


def get_portfolio_by_id(user_id: int, portfolio_id: int) -> Portfolio:
    """Returns the portfolio from the given portfolio Id"""
    try:
        current_app.logger.info(f"Getting portfolio by {portfolio_id}")
        portfolio = (
            Portfolio.query.filter_by(owner_id=user_id)
            .filter_by(id=portfolio_id)
            .options(
                lazyload(Portfolio.owner),
                lazyload(Portfolio.properties),
            )
            .one()
        )
        return portfolio
    except NoResultFound as err:
        error_message = f"Portfolio not found for userid: {user_id} and portfolio_id {portfolio_id}. Error {err}"
        current_app.logger.error(error_message)
        raise NotFound(error_message) from err

    except MultipleResultsFound as err:
        error = f"Multiple portfolio's not found for userid {user_id} and portfolio_id {portfolio_id}. Error: {err}"
        current_app.logger.error(error)
        raise BadRequest(error) from err


def save_new_portfolio(data, user_id) -> Portfolio:
    """Creates a new Portfolio"""
    sanitised_name = clean(data["name"])
    current_app.logger.info(f"Adding portfolio {sanitised_name}")
    portfolio = (
        Portfolio.query.filter_by(name=sanitised_name)
        .filter_by(owner_id=user_id)
        .first()
    )
    if not portfolio:
        new_portfolio = Portfolio(
            name=sanitised_name,
            owner_id=user_id,
        )
        save_changes(new_portfolio)
        current_app.logger.info(f"Portfolio {sanitised_name} successfully added.")
        return new_portfolio
    else:
        raise BadRequest("Portfolio already exists.")


def update_portfolio(portfolio_id: int, data: dict) -> Portfolio:
    """Update a portfolio"""
    portfolio_query = Portfolio.query.filter_by(id=portfolio_id).one()
    if not portfolio_query:
        raise NotFound("Portfolio not found.")
    try:
        stmt = update(Portfolio).where(Portfolio.id == portfolio_id).values(data)
        db.session.execute(stmt)
        db.session.commit()
        return portfolio_query
    except IntegrityError as err:
        raise InternalServerError(err.statement) from err
    except Exception as e:
        raise InternalServerError(repr(e)) from e


def delete_portfolio_by_id(user, portfolio_id):
    """Deletes the Portfolio and related data"""
    portfolio = (
        Portfolio.query.filter_by(id=portfolio_id)
        .filter_by(id=portfolio_id)
        .options(
            lazyload(Portfolio.owner),
            lazyload(Portfolio.properties),
            lazyload(Portfolio.properties.images),
            lazyload(Portfolio.properties),
        )
        .scalar()
    )
    if portfolio is not None:
        if portfolio.owner_id == user.id:
            portfolio.delete()


def save_changes(data) -> None:
    """Saves changes"""
    db.session.add(data)
    db.session.commit()
