"""Portfolio Service for interacting with portfolios"""

from http import HTTPStatus
from typing import List, Dict, Tuple, Union

from flask import current_app
from sqlalchemy import Update, update, exists
from sqlalchemy.exc import (
    IntegrityError,
    NoResultFound,
    MultipleResultsFound,
    SQLAlchemyError,
)
from sqlalchemy.orm import lazyload
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError
import json
from app.main import db, redis_client
from app.main.model.portfolio import Portfolio
from app.main.model.user import User
from app.main.schemas.portfolio import PortfolioSchema


def get_all_portfolios_for_user(user: User) -> List[Portfolio]:
    """Gets all Portfolios for the logged in user"""

    cache_key = f"portfolios_user_{'admin' if user.admin else user.id}"
    cached = redis_client.get(cache_key)

    if cached:
        current_app.logger.info("Portfolio found in cache with key: %s", cache_key)
        # Deserialize JSON string to Python objects
        portfolio_dicts = json.loads(cached)
        # Convert dicts back to Portfolio objects if needed
        # If you have a Portfolio schema, use it here
        # Otherwise, return the dicts
        return portfolio_dicts

    current_app.logger.info("Portfolio not found in cache. Calling database.")
    if user.admin:
        portfolios = Portfolio.query.all()
    else:
        portfolios = (Portfolio.query.filter_by(owner_id=user.id)
        .options(lazyload(Portfolio.owner), lazyload(Portfolio.properties))
        .all())
    # Serialize portfolios to JSON (use a schema if available)
    schema = PortfolioSchema(many=True)
    portfolios_json = schema.dumps(portfolios)

    # Store in Redis (set an expiry if desired, e.g., 300 seconds)
    redis_client.setex(cache_key, 300, portfolios_json)

    return portfolios



def get_portfolio_by_id(user: User, portfolio_id: int) -> Portfolio:
    """Returns the portfolio from the given portfolio Id"""
    try:
        current_app.logger.info(f"Getting portfolio by {portfolio_id}")
        if user.admin:
            return (
                Portfolio.query.filter_by(id=portfolio_id)
                .options(lazyload(Portfolio.owner), lazyload(Portfolio.properties))
                .one()
            )
        else:
            return (
                Portfolio.query.filter_by(owner_id=user.id, id=portfolio_id)
                .options(lazyload(Portfolio.owner), lazyload(Portfolio.properties))
                .one()
            )
    except NoResultFound as err:
        error_message = (
            f"Portfolio not found for userid: {user.id} and portfolio_id {portfolio_id}. Error {err}"
        )
        current_app.logger.error(error_message)
        raise NotFound(error_message) from err
    except MultipleResultsFound as err:
        error_message = (
            f"Multiple portfolios found for userid {user.id} and portfolio_id {portfolio_id}. Error: {err}"
        )
        current_app.logger.error(error_message)
        raise BadRequest(error_message) from err


def save_new_portfolio(data: Dict[str, str], user_id: int) -> Portfolio:
    """Creates a new Portfolio"""
    sanitised_name = data["name"]
    current_app.logger.info(f"Adding portfolio {sanitised_name}")
    portfolio_exists = db.session.query(exists().where(Portfolio.name == sanitised_name).where(Portfolio.owner_id == user_id)).scalar()
    if not portfolio_exists:
        current_app.logger.info(f"Portfolio {sanitised_name} does not exist so adding.")
        new_portfolio = Portfolio(name=sanitised_name, owner_id=user_id)
        save_changes(new_portfolio)
        current_app.logger.info(f"Portfolio {sanitised_name} successfully added.")
        return new_portfolio
    raise BadRequest("Portfolio already exists.")


def update_portfolio(portfolio_id: int, data: Dict[str, Union[str, int]]) -> Portfolio:
    """Update a portfolio"""
    if portfolio_id != data["id"]:
        raise BadRequest("Invalid Request. Please check your data")
    portfolio_query = Portfolio.query.filter_by(id=portfolio_id).one_or_none()
    if not portfolio_query:
        raise NotFound("Portfolio not found.")
    try:
        sanitised_name = str(data.get("name", ""))
        data["name"] = sanitised_name
        stmt = update(Portfolio).where(Portfolio.id == portfolio_id).values(data)
        db.session.execute(stmt)
        db.session.commit()
        return portfolio_query
    except IntegrityError as err:
        raise InternalServerError(err.statement) from err
    except SQLAlchemyError as ex:
        current_app.logger.exception(ex)
        raise InternalServerError(repr(ex)) from ex


def delete_portfolio_by_id(user: User, portfolio_id: int) -> Tuple[Dict[str, Union[str, Dict[str, int]]], HTTPStatus]:
    """Deletes the Portfolio and related data"""
    portfolio = Portfolio.query.filter_by(id=portfolio_id).one_or_none()
    if not portfolio:
        raise NotFound("Portfolio not found")
    if portfolio.owner_id != user.id:
        current_app.logger.error(
            f"{user.id} tried to delete portfolio {portfolio_id} which they are not the owner of"
        )
        raise BadRequest("You cannot delete this portfolio")
    db.session.delete(portfolio)
    db.session.commit()
    response_object = {
        "status": "success",
        "message": "Successfully deleted the portfolio.",
        "data": {"id": portfolio_id},
    }
    return response_object, HTTPStatus.NO_CONTENT


def save_changes(data: Union[Portfolio, User]) -> None:
    """Saves changes"""
    try:
        db.session.add(data)
        db.session.commit()
    except SQLAlchemyError as ex:
        current_app.logger.exception(ex)
        raise InternalServerError(repr(ex)) from ex