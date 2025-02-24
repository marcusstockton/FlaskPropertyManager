"""Property Entity"""

from dataclasses import dataclass
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey, Integer, LargeBinary, String

from app.main.model.base import BaseClass
from .property import Property


@dataclass
class PropertyImages(BaseClass):
    """Property Images model for storing property images"""

    __tablename__ = "propertyImages"
    image: Mapped[LargeBinary] = mapped_column(LargeBinary)
    file_name: Mapped[str] = mapped_column(String(200))
    property_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("property.id"), nullable=False
    )
    property: Mapped["Property"] = relationship(
        "Property", back_populates="property_pics"
    )
