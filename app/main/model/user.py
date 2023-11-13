import re
from datetime import timedelta, datetime, timezone

import jwt

from app.main.model.blacklist import BlacklistToken
from .. import db, flask_bcrypt
from ..config import key


class User(db.Model):
    """User Model for storing user related details"""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    public_id = db.Column(db.String(100), unique=True, index=True)
    username = db.Column(db.String(50), unique=True, index=True)
    password_hash = db.Column(db.String(100))
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    date_of_birth = db.Column(db.DateTime, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    roles = db.relationship(
        "Role", secondary="user_roles", backref=db.backref("user", lazy="dynamic")
    )

    @property
    def password(self):
        """Handle write attempt to read-only field"""
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode(
            "utf-8"
        )

    def check_password(self, password):
        """Checks user password"""
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def validate_password(self, password):
        if len(password) < 8:
            print("Make sure your password is at lest 8 letters")
        elif re.search("[0-9]", password) is None:
            print("Make sure your password has a number in it")
        elif re.search("[A-Z]", password) is None:
            print("Make sure your password has a capital letter in it")
        else:
            print("Your password seems fine")

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                "exp": datetime.now(timezone.utc) + timedelta(days=1, seconds=5),
                "iat": datetime.now(timezone.utc),
                "sub": user_id,
                "username": User.query.filter_by(id=user_id).first().username,
            }
            return jwt.encode(payload, key, algorithm="HS256")
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            if auth_token.startswith("Bearer"):
                auth_token = auth_token.replace("Bearer ", "")

            payload = jwt.decode(auth_token, key, algorithms=["HS256"])
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return "Token blacklisted. Please log in again."
            else:
                return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."

    def __repr__(self):
        return "<User 'Id: {} {}'>".format(self.id, self.username)


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return f"<Role 'Id: {self.id} {self.name}'>"


# Define the UserRoles association tabletest_registered_user_login
class UserRoles(db.Model):
    __tablename__ = "user_roles"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id", ondelete="CASCADE"))
    role_id = db.Column(db.Integer(), db.ForeignKey("roles.id", ondelete="CASCADE"))

    def __repr__(self):
        return f"<UserRole 'Id: {self.id} user_id: {self.user_id}, role_id: {self.role_id}'>"
