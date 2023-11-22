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
    # id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    # created_date: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow)
    # updated_date: Mapped[datetime] = mapped_column(
    #     db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    # )
    owner_id: Mapped[int] = mapped_column(
        Integer, db.ForeignKey(User.id, ondelete="CASCADE")
    )
    owner: Mapped["User"] = db.relationship("User")
    properties: Mapped[List["Property"]] = db.relationship(
        "Property", cascade="all, delete"
    )
