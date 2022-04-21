from .. import db
from datetime import datetime


class Address(db.Model):
	""" Address Model for storing addresses """
	__tablename__ = "address"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	line_1 = db.Column(db.String(100))
	line_2 = db.Column(db.String(100), nullable=True)
	line_3 = db.Column(db.String(100), nullable=True)
	post_code = db.Column(db.String(100))
	town = db.Column(db.String(100), nullable=True)
	city = db.Column(db.String(100), nullable=True)
	created_date = db.Column(db.DateTime, default=datetime.utcnow)
	updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  
	property_id = db.Column(db.Integer, db.ForeignKey("property.id"))
	property = db.relationship("Property", back_populates="address", foreign_keys=[property_id])

	def __repr__(self):
		return "<Address 'Id:{} Address:{} {} {} {} {} {} PropertyId:{}'>"\
			.format(self.id, self.line_1, self.line_2, self.line_3, self.post_code, self.town, self.city, self.property_id)
