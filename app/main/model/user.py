"""User Entity"""

from dataclasses import dataclass
from datetime import date, timedelta, datetime, timezone
from typing import Optional
from flask import current_app
from sqlalchemy_utils import EmailType
import jwt
from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.main.model.base import BaseClass
from app.main.model.blacklist import BlacklistToken
from .. import db, flask_bcrypt
from ..config import key


@dataclass
class User(BaseClass):
    """User Model for storing user related details"""

    __tablename__ = "user"

    email: Mapped[str] = mapped_column(
        EmailType, unique=True, nullable=False, index=True
    )
    registered_on: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    public_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(100))
    first_name: Mapped[str] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)
    date_of_birth: Mapped[Optional[date]] = mapped_column(DateTime, nullable=True)
    roles = relationship(
        "Role", secondary="user_roles", backref=db.backref("user", lazy="dynamic")
    )

    @property
    def password(self):
        """Handle write attempt to read-only field"""
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password) -> None:
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode(
            "utf-8"
        )

    def check_password(self, password) -> bool:
        """Checks user password"""
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def encode_auth_token(self, user_id, expires_mins=1440) -> str:
        """
        Generates the Auth Token
        :return: string
        """
        try:
            roles = [role.name for role in self.roles]
            payload = {
                "exp": datetime.now(timezone.utc) + timedelta(minutes=expires_mins),
                "iat": datetime.now(timezone.utc),
                "sub": str(user_id),
                "username": self.username,
                "roles": roles,
            }
            token = jwt.encode(payload, key, algorithm="HS256")
            # PyJWT >= 2.0 returns a string, <2.0 returns bytes
            if isinstance(token, bytes):
                token = token.decode("utf-8")
            return token
        except Exception as e:
            current_app.logger.error(f"Token generation failed: {e}")
            raise RuntimeError(f"Token generation failed: {e}") from e

    @staticmethod
    def decode_auth_token(auth_token) -> dict | str:
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            if auth_token.startswith("Bearer"):
                auth_token = auth_token.replace("Bearer ", "")

            payload = jwt.decode(auth_token, key, algorithms=["HS256"])
            if BlacklistToken.check_blacklist(auth_token):
                return "Token blacklisted. Please log in again."
            return payload
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."
        except Exception as e:
            return f"Token decode error: {e}"


@dataclass
class Role(db.Model):
    """Roles"""

    __tablename__ = "roles"
    id: int = db.Column(db.Integer(), primary_key=True)
    name: str = db.Column(db.String(50), unique=True)


@dataclass
class UserRoles(db.Model):
    """Join table for users and roles"""

    __tablename__ = "user_roles"
    id: int = db.Column(db.Integer(), primary_key=True)
    user_id: int = db.Column(db.Integer(), db.ForeignKey("user.id", ondelete="CASCADE"))
    role_id: int = db.Column(
        db.Integer(), db.ForeignKey("roles.id", ondelete="CASCADE")
    )
