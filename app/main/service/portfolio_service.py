import datetime
from typing import List, Dict

import flask
from flask import current_app
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import lazyload
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError

from app.main import db
from app.main.model.portfolio import Portfolio


def get_all_portfolios_for_user(user_id: int) -> List[Portfolio]:
    return Portfolio.query.filter_by(owner_id=user_id).options(lazyload(Portfolio.owner),
                                                               lazyload(Portfolio.properties)).all()


def get_portfolio_by_id(user_id: int, portfolio_id: int) -> Portfolio:
    try:
        return Portfolio.query.filter_by(owner_id=user_id).filter_by(id=portfolio_id) \
            .options(lazyload(Portfolio.owner),
                     lazyload(Portfolio.properties)).one()
    except NoResultFound as e:
        current_app.logger.error(f"Portfolio not found for userid: {user_id} and portfolio_id {portfolio_id}. Error {e}")
        raise NotFound("Portfolio not found for userid %s and portfolio_id %s", user_id, portfolio_id)
    except MultipleResultsFound as e:
        current_app.logger.error("Multiple portfolio's not found for userid %s and portfolio_id %s", user_id, portfolio_id)
        raise BadRequest("Multiple portfolio's found for userid %s and portfolio_id %s. Error %s", user_id, portfolio_id, e)


def save_new_portfolio(data, user_id) -> Dict[str, str]:
    sanitised_name = flask.escape(data["name"])
    portfolio = Portfolio.query.filter_by(name=sanitised_name).filter_by(owner_id=user_id).first()
    if not portfolio:
        new_portfolio = Portfolio(
            name=sanitised_name,
            owner_id=user_id,
            created_date=datetime.datetime.utcnow()
        )
        save_changes(new_portfolio)
        return new_portfolio
    else:
        raise BadRequest("Portfolio already exists.")


def update_portfolio(portfolio_id: int, data: dict):
    portfolio_query = Portfolio.query.filter_by(id=portfolio_id).one()
    if not portfolio_query:
        raise NotFound("Portfolio not found.")
    try:
        stmt = update(Portfolio).where(Portfolio.id == portfolio_id).values(flask.escape(data))
        db.session.execute(stmt)
        db.session.commit()
        return Portfolio(**data)
    except IntegrityError as e:
        raise InternalServerError(e.orig)


def save_changes(data) -> None:
    db.session.add(data)
    db.session.commit()
