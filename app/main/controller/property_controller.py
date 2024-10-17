"""Property Controller API Routes"""

from collections import namedtuple

from http import HTTPStatus
from typing import List
from flask import request
from flask import current_app as app
from flask_restx import Namespace, OrderedModel, Resource, abort, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest

from app.main.model.property import Property
from app.main.model.user import User
from app.main.service.auth_helper import Auth


from ..service.property_service import (
    get_all_properties_for_portfolio,
    save_new_property,
    get_property_by_id,
    add_images_to_property,
)
from ..util.decorator import token_required
from ..util.dto.property_dto import PropertyDto

api: Namespace = PropertyDto.api
_property: reqparse.Model | OrderedModel = PropertyDto.property
_property_list: reqparse.Model | OrderedModel = PropertyDto.property_list
_property_create: reqparse.Model | OrderedModel = PropertyDto.property_create

upload_parser = reqparse.RequestParser()
upload_parser.add_argument(
    "images", location="files", type=FileStorage, required=True, action="append"
)


@api.route("/")
class PropertyList(Resource):
    """Property Items endpoint"""

    @token_required
    @api.doc("list_of_properties")
    @api.marshal_list_with(_property_list)
    def get(self, portfolio_id) -> List[Property]:
        """Get all properties for the portfolio"""
        user: User | None = Auth.get_logged_in_user_object(request)
        return get_all_properties_for_portfolio(user, portfolio_id)

    @token_required
    @api.response(201, "Property successfully created.")
    @api.doc("create a new property")
    @api.expect(_property_create, validate=True)
    def post(self, portfolio_id):
        """Creates a new Property"""
        data = api.payload
        return save_new_property(portfolio_id, data=data)


@api.route("/<int:property_id>")
class PropertyItem(Resource):
    """Single Property Endpoints"""

    @token_required
    @api.doc("property details")
    @api.marshal_list_with(_property)
    def get(self, portfolio_id, property_id) -> Property:
        """Gets the property by id."""
        user: User | None = Auth.get_logged_in_user_object(request)
        if user:
            return get_property_by_id(user, portfolio_id, property_id)
        raise BadRequest("User not found")

    @token_required
    @api.doc("update property")
    @api.marshal_with(_property)
    def put(self, portfolio_id, property_id):
        """Updates the property"""
        app.logger.info(f"Updating property {property_id} for portfolio {portfolio_id}")
        data = api.payload
        pass

    @token_required
    @api.doc("delete a property")
    def delete(self, property_id):
        """Deletes a property"""
        app.logger.info(f"Deleting property {property_id}")
        data = api.payload
        pass


@api.route("/<int:property_id>/images")
class PropertyImage(Resource):
    """Property Image endpoint"""

    @token_required
    @api.doc("add images of property")
    @api.expect(upload_parser)
    @api.marshal_list_with(_property)
    def post(self, portfolio_id, property_id):
        """Add images of property."""

        args: reqparse.ParseResult = upload_parser.parse_args()
        images = args["images"]
        ImageTuple = namedtuple("ImageTuple", ["file_name", "image"])
        if images:
            image_strings = []
            for image in images:
                img_ext = image.content_type.rsplit("/")[1]
                if img_ext.lower() not in app.config["UPLOAD_EXTENSIONS"]:
                    abort(
                        HTTPStatus=HTTPStatus.BAD_REQUEST, message="Invalid image type"
                    )
                image_string = image.read()
                img = ImageTuple(image.filename, image_string)
                image_strings.append(img)
            if image_strings is not None:
                return add_images_to_property(portfolio_id, property_id, image_strings)
        return BadRequest("No images passed in")
