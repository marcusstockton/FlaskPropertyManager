from http import HTTPStatus

from flask import current_app as app

from app.main import db
from app.main.model.blacklist import BlacklistToken


def save_token(token):
    blacklist_token = BlacklistToken(token=token)
    try:
        # insert the token
        app.logger.info(f"Trying to add a blacklist token {blacklist_token}")
        db.session.add(blacklist_token)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Successfully logged out.'
        }
        app.logger.info(f"Token {blacklist_token} added to blacklist")
        return response_object, HTTPStatus.OK
    except Exception as e:
        app.logger.error(f"Unable to add Token {blacklist_token}. {e}")
        response_object = {
            'status': 'fail',
            'message': e
        }
        return response_object, HTTPStatus.OK
