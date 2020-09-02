from app.main import db
from flask import current_app
from app.main.model.portfolio import Portfolio
from typing import List, Dict
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update
from sqlalchemy.orm import lazyload
import datetime
from flask_restx import abort


def get_all_portfolios_for_user(user_id: int) -> List[Portfolio]:
    return Portfolio.query.filter_by(owner_id=user_id).options(lazyload(Portfolio.owner),
                                                               lazyload(Portfolio.properties)).all()


def get_portfolio_by_id(user_id: int, portfolio_id: int) -> Portfolio:
    try:
        return Portfolio.query.filter_by(owner_id=user_id).filter_by(id=portfolio_id) \
            .options(lazyload(Portfolio.owner),
                     lazyload(Portfolio.properties)).one()
    except NoResultFound as e:
        current_app.logger.error("Portfolio not found for userid %s and portfolio_id %s", user_id, portfolio_id)
        abort(404, "Portfolio not found")
    except MultipleResultsFound as e:
        current_app.logger.error("Multiple portfolio's not found for userid %s and portfolio_id %s", user_id, portfolio_id)
        abort(500, "Multiple Portfolio's found")


def save_new_portfolio(data, user) -> Dict[str, str]:
    portfolio = Portfolio.query.filter_by(name=data['name']).first()
    if not portfolio:
        new_portfolio = Portfolio(
            name=data['name'],
            owner_id=user.id,
            created_on=datetime.datetime.utcnow()
        )
        save_changes(new_portfolio)
        return new_portfolio
    else:
        abort(409, "Portfolio already exists.")


def update_portfolio(portfolio_id: int, data: dict):
    portfolio_query = db.session.query(Portfolio).filter(Portfolio.id == portfolio_id)
    if not portfolio_query:
        abort(404, "Portfolio not found.")

    try:
        stmt = update(Portfolio).where(Portfolio.id == portfolio_id).values(data)
        db.session.execute(stmt)
        db.session.commit()
        return Portfolio(**data)

    except IntegrityError as e:
        abort(500, e.args)

    except Exception as e:
        abort(500, e)


def save_changes(data) -> None:
    db.session.add(data)
    db.session.commit()
