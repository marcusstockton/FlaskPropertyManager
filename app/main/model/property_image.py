from dataclasses import dataclass
from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy import LargeBinary
from .. import db


@dataclass
class PropertyImages(db.Model):
    """Property Images model for storing property images"""

    __tablename__ = "propertyImages"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_date: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date: datetime = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    image: LargeBinary = db.Column(LargeBinary)
    file_name: str = db.Column(db.String(200))
    property_id: int = db.Column(
        db.Integer, db.ForeignKey("property.id"), nullable=False
    )
    property: Mapped["Property"] = db.relationship(
        "Property", back_populates="property_pics"
    )
