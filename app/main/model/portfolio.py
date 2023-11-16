from dataclasses import dataclass
from datetime import datetime

from .user import User
from .. import db


@dataclass
class Portfolio(db.Model):
    """Portfolio Model for storing portfolio's"""

    __tablename__ = "portfolio"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(100), nullable=False)
    created_date: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date: datetime = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    owner_id: int = db.Column(db.Integer, db.ForeignKey(User.id, ondelete="CASCADE"))
    owner = db.relationship("User")
    properties = db.relationship("Property", cascade="all, delete")
