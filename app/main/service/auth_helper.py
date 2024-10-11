"""Auth Helper Service for managing users"""

from http import HTTPStatus
from flask import current_app as app
from werkzeug.exceptions import NotFound, Unauthorized
from app.main.model.user import User
from ..service.blacklist_service import save_token


class Auth:
    """Contains Authentication functions"""

    @staticmethod
    def login_user(data):
        """User Auth"""
        user: User | None = User.query.filter_by(email=data.get("email")).first()
        if user is None:
            raise NotFound("Username or password invalid.")
        if user and user.check_password(data.get("password")):
            app.logger.info(f"User with email {data.get('email')} password confirmed.")
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response_object = {
                    "status": "success",
                    "message": "Successfully logged in.",
                    "Authorization": auth_token,
                    "username": user.username,
                }
                return response_object, HTTPStatus.OK
        else:
            raise Unauthorized("Username or password invalid")

    @staticmethod
    def logout_user(data):
        """Logs out the user and blacklists the token"""
        if data:
            resp = User.decode_auth_token(data)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                return save_token(token=data)
            else:
                response_object: dict[str, str] = {"status": "fail", "message": resp}
                return response_object, HTTPStatus.UNAUTHORIZED
        else:
            raise Unauthorized("Provide a valid auth token.")

    @staticmethod
    def get_logged_in_user(new_request):
        """get the auth token"""
        auth_token = new_request.headers.get("Authorization")
        if auth_token:
            app.logger.info(
                f"Auth token received {auth_token} decoding and checking..."
            )
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                app.logger.info(f"Auth token {auth_token} decoded finding user {resp}")
                user = User.query.filter_by(id=resp).first()
                if user is None:
                    raise NotFound(user)
                app.logger.info("User found...")
                response_object = {
                    "status": "success",
                    "data": {
                        "user_id": user.id,
                        "email": user.email,
                        "username": user.username,
                        "admin": user.admin,
                        "registered_on": str(user.registered_on),
                    },
                }
                return response_object, HTTPStatus.OK
            response_object = {"status": "fail", "message": resp}
            return response_object, HTTPStatus.UNAUTHORIZED
        else:
            raise Unauthorized("Provide a valid auth token.")

    @staticmethod
    def get_logged_in_user_object(request) -> User | None:
        """Returns the logged in user"""
        auth_token = request.headers.get("Authorization")
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                if user:
                    return user
