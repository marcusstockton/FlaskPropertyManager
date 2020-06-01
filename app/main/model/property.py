from .. import db
from .portfolio import Portfolio


class Property(db.Model):
	""" Property Model for storing properties """
	__tablename__ = "property"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	portfolio_id = db.Column(db.Integer, db.ForeignKey(Portfolio.id))
	address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
	address = db.relationship("Address", foreign_keys=[address_id])
	purchase_price = db.Column(db.Float(precision='10, 2'), nullable=True)
	purchase_date = db.Column(db.DateTime, nullable=True)
	monthly_rental_price = db.Column(db.Float(precision='10, 2'), nullable=True)

