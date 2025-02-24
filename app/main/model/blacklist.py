"""Blacklist Entity"""

from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from .. import db
from sqlalchemy.orm import Mapped, mapped_column


@dataclass
class BlacklistToken(db.Model):
    """Token Model for storing JWT tokens"""

    __tablename__ = "blacklist_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    blacklisted_on: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.now()

    def __repr__(self):
        return "<id: token: {}".format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        """check whether auth token has been blacklisted"""
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
