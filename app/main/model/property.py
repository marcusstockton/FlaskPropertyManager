from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar, List

from sqlalchemy import LargeBinary

from app.main.model.address import Address

from .portfolio import Portfolio
from .user import User
from .. import db


@dataclass
class Property(db.Model):
    """Property Model for storing properties"""

    __tablename__ = "property"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    portfolio_id: int = db.Column(
        db.Integer, db.ForeignKey(Portfolio.id, ondelete="cascade")
    )
    owner_id: int = db.Column(db.Integer, db.ForeignKey(User.id, ondelete="cascade"))
    purchase_price: float = db.Column(db.Float(precision="10, 2"), nullable=True)
    purchase_date: datetime = db.Column(db.Date, nullable=True)
    sold_date: datetime | None = db.Column(db.Date, nullable=True)
    monthly_rental_price: float = db.Column(db.Float(precision="10, 2"), nullable=True)
    created_date: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date: datetime = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    address = db.relationship(
        "Address", back_populates="property", uselist=False, cascade="all, delete"
    )
    tenants = db.relationship(
        "Tenant", back_populates="property", cascade="all, delete"
    )
    owner = db.relationship("User")
    property_pics = db.relationship(
        "PropertyImages", back_populates="property", lazy=True
    )


@dataclass
class PropertyImages(db.Model):
    """Property Images model for storing property images"""

    __tablename__ = "propertyImages"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_date: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date: datetime = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    image: LargeBinary = db.Column(LargeBinary)
    file_name: str = db.Column(db.String(200))
    property_id: int = db.Column(db.Integer, db.ForeignKey(Property.id), nullable=False)
    property = db.relationship("Property", back_populates="property_pics")
