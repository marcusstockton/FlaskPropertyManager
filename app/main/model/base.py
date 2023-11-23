from datetime import datetime
from sqlalchemy.orm import Mapped
from .. import db


# @dataclass(kw_only=True)
class BaseClass(db.Model):
    __abstract__ = True

    # id: int = field(init=False)
    # created_date: datetime = field(init=False)
    # updated_date: datetime = field(init=False)

    id: Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_date: Mapped[datetime] = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date: Mapped[datetime] = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
