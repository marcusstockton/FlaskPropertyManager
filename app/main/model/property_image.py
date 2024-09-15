"""Property Entity"""

from dataclasses import dataclass
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import LargeBinary

from app.main.model.base import BaseClass
from .property import Property
from .. import db


@dataclass
class PropertyImages(BaseClass):
    """Property Images model for storing property images"""

    __tablename__ = "propertyImages"
    image: Mapped[LargeBinary] = db.Column(LargeBinary)
    file_name: Mapped[str] = db.Column(db.String(200))
    property_id: Mapped[int] = db.Column(
        db.Integer, db.ForeignKey("property.id"), nullable=False
    )
    property: Mapped["Property"] = relationship(
        "Property", back_populates="property_pics"
    )
