from app.main import db
from app.main.model.portfolio import Portfolio
import uuid

def get_all_portfolios():
    return Portfolio.query.all()


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
        save_changes(portfolio)
        return new_user
    else:
        response_object = {
            'status': 'fail',
            'message': 'Portfolio already exists.',
        }
        return response_object, 409


# id = db.Column(db.Integer, primary_key=True, autoincrement=True)
# 	name = db.Column(db.String(100))
# 	created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
# 	owner = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'))
# 	properties = db.relationship("Property")