"""Property Entity"""

from dataclasses import dataclass
from datetime import datetime
from typing import List
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.main.model.base import BaseClass


from .. import db


@dataclass
class Property(BaseClass):
    """Property Model for storing properties"""

    __tablename__ = "property"
    portfolio_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("portfolio.id", ondelete="cascade")
    )
    purchase_price: Mapped[float] = mapped_column(
        db.Float(precision="10, 2"), nullable=True
    )
    purchase_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    sold_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    monthly_rental_price: Mapped[float] = mapped_column(
        db.Float(precision="10, 2"), nullable=True
    )
    address: Mapped["Address"] = relationship(
        back_populates="property", uselist=False, cascade="all, delete, delete-orphan"
    )
    tenants: Mapped[List["Tenant"]] = relationship(
        "Tenant", back_populates="property", cascade="all, delete, delete-orphan"
    )
    property_pics: Mapped[List["PropertyImages"]] = relationship(
        "PropertyImages",
        back_populates="property",
        lazy=True,
        cascade="all, delete, delete-orphan",
    )
