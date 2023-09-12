from flask import current_app as app
from flask import request
from flask_restx import Resource, marshal

from app.main.util.decorator import token_required, admin_token_required
from ..service.user_service import (
    save_new_user,
    get_all_users,
    get_a_user,
    update_user,
    delete_user,
)
from ..util.dto.user_dto import UserDto

api = UserDto.api
_user = UserDto.user
_user_create = UserDto.user_create
_user_details = UserDto.user_details


@api.route("/")
class UserList(Resource):
    @admin_token_required
    @api.doc("list_of_registered_users")
    @api.marshal_list_with(_user)
    def get(self):
        """List all registered users"""
        app.logger.info(f"Getting all registered users")
        return get_all_users()

    @api.response(201, "User successfully created.")
    @admin_token_required
    @api.doc("create a new user")
    @api.expect(_user_create, validate=True)
    def post(self):
        """Creates a new User"""
        data = request.json
        app.logger.info(f"Creating a new user for {data['username']}")
        return save_new_user(data=data)


@api.route("/<public_id>")
@api.param("public_id", "The User identifier")
@api.response(404, "User not found.")
@api.response(200, "User record returned.")
class User(Resource):
    @token_required
    @api.doc("get a user")
    @api.marshal_with(_user_details)
    def get(self, public_id):
        """get a user given its identifier"""
        app.logger.info(f"Finding user with public_id {public_id}")
        user = get_a_user(public_id)
        if not user:
            app.logger.error(f"Unable to find user with public_id {public_id}")
            api.abort(404)
        else:
            return user

    @api.expect(_user_details, validate=True)
    def put(self, public_id):
        """update a user"""
        data = request.json
        app.logger.info(
            f"Updating user with public_id {public_id}, payload received {data}"
        )
        return update_user(public_id, data)

    @admin_token_required
    @api.response(204, "User Deleted.")
    def delete(self, public_id):
        """Deletes a user"""
        app.logger.info(f"Deleting user with public_id {public_id}")
        return delete_user(public_id)
