from dataclasses import dataclass
from datetime import datetime
from typing import List
from app.main.model.base import BaseClass

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .. import db


@dataclass
class Property(BaseClass):

    """Property Model for storing properties"""

    __tablename__ = "property"
    portfolio_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("portfolio.id", ondelete="cascade")
    )
    owner_id: Mapped[int] = mapped_column(
        Integer, db.ForeignKey("user.id", ondelete="cascade")
    )
    purchase_price: Mapped[float] = mapped_column(
        db.Float(precision="10, 2"), nullable=True
    )
    purchase_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    sold_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    monthly_rental_price: Mapped[float] = mapped_column(
        db.Float(precision="10, 2"), nullable=True
    )
    address: Mapped[List["Address"]] = db.relationship(
        "Address", back_populates="property", uselist=False, cascade="all, delete"
    )
    tenants: Mapped[List["Tenant"]] = db.relationship(
        "Tenant", back_populates="property", cascade="all, delete"
    )
    owner = db.relationship("User")
    property_pics: Mapped[List["PropertyImages"]] = db.relationship(
        "PropertyImages", back_populates="property", lazy=True
    )
