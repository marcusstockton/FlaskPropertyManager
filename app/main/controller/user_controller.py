from flask import current_app as app
from flask import request
from flask_restx import Resource

from app.main.util.decorator import token_required
from ..service.user_service import save_new_user, get_all_users, get_a_user
from ..util.dto.user_dto import UserDto

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):
	@token_required
	@api.doc('list_of_registered_users')
	@api.marshal_list_with(_user)
	def get(self):
		"""List all registered users"""
		app.logger.info(f"Getting all registered users")
		return get_all_users()

	@api.response(201, 'User successfully created.')
	@api.doc('create a new user')
	@api.expect(_user, validate=True)
	def post(self):
		"""Creates a new User """
		data = request.json
		app.logger.info(f"Creating a new user for {data['username']}")
		return save_new_user(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
	@token_required
	@api.doc('get a user')
	@api.marshal_with(_user)
	def get(self, public_id):
		"""get a user given its identifier"""
		app.logger.info(f"Finding user with public_id {public_id}")
		user = get_a_user(public_id)
		if not user:
			app.logger.error(f"Unable to find user with public_id {public_id}")
			api.abort(404)
		else:
			return user
