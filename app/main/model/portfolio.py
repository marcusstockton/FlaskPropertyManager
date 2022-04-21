from datetime import datetime

from .user import User
from .. import db


class Portfolio(db.Model):
	""" Portfolio Model for storing portfolio's """
	__tablename__ = "portfolio"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(100))
	created_date = db.Column(db.DateTime, default=datetime.utcnow)
	updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  
	owner_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'))
	owner = db.relationship("User")
	properties = db.relationship("Property", cascade="all, delete")

	def __repr__(self):
		return "<Portfolio 'Id:{}, Name:{}'>".format(self.id, self.name)