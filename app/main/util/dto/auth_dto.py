from flask_restx import Namespace, fields


class AuthDto:
    """Auth DTO"""

    api = Namespace("Auth", description="Authentication related operations")

    user_auth = api.model(
        "auth_details",
        {
            "email": fields.String(required=True, description="The email address"),
            "password": fields.String(required=True, description="The user password"),
        },
    )

    forgotten_password = api.model(
        "forgotten_password",
        {
            "email": fields.String(required=True, description="Your email address"),
            "date_of_birth": fields.Date(
                required=True, description="Your date of birth"
            ),
        },
    )

    reset_password = api.model(
        "reset-password",
        {
            "token": fields.String(required=True, description="Reset token"),
            "password": fields.String(required=True, description="The user password"),
        },
    )
