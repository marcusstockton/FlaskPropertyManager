from app.main import db
from app.main.model.portfolio import Portfolio
import uuid

def get_all_portfolios_for_user(userId):
    return Portfolio.query.filter_by(owner=userId).all()


def save_new_portfolio(data):
    portfolio = Portfolio.query.filter_by(id=data['id']).first()
    if not portfolio:
        new_portfolio = Portfolio(
            id=str(uuid.uuid4()),
            name=data['name'],
            owner=data['owner'],
            properties=data['properties'],
            created_on=datetime.datetime.utcnow()
        )
        save_changes(new_portfolio)
        return new_portfolio
    else:
        response_object = {
            'status': 'fail',
            'message': 'Portfolio already exists.',
        }
        return response_object, 409


def save_changes(data):
    db.session.add(data)
    db.session.commit()
