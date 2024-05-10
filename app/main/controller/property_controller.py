"""Property Controller API Routes"""

from collections import namedtuple

from http import HTTPStatus
from flask import request
from flask import current_app as app
from flask_restx import Resource, abort, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest


from ..service.property_service import (
    get_all_properties_for_portfolio,
    save_new_property,
    get_property_by_id,
    add_images_to_property,
)
from ..util.decorator import token_required
from ..util.dto.property_dto import PropertyDto

api = PropertyDto.api
_property = PropertyDto.property
_property_list = PropertyDto.property_list
_property_create = PropertyDto.property_create

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
    def get(self, portfolio_id):
        """Get all properties for the portfolio"""
        return get_all_properties_for_portfolio(portfolio_id)

    @token_required
    @api.response(201, "Property successfully created.")
    @api.doc("create a new property")
    @api.expect(_property_create, validate=True)
    def post(self, portfolio_id):
        """Creates a new Property"""
        data = request.json
        return save_new_property(portfolio_id, data=data)


@api.route("/<int:property_id>")
class PropertyItem(Resource):
    """Single Property Endpoints"""

    @token_required
    @api.doc("property details")
    @api.marshal_list_with(_property)
    def get(self, portfolio_id, property_id):
        """Gets the property by id."""
        return get_property_by_id(portfolio_id, property_id)

    @token_required
    @api.doc("update property")
    @api.marshal_with(_property)
    def put(self, portfolio_id, property_id):
        """Updates the property"""
        app.logger.info(f"Updating property {property_id} for portfolio {portfolio_id}")
        data = request.get_json(force=True)
        pass

    @token_required
    @api.doc("delete a property")
    def delete(self, property_id):
        """Deletes a property"""
        app.logger.info(f"Deleting property {property_id}")
        data = request.get_json(force=True)
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

        args = upload_parser.parse_args()
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
