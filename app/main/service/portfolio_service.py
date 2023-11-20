import datetime
from typing import List, Dict

from flask import current_app
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError, NoResultFound, MultipleResultsFound
from sqlalchemy.orm import lazyload
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError
from bleach import clean

from app.main import db
from app.main.model.portfolio import Portfolio


def get_all_portfolios_for_user(user_id: int) -> List[Portfolio]:
    """Gets all Portfolios for the logged in user"""
    portfolios = (
        Portfolio.query.filter_by(owner_id=user_id)
        .options(
            lazyload(Portfolio.owner), lazyload(Portfolio.properties)  # type: ignore
        )
        .all()
    )  # type: ignore
    return portfolios


def get_portfolio_by_id(user_id: int, portfolio_id: int) -> Portfolio:
    try:
        current_app.logger.info(f"Getting portfolio by {portfolio_id}")
        return (
            Portfolio.query.filter_by(owner_id=user_id)
            .filter_by(id=portfolio_id)
            .options(
                lazyload(Portfolio.owner),  # type: ignore
                lazyload(Portfolio.properties),
            )
            .one()
        )  # type: ignore
    except NoResultFound as err:
        error_message = f"Portfolio not found for userid: {user_id} and portfolio_id {portfolio_id}. Error {err}"
        current_app.logger.error(error_message)
        raise NotFound(error_message)

    except MultipleResultsFound as err:
        error = f"Multiple portfolio's not found for userid {user_id} and portfolio_id {portfolio_id}"
        current_app.logger.error(error)
        raise BadRequest(error)


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


def delete_portfolio_by_id(user, portfolio_id):
    """Deletes the Portfolio and related data"""
    portfolio = (
        Portfolio.query.filter_by(id=portfolio_id)
        .filter_by(id=portfolio_id)
        .options(
            lazyload(Portfolio.owner),  # type: ignore
            lazyload(Portfolio.properties),  # type: ignore
            lazyload(Portfolio.properties.images),
            lazyload(Portfolio.properties),
        )
    )  # type: ignore
    if portfolio:
        if portfolio.owner_id == user.id:
            portfolio.delete()


def save_changes(data) -> None:
    db.session.add(data)
    db.session.commit()
