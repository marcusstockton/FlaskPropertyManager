from app.main import db
from app.main.model.property import Property
from app.main.model.address import Address
from app.main.model.portfolio import Portfolio
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
import datetime


def get_all_properties_for_portfolio(portfolio_id):
    return Property.query.filter_by(portfolio_id=portfolio_id).all()


def save_new_property(portfolio_id, data):
    portfolio = Portfolio.query.filter_by(id=portfolio_id).first()

    if portfolio is None:
        response_object = {
            'status': 'fail',
            'message': 'No portfolio found',
        }
        return response_object, 409

    if data['address']:
        # create address
        new_address = Address(
            line_1=data['address']['line_1'],
            line_2=data['address'].get('line_2', None),
            line_3=data['address'].get('line_3', None),
            post_code=data['address']['post_code'],
            town=data['address'].get('town', None),
            city=data['address'].get('city', None)
        )
        new_property = Property(
            portfolio_id=portfolio_id,
            purchase_price=data['purchase_price'],
            purchase_date=datetime.datetime.strptime(data['purchase_date'], '%Y-%m-%d'),
            monthly_rental_price=data['monthly_rental_price'],
            created_on=datetime.datetime.utcnow()
        )

        new_property.address = new_address
        portfolio.properties.append(new_property)
        try:
            save_changes(portfolio)
            response_object = {
                'status': 'success',
                'message': 'Successfully created property.',
                'data': {
                    'id': new_property.id
                }
            }
            return response_object, 201
        except Exception as ex:
            response_object = {
                'status': 'failure',
                'message': 'Error saving property.',
                'data': {
                    f'Exception: {ex}',
                }
            }
            return response_object, 500


def get_property_by_id(portfolio_id, property_id):
    try:
        return Property.query.filter_by(portfolio_id=portfolio_id, id=property_id).one()
    except MultipleResultsFound as e:
        print(e)
    except NoResultFound as e:
        print(e)


def save_changes(data):
    db.session.add(data)
    db.session.commit()
