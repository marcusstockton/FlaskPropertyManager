import uuid
from datetime import datetime

from flask import current_app

from app.main import db
from app.main.model.user import User, Role


def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    owner_role = Role.query.filter_by(name='Owner').first()  # All users created are owners...for now
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            first_name=data['firstname'] if 'firstname' in data else None,
            last_name=data['lastname'] if 'lastname' in data else None,
            date_of_birth=datetime.strptime(data['dateofbirth'], '%Y-%m-%d') if 'dateofbirth' in data else None,
            registered_on=datetime.utcnow()
        )
        new_user.roles = [owner_role, ]
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    current_app.logger.info('Calling get all users')
    return User.query.all()


def get_a_user(public_id):
    current_app.logger.info('Calling get a user')
    return User.query.filter_by(public_id=public_id).first()


def generate_token(user):
    try:
        # generate the auth token
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'user_id': user.public_id,
            'user_name': user.username,
            'Authorization': auth_token
        }
        current_app.logger.info('auth_token created successfully')
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        current_app.logger.error(e)
        return response_object, 401


def save_changes(data):
    db.session.add(data)
    db.session.commit()
