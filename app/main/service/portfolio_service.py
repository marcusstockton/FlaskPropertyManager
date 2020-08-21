from app.main import db
from app.main.model.portfolio import Portfolio
from typing import List, Dict
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import update
from sqlalchemy.orm import lazyload
import datetime


def get_all_portfolios_for_user(userId: int) -> List[Portfolio]:
	return Portfolio.query.filter_by(owner_id=userId).options(lazyload(Portfolio.owner), lazyload(Portfolio.properties)).all()


def get_portfolio_by_id(userId: int, portfolio_id: int) -> Portfolio:
	try:
		return Portfolio.query.filter_by(owner_id=userId).filter_by(id=portfolio_id).options(lazyload(Portfolio.owner), lazyload(Portfolio.properties)).one()
	except NoResultFound as e:
		response_object = {
			"status": "fail",
			"message": "Portfolio not found!"
		}
		return response_object, 404

def save_new_portfolio(data, user) -> Dict[str, str]:
	portfolio = Portfolio.query.filter_by(name=data['name']).first()
	if not portfolio:
		new_portfolio = Portfolio(
			name=data['name'],
			owner_id=user.id,
			created_on=datetime.datetime.utcnow()
		)
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


def update_portfolio(portfolio_id: int, data: dict):
	portfolio_query = db.session.query(Portfolio).filter(Portfolio.id == portfolio_id)
	if not portfolio_query:
		response_object = {
			'status': 'fail',
			'message': 'Portfolio not found.',
		}
		return response_object, 404
	created_on = data.get('created_on')
	data['created_on'] = datetime.datetime.strptime(created_on, '%Y-%m-%dT%H:%M:%S.%f')
	try:
		stmt = update(Portfolio).where(Portfolio.id==portfolio_id).values(data)
		db.session.execute(stmt)
		db.session.commit()
		response_object = {
			'status': 'success',
			'message': 'Portfolio updated.',
			'data': Portfolio(**data)
		}
		return response_object, 204
	except Exception as e:
		response_object = {
			'status': 'fail',
			'message': e
		}
		return response_object, 500



def save_changes(data) -> None:
	db.session.add(data)
	db.session.commit()
