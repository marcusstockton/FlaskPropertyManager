from .. import db
import datetime
from .user import User


class Portfolio(db.Model):
	""" Portfolio Model for storing portfolio's """
	__tablename__ = "portfolio"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(100))
	created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	owner_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'))
	owner = db.relationship("User")
	properties = db.relationship("Property")

	def __repr__(self):
		return "<Portfolio '{}'>".format(self.name)