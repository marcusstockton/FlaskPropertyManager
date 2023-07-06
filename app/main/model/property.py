from datetime import datetime

from sqlalchemy import LargeBinary

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
    purchase_date = db.Column(db.Date, nullable=True)
    sold_date = db.Column(db.Date, nullable=True)
    monthly_rental_price = db.Column(db.Float(precision='10, 2'), nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    address = db.relationship("Address", back_populates="property", uselist=False, cascade="all, delete")
    tenants = db.relationship("Tenant", back_populates="property", cascade="all, delete")
    owner = db.relationship("User")
    property_pics = db.relationship("PropertyImages", back_populates="property", lazy=True)

    def __repr__(self):
        return f"<Property 'Id:{self.id} PortfolioId:{self.portfolio_id} Owner:{self.owner} Address: {self.address}'>"


class PropertyImages(db.Model):
    """Property Images model for storing property images"""
    __tablename__ = "propertyImages"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    image = db.Column(LargeBinary)
    file_name = db.Column(db.String(200))
    property_id = db.Column(db.Integer, db.ForeignKey(Property.id), nullable=False)
    property = db.relationship("Property", back_populates="property_pics")

    def __repr__(self):
        return f"<Property Image 'Id:{self.id} Property_Id:{self.property_id} Filename:{self.file_name}'>"
