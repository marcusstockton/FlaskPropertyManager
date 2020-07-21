from app.main import db
from app.main.model.portfolio import Portfolio
from app.main.model.user import User
import uuid
import datetime
from sqlalchemy.orm import subqueryload
import pdb

def get_all_portfolios_for_user(userId):
    return Portfolio.query.filter_by(owner_id=userId).all()

def get_portfolio_by_id(portfolio_id):
    return db.session.query(Portfolio).get(portfolio_id)

def save_new_portfolio(data, user):
    portfolio = Portfolio.query.filter_by(name=data['name']).first()
    if not portfolio:
        new_portfolio = Portfolio(
            name=data['name'],
            owner_id=user.id,
            created_on=datetime.datetime.utcnow()
        )
        pdb.set_trace()
        save_changes(new_portfolio)
        response_object = {
            "status": "success",
            "message": "Portfolio created successfully!"
        }
        return response_object
    else:
        response_object = {
            'status': 'fail',
            'message': 'Portfolio already exists.',
        }
        return response_object, 409


def update_portfolio(portfolio_id, data):
    portfolio = db.session.query(Portfolio).get(portfolio_id)
    if not portfolio:
        response_object = {
            'status': 'fail',
            'message': 'Portfolio not found.',
        }
        return response_object, 404

    pdb.set_trace()
    db.session.query(Portfolio)\
       .filter(id==portfolio_id)\
       .update({BankAccount.money: BankAccount.money + 50})


def save_changes(data):
    db.session.add(data)
    db.session.commit()
