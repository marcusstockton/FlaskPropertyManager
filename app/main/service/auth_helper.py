from http import HTTPStatus

from flask import current_app as app

from app.main.model.user import User
from ..service.blacklist_service import save_token


class Auth:
	@staticmethod
	def login_user(data):
		try:
			# fetch the user data
			user = User.query.filter_by(email=data.get('email')).first()
			app.logger.info(f"User with email {data.get('email')} found...checking password...")
			if user and user.check_password(data.get('password')):
				app.logger.info(f"User with email {data.get('email')} password confirmed. Generating token")
				auth_token = user.encode_auth_token(user.id)
				if auth_token:
					response_object = {
						'status': 'success',
						'message': 'Successfully logged in.',
						'Authorization': auth_token,
						'username': user.username
					}
					return response_object, HTTPStatus.OK
			else:
				response_object = {
					'status': 'fail',
					'message': 'Email or password does not match.'
				}
				return response_object, HTTPStatus.UNAUTHORIZED

		except Exception as e:
			print(e)
			response_object = {
				'status': 'fail',
				'message': 'Try again'
			}
			return response_object, HTTPStatus.INTERNAL_SERVER_ERROR

	@staticmethod
	def logout_user(data):
		if data:
			auth_token = data.split(" ")[1]
		else:
			auth_token = ''
		if auth_token:
			resp = User.decode_auth_token(auth_token)
			if not isinstance(resp, str):
				# mark the token as blacklisted
				return save_token(token=auth_token)
			else:
				response_object = {
					'status': 'fail',
					'message': resp
				}
				return response_object, HTTPStatus.UNAUTHORIZED
		else:
			response_object = {
				'status': 'fail',
				'message': 'Provide a valid auth token.'
			}
			return response_object, HTTPStatus.FORBIDDEN
			
	@staticmethod
	def get_logged_in_user(new_request):
		# get the auth token
		auth_token = new_request.headers.get('Authorization')
		if auth_token:
			app.logger.info(f"Auth token received {auth_token} decoding and checking...")
			resp = User.decode_auth_token(auth_token)
			if not isinstance(resp, str):
				app.logger.info(f"Auth token {auth_token} decoded finding user {resp}")
				user = User.query.filter_by(id=resp).first()
				app.logger.info(f"User found...")
				response_object = {
					'status': 'success',
					'data': {
						'user_id': user.id,
						'email': user.email,
						'username': user.username,
						'admin': user.admin,
						'registered_on': str(user.registered_on)
					}
				}
				return response_object, HTTPStatus.OK
			response_object = {
				'status': 'fail',
				'message': resp
			}
			return response_object, HTTPStatus.UNAUTHORIZED
		else:
			response_object = {
				'status': 'fail',
				'message': 'Provide a valid auth token.'
			}
			return response_object, HTTPStatus.UNAUTHORIZED

	def get_logged_in_user_object(request):
		auth_token = request.headers.get('Authorization')
		if auth_token:
			resp = User.decode_auth_token(auth_token)
			if not isinstance(resp, str):
				user = User.query.filter_by(id=resp).first()
				if user:
					return user
