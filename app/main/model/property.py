from dataclasses import dataclass
from datetime import datetime
from sqlalchemy.orm import Mapped

# from app.main.model.address import Address

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
    address: Mapped["Address"] = db.relationship(
        "Address", back_populates="property", uselist=False, cascade="all, delete"
    )
    tenants: Mapped[list["Tenant"]] = db.relationship(
        "Tenant", back_populates="property", cascade="all, delete"
    )
    owner = db.relationship("User")
    property_pics: Mapped[list["PropertyImages"]] = db.relationship(
        "PropertyImages", back_populates="property", lazy=True
    )
