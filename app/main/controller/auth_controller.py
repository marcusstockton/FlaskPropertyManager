"""Authorisation Controller API Routes"""

from flask import current_app as app
from flask import request
from flask_restx import Resource

from app.main.service.auth_helper import Auth
from ..util.dto.auth_dto import AuthDto

api = AuthDto.api
user_auth = AuthDto.user_auth


@api.route("/login")
class UserLogin(Resource):
    """User Login Resource"""

    @api.doc("user login")
    @api.expect(user_auth, validate=True)
    @api.response(401, "Invalid username and/or password")
    def post(self):
        """Logs a User in"""
        # get the post data
        app.logger.info(f"Received login details for  {request.json}")
        post_data = request.json

        return Auth.login_user(data=post_data)


@api.route("/logout")
class LogoutAPI(Resource):
    """Logout Resource"""

    @api.doc("logout a user")
    def post(self):
        """Logs a user out"""
        # get auth token
        auth_header = request.headers.get("Authorization")
        return Auth.logout_user(data=auth_header)
