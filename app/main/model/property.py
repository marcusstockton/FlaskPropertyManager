from datetime import datetime

from .portfolio import Portfolio
from .user import User
from .. import db


class Property(db.Model):
    """ Property Model for storing properties """
    __tablename__ = "property"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey(Portfolio.id, ondelete="cascade"))
    owner_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete="cascade"))
    purchase_price = db.Column(db.Float(precision='10, 2'), nullable=True)
    purchase_date = db.Column(db.DateTime, nullable=True)
    monthly_rental_price = db.Column(db.Float(precision='10, 2'), nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    address = db.relationship("Address",  back_populates="property",uselist=False, cascade="all, delete")
    tenants = db.relationship("Tenant", cascade="all, delete")
    owner = db.relationship("User")

    def __repr__(self):
        return "<Property 'Id:{} PortfolioId:{} Owner:{} Address: {}'>".format(self.id, self.portfolio_id, self.owner, self.address)
