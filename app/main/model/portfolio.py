"""Portfolio Entity"""

from dataclasses import dataclass
from typing import List
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.main.model.base import BaseClass

from .user import User
from .property import Property


@dataclass
class Portfolio(BaseClass):  # Revert this to db.Model
    """Portfolio Model for storing portfolio's"""

    __tablename__ = "portfolio"
    name: Mapped[str] = mapped_column(String, nullable=False)
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(User.id, ondelete="CASCADE")
    )
    owner: Mapped["User"] = relationship("User")
    properties: Mapped[List["Property"]] = relationship(
        "Property", cascade="all, delete, delete-orphan"
    )
