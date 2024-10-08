"""Address Entity"""

from dataclasses import dataclass
from sqlalchemy.orm import Mapped, relationship
from app.main.model.base import BaseClass
from .. import db


@dataclass
class Address(BaseClass):
    """Address Model for storing addresses"""

    __tablename__ = "address"
    line_1: Mapped[str] = db.Column(db.String(100))
    line_2: Mapped[str] = db.Column(db.String(100), nullable=True)
    line_3: Mapped[str] = db.Column(db.String(100), nullable=True)
    post_code: Mapped[str] = db.Column(db.String(100))
    town: Mapped[str] = db.Column(db.String(100), nullable=True)
    city: Mapped[str] = db.Column(db.String(100), nullable=True)
    property_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey("property.id"))
    property: Mapped["Property"] = relationship(back_populates="address")
