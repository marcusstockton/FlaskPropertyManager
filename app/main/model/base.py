"""Abstract Base Class (to be inherited only)"""

from datetime import datetime
from datetime import timezone
from sqlalchemy.orm import Mapped
from .. import db


# @dataclass(kw_only=True)
class BaseClass(db.Model):
    """Base class"""

    __abstract__ = True
    id: Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_date: Mapped[datetime] = db.Column(
        db.DateTime, default=datetime.now(timezone.utc)
    )
    updated_date: Mapped[datetime] = db.Column(
        db.DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
