"""Address Entity"""

from dataclasses import dataclass
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship, mapped_column
from app.main.model.base import BaseClass


@dataclass
class Address(BaseClass):
    """Address Model for storing addresses"""

    __tablename__ = "address"
    line_1: Mapped[str] = mapped_column(String(100))
    line_2: Mapped[str] = mapped_column(String(100), nullable=True)
    line_3: Mapped[str] = mapped_column(String(100), nullable=True)
    post_code: Mapped[str] = mapped_column(String(100))
    town: Mapped[str] = mapped_column(String(100), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=True)
    property_id: Mapped[int] = mapped_column(Integer, ForeignKey("property.id"))
    property: Mapped["Property"] = relationship(back_populates="address")
