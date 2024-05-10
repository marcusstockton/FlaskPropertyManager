"""Portfolio Entity"""

from dataclasses import dataclass
from datetime import datetime
from typing import List
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.main.model.base import BaseClass

from .user import User
from .. import db


@dataclass
class Portfolio(BaseClass):  # Revert this to db.Model
    """Portfolio Model for storing portfolio's"""

    __tablename__ = "portfolio"
    name: Mapped[str] = mapped_column(String, nullable=False)
    owner_id: Mapped[int] = mapped_column(
        Integer, db.ForeignKey(User.id, ondelete="CASCADE")
    )
    owner: Mapped["User"] = db.relationship("User")
    properties: Mapped[List["Property"]] = db.relationship(
        "Property", cascade="all, delete"
    )
