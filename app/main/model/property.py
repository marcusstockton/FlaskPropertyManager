from .. import db
from .portfolio import Portfolio
import datetime
from .user import User


class Property(db.Model):
	""" Property Model for storing properties """
	__tablename__ = "property"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	portfolio_id = db.Column(db.Integer, db.ForeignKey(Portfolio.id))
	address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
	owner_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'))
	purchase_price = db.Column(db.Float(precision='10, 2'), nullable=True)
	purchase_date = db.Column(db.DateTime, nullable=True)
	monthly_rental_price = db.Column(db.Float(precision='10, 2'), nullable=True)
	created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	address = db.relationship("Address", foreign_keys=[address_id])
	tenants = db.relationship("Tenant")
	owner = db.relationship("User")