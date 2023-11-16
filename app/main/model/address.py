from dataclasses import dataclass
from .. import db
from datetime import datetime


@dataclass
class Address(db.Model):
    """Address Model for storing addresses"""

    __tablename__ = "address"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    line_1: str = db.Column(db.String(100))
    line_2: str = db.Column(db.String(100), nullable=True)
    line_3: str = db.Column(db.String(100), nullable=True)
    post_code: str = db.Column(db.String(100))
    town: str = db.Column(db.String(100), nullable=True)
    city: str = db.Column(db.String(100), nullable=True)
    created_date: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date: datetime = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    property_id: int = db.Column(db.Integer, db.ForeignKey("property.id"))
    property = db.relationship(
        "Property", back_populates="address", foreign_keys=[property_id]
    )
