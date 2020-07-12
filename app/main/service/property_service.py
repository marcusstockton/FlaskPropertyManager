from app.main import db
from app.main.model.property import Property
from app.main.model.address import Address
from app.main.model.portfolio import Portfolio
import uuid
import json
from collections import namedtuple


def get_all_properties_for_portfolio(portfolioId):
    return Property.query.filter_by(portfolio_id=portfolioId).all()


def save_new_property(portfolio_id, data):
    property = Property.query.filter_by(id=data['id']).first()
    if property is None:
        response_object = {
            'status': 'fail',
            'message': 'No portfolio found',
        }
        return response_object, 409

    test_parse = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

    if data['address']:
        # create address
        new_address = Address(
            id=str(uuid.uuid4()),
            line_1 = data['address']['line_1'],
            line_2 = data['address']['line_2'],
            line_3 = data['address']['line_3'],
            post_code = data['address']['post_code'],
            town = data['address']['town'],
            city = data['address']['city']
        )
    if not portfolio:
        new_property = Property(
            id=str(uuid.uuid4()),
            portfolio_id=portfolio_id,
            purchase_price=data['purchase_price'],
            purchase_date=data['purchase_date'],
            monthly_rental_price=data['monthly_rental_price'],
            created_on=datetime.datetime.utcnow()
        )
        new_property.append(new_address)
        Portfolio.properties.append(new_property)
        save_changes()
        return new_property
    else:
        response_object = {
            'status': 'fail',
            'message': 'Portfolio already exists.',
        }
        return response_object, 409


def save_changes(data):
    db.session.add(data)
    db.session.commit()
