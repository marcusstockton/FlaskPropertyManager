"""User Service for interacting with users"""

import uuid
from datetime import datetime, timezone
from http import HTTPStatus

from flask import current_app
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound

from app.main import db
from app.main.model.user import User, Role


def save_new_user(data):
    """Creates a new user"""
    user = User.query.filter_by(email=data["email"]).first()
    if user:
        raise BadRequest("User already exists. Please Log in.")

    owner_role = Role.query.filter_by(
        name="Owner"
    ).first()  # All users created are owners...for now
    new_user = User(
        public_id=str(uuid.uuid4()),
        email=data["email"],
        username=data["username"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        date_of_birth=(
            datetime.strptime(data["date_of_birth"], "%Y-%m-%d")
            if "date_of_birth" in data
            else None
        ),
        registered_on=datetime.now(timezone.utc),
    )
    new_user.password = data["password"]
    new_user.roles = [
        owner_role,
    ]
    save_changes(new_user)
    return generate_token(new_user)


def update_user(user_id, data):
    """Updates a user"""
    user_query = User.query.filter_by(public_id=user_id).one()
    if not user_query:
        raise NotFound("User not found.")
    try:
        data["date_of_birth"] = datetime.strptime(
            data["date_of_birth"], "%Y-%m-%d"
        ).date()
        data["updated_date"] = datetime.now()
        stmt = update(User).where(User.id == user_query.id).values(data)
        db.session.execute(stmt)
        db.session.commit()

        response_object = {
            "status": "success",
            "message": "Successfully updated user.",
            "data": {"id": user_id},
        }
        return response_object, HTTPStatus.NO_CONTENT
    except IntegrityError as e:
        raise InternalServerError(e) from e


def delete_user(user_id):
    """Deletes a user"""
    obj = User.query.filter_by(public_id=user_id).one()
    try:
        db.session.delete(obj)
        db.session.commit()
        response_object = {
            "status": "success",
            "message": f"Successfully deleted user {user_id}",
        }
        return response_object, HTTPStatus.NO_CONTENT
    except IntegrityError as e:
        raise InternalServerError(e) from e


def get_all_users():
    """Returns all users"""
    current_app.logger.info("Calling get all users")
    return User.query.all()


def get_a_user(public_id):
    """Retrieves a user via its public id"""
    current_app.logger.info(f"Calling get a user with public_id {public_id}")
    user = User.query.filter_by(public_id=public_id).first()
    return user


def get_a_user_by_username(username):
    """Retrieves a user via its username"""
    current_app.logger.info(f"Calling get a user with username {username}")
    return User.query.filter_by(username=username).first()


def generate_token(user):
    """Generates a JWT Token"""
    try:
        # generate the auth token
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            "status": "success",
            "message": "Successfully registered.",
            "user_id": user.public_id,
            "user_name": user.username,
            "Authorization": auth_token,
        }
        current_app.logger.info("auth_token created successfully")
        return response_object, HTTPStatus.CREATED
    except Exception as e:
        raise InternalServerError(e) from e


def save_changes(data):
    """Saves changes"""
    db.session.add(data)
    db.session.commit()
