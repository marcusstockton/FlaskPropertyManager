"""Tenant Controller API Routes"""

from http import HTTPStatus
from typing import List
from flask import current_app as app
from flask import request
from flask_restx import Model, Namespace, OrderedModel, Resource, abort
from flask_restx.reqparse import RequestParser
from werkzeug.datastructures import FileStorage

from app.main.model.tenant import Tenant

from ..service.tenant_service import (
    add_tenant_document,
    get_all_tenants_for_property,
    get_tenant_documents,
    save_new_tenant,
    get_tenant_by_id,
    delete_tenant,
    add_profile_to_tenant,
    update_tenant,
)
from ..util.decorator import token_required
from ..util.dto.tenant_dto import TenantDto

api: Namespace = TenantDto.api
_tenant: Model | OrderedModel = TenantDto.tenant
_tenant_list: Model | OrderedModel = TenantDto.tenant_list
_tenant_create: Model | OrderedModel = TenantDto.tenant_create
_tenant_update: Model | OrderedModel = TenantDto.tenant_update
_tenant_documents: Model | OrderedModel = TenantDto.tenant_documents

upload_parser: RequestParser = api.parser()
upload_parser.add_argument(
    "image",
    location="files",
    type=FileStorage,
    required=True,
    help="Image file cannot empty",
)
doc_upload_parser: RequestParser = api.parser()
doc_upload_parser.add_argument("document_type_id", type=int, required=True)
doc_upload_parser.add_argument(
    "file",
    location="files",
    type=FileStorage,
    required=True,
    help="File cannot empty",
)


@api.route("/")
class TenantList(Resource):
    """Tenant List API Endpoints"""

    @token_required
    @api.doc("list_of_tenants")
    @api.marshal_list_with(_tenant_list)
    def get(self, portfolio_id, property_id) -> List[Tenant]:
        """Get all tenants for the property"""
        app.logger.info(f"Getting all tenants for propertyId {property_id}")
        return get_all_tenants_for_property(portfolio_id, property_id)

    @token_required
    @api.response(201, "Tenant successfully created.")
    @api.doc(
        "create a new tenant against a property",
        responses={
            201: "Tenant successfully created.",
            404: "Property does not exist against this portfolio",
            409: "Tenant already exists",
        },
    )
    @api.expect(_tenant_create, validate=True)
    @api.marshal_with(_tenant_create)
    def post(self, portfolio_id, property_id):
        """Creates a new Tenant"""
        data = request.get_json(force=True)
        app.logger.info(f"Adding new tenant {data['email_address']} to {property_id}")
        return save_new_tenant(portfolio_id, property_id, data)


@api.route("/<int:tenant_id>")
class TenantItem(Resource):
    """Singular Tenant API endpoints"""

    @token_required
    @api.doc(
        "tenant details",
        responses={403: "Not Authorized", 400: "Bad Request", 200: "Ok"},
    )
    @api.marshal_with(_tenant)
    def get(self, portfolio_id, property_id, tenant_id):
        """Gets a tenant by Id"""
        app.logger.info(f"Finding tenant by id {tenant_id}")
        return get_tenant_by_id(portfolio_id, property_id, tenant_id)

    @token_required
    @api.doc(
        "tenant delete",
        responses={403: "Not Authorized", 400: "Bad Request", 204: "No Content"},
    )
    @api.marshal_with(_tenant)
    def delete(self, portfolio_id, property_id, tenant_id):
        """Deletes a tenant."""
        app.logger.info(
            f"Deleting tenant id {tenant_id} for property {property_id} and portfolio {portfolio_id}"
        )
        return delete_tenant(property_id, tenant_id)

    @token_required
    @api.doc(
        "tenant update",
        responses={403: "Not Authorized", 400: "Bad Request", 204: "Updated"},
    )
    @api.expect(_tenant_update, validate=True)
    def put(self, portfolio_id, property_id, tenant_id):
        """Update a tenant details"""
        data = request.json
        app.logger.info(
            f"Updating tenant id {tenant_id} for property {property_id} and portfolio {portfolio_id}"
        )
        return update_tenant(property_id, tenant_id, data)


@api.route("/<int:tenant_id>/images")
class TenantImage(Resource):
    """Tenant Image API Endpoints"""

    @token_required
    @api.doc(
        "Add an image of the tenant",
        responses={403: "Not Authorized", 400: "Bad Request", 201: "Created"},
    )
    @api.expect(upload_parser)
    def post(self, portfolio_id, property_id, tenant_id):
        """Adds a tenant profile pic."""
        app.logger.info(
            f"Adding tenant profile for tenant {tenant_id}, property {property_id}, portfolio {portfolio_id}"
        )
        args = upload_parser.parse_args()
        file = args["image"]
        if file:
            img_ext = file.content_type.rsplit("/")[1]
            if img_ext.lower() not in app.config["UPLOAD_EXTENSIONS"]:
                abort(HTTPStatus=HTTPStatus.BAD_REQUEST, message="Invalid image type")
            # Save image as base64 string
            # verify user has permission to do this...?
            app.logger.info(
                f"Adding a tenant profile image {file.filename} for tenant id {tenant_id}"
            )
            image_string = file.read()
            return add_profile_to_tenant(tenant_id, image_string)


@api.route("/<int:tenant_id>/documents")
class TenantDocument(Resource):
    """Tenant Documents API endpoints"""

    @api.expect(doc_upload_parser)
    def post(self, portfolio_id: int, property_id: int, tenant_id: int):
        args = doc_upload_parser.parse_args()
        doc_data = args["file"]
        print(type(doc_data))
        doc_type_id = args["document_type_id"]
        app.logger.info(
            f"file data received: name: {doc_data.filename}, ext:{doc_data.content_type.rsplit("/")[1]}, tenant_id: {tenant_id}"
        )

        return add_tenant_document(
            portfolio_id, property_id, tenant_id, doc_type_id, doc_data
        )

    @api.marshal_list_with(_tenant_documents)
    def get(self, portfolio_id: int, property_id: int, tenant_id):
        app.logger.info(f"Finding tenant documents for tenant id {tenant_id}")
        return get_tenant_documents(tenant_id)
