import base64
import imghdr
from collections import namedtuple

from flask import request
from flask import current_app as app
from flask_restx import Resource, abort
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest

from ..service.property_service import get_all_properties_for_portfolio, save_new_property, get_property_by_id, \
	add_images_to_property
from ..util.decorator import token_required
from ..util.dto.property_dto import PropertyDto

api = PropertyDto.api
_property = PropertyDto.property
_property_list = PropertyDto.property_list
_property_create = PropertyDto.property_create

upload_parser = api.parser()
upload_parser.add_argument('images', location='files', type=FileStorage, required=True, action="append")


@api.route('/')
class PropertyList(Resource):
	@token_required
	@api.doc('list_of_properties')
	@api.marshal_list_with(_property_list)
	def get(self, portfolio_id):
		"""Get all properties for the portfolio"""
		return get_all_properties_for_portfolio(portfolio_id)

	@token_required
	@api.response(201, 'Property successfully created.')
	@api.doc('create a new property')
	@api.expect(_property_create, validate=True)
	def post(self, portfolio_id):
		"""Creates a new Property """
		data = request.json
		return save_new_property(portfolio_id, data=data)


@api.route('/<int:property_id>')
class PropertyItem(Resource):
	@token_required
	@api.doc('property details')
	@api.marshal_list_with(_property)
	def get(self, portfolio_id, property_id):
		""" Gets the property by id. """
		return get_property_by_id(portfolio_id, property_id)

	@token_required
	@api.doc('update property')
	@api.marshal_list_with(_property)
	def put(self, portfolio_id, property_id):
		"""Updates the property"""
		data = request.json
		pass


@api.route('/<int:property_id>/images')
class PropertyImage(Resource):
	@token_required
	@api.doc('add images of property')
	@api.expect(upload_parser)
	@api.marshal_list_with(_property)
	def post(self, portfolio_id, property_id):
		""" Add images of property. """
		args = upload_parser.parse_args()
		images = args['images']
		ImageTuple = namedtuple('ImageTuple', ['file_name', 'image'])
		if images:
			image_strings = []
			for image in images:
				# The imghdr module determines the type of image contained in a file or byte stream.
				if imghdr.what(image) not in app.config['UPLOAD_EXTENSIONS']:
					abort(400, message="Invalid image type")
				image_string = base64.b64encode(image.read())
				img = ImageTuple(image.filename, image_string)
				image_strings.append(img)
			if image_strings is not None:
				return add_images_to_property(portfolio_id, property_id, image_strings)
		return BadRequest("No images passed in")
