"""Blacklist Entity"""

from dataclasses import dataclass
from datetime import datetime
from .. import db
from sqlalchemy.orm import Mapped


@dataclass
class BlacklistToken(db.Model):
    """Token Model for storing JWT tokens"""

    __tablename__ = "blacklist_tokens"

    id: Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on: Mapped[datetime] = db.Column(db.DateTime, nullable=False)

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
