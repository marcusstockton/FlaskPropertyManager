"""Authorisation Controller API Routes"""

from datetime import datetime
from flask import current_app as app
from flask import request
from flask_restx import Resource
from werkzeug.exceptions import NotFound, BadRequest
from app.main.service.auth_helper import Auth
from app.main.service.user_service import (
    reset_user_password,
    forgotten_password_user_lookup,
)
from ..util.dto.auth_dto import AuthDto
from ..service import mail_service

api = AuthDto.api
user_auth = AuthDto.user_auth
forgotten_password = AuthDto.forgotten_password
reset_password = AuthDto.reset_password


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


# This whole process needs a little re-work. As I don't have a UI, I can't add a link in the email, but if I had a UI, I would pass the token in the request,
# parse this out in the code behind, and use this along with a password input on a form to submit back, but for now, you can just copy the token from the email
# and use that in the password-reset request along with the new password.


@api.route("/forgot-password")
class ForgotPassword(Resource):
    """Password Reset endpoint"""

    @api.doc("Sends the user a password reset email")
    @api.expect(forgotten_password, validate=True)
    def post(self):
        """Function for sending out a password reset email"""
        post_data = request.json

        dob = datetime.strptime(post_data["date_of_birth"], "%Y-%m-%d")
        user = forgotten_password_user_lookup(post_data["email"], dob)
        if user:
            token = user.encode_auth_token(user.id, 5)

            url_reset = request.host + "/Auth/" + "password-reset" + "/" + token
            mail_service.send_email(
                post_data["email"],
                "Password Reset",
                f"Dear {user.first_name},\n You or someone else has requested that a new password be generated for your account.\n If you made this request, then please follow this link:\n {url_reset}",
            )
            return {"message": "Password reset link sent"}
        raise NotFound(user)


@api.route("/password-reset")
class ResetPassword(Resource):
    """Endpoint for sending password reset links"""

    @api.expect(reset_password, validate=True)
    def post(self):
        """Function to update the users password"""
        try:

            post_data = request.json

            reset_token = post_data["token"]
            password = post_data["password"]

            if not reset_token or not password:
                raise BadRequest()

            user = reset_user_password(reset_token, password)
            if user:
                mail_service.send_email(
                    user.email,
                    "Password Reset Complete",
                    f"Dear {user.first_name},\nPassword reset complete.",
                )
                return {"message": "Password reset complete"}

        except:
            raise BadRequest("Something went wrong resetting your password.")
