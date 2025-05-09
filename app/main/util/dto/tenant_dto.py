"""Tenant DTO"""

import base64
from datetime import date

from flask_restx import Namespace, fields

from ...model.tenant import TitleEnum


class Base64Decoder(fields.Raw):
    """Decode an image to a base 64 string"""

    def format(self, value):
        data_bytes = base64.b64encode(value)
        data = data_bytes.decode("utf-8")
        return data


class CalcuateAge(fields.Raw):
    """Calculates the tenants age"""

    def format(self, value):
        today = date.today()
        return (
            today.year
            - value.year
            - ((today.month, today.day) < (value.month, value.day))
        )


# class CurrentTenants(fields.Raw):
#     def format(self, value):
#         return value.upper()


# class FileLocationToUrl(fields.Raw):
#     def format(self, value):
#         return value


class TenantDto:
    """Flask-Restx Tenant related operations."""

    api = Namespace("Tenant", description="Tenant related operations")
    tenant_notes = api.model(
        "TenantNote",
        {
            "id": fields.Integer(required=True, description="id"),
            "created_date": fields.DateTime(required=False, description="date created"),
            "updated_date": fields.DateTime(
                required=False, description="date last updated"
            ),
            "note": fields.String(required=True, description="note"),
        },
    )

    tenant_profile = api.model(
        "TenantProfile",
        {
            "id": fields.Integer(required=True, description="id"),
            "created_date": fields.DateTime(required=False, description="date created"),
            "updated_date": fields.DateTime(
                required=False, description="date last updated"
            ),
            "image_base_64": Base64Decoder(attribute="image"),
        },
    )

    tenant_notes_create = api.model(
        "TenantNote",
        {
            "note": fields.String(required=True, description="note"),
        },
    )

    tenant = api.model(
        "Tenant",
        {
            "id": fields.Integer(required=True, description="id"),
            "title": fields.String(
                required=False,
                description="Title",
                enum=[x.name.casefold() for x in TitleEnum],
                attribute="title.name",
            ),
            "phone_number": fields.String(required=False, description="phone number"),
            "email_address": fields.String(required=False, description="email_address"),
            "first_name": fields.String(
                required=True, description="first name", attribute="first_name"
            ),
            "last_name": fields.String(required=True, description="last name"),
            "date_of_birth": fields.Date(required=True, description="date of birth"),
            "job_title": fields.String(required=True, description="job title"),
            "tenancy_start_date": fields.Date(
                required=True, description="tenancy start date"
            ),
            "tenancy_end_date": fields.Date(
                required=True, description="tenancy end date"
            ),
            "created_date": fields.DateTime(required=False, description="date created"),
            "updated_date": fields.DateTime(
                required=False, description="date last updated"
            ),
            "age": CalcuateAge(attribute="date_of_birth"),
            "profile_pic": fields.List(
                fields.Nested(tenant_profile),
                required=False,
                description="tenant profile pic",
            ),
            "notes": fields.List(
                fields.Nested(tenant_notes), required=False, description="tenant notes"
            ),
        },
    )

    tenant_list = api.model(
        "Tenant",
        {
            "id": fields.Integer(required=True, description="id"),
            "title": fields.String(
                required=False,
                description="title",
                enum=[x.name for x in TitleEnum],
                attribute="title.name",
            ),
            "phone_number": fields.String(required=False, description="phone number"),
            "first_name": fields.String(
                required=True, description="first name", attribute="first_name"
            ),
            "last_name": fields.String(required=True, description="last name"),
            "date_of_birth": fields.Date(required=True, description="date of birth"),
            "job_title": fields.String(required=True, description="job title"),
            "tenancy_start_date": fields.Date(
                required=True, description="tenancy start date"
            ),
            "tenancy_end_date": fields.Date(
                required=True, description="tenancy end date"
            ),
            "created_date": fields.DateTime(required=False, description="date created"),
            "updated_date": fields.DateTime(
                required=False, description="date last updated"
            ),
        },
    )

    tenant_create = api.model(
        "Tenant",
        {
            "title": fields.String(
                required=False,
                description="title",
                enum=[x.name for x in TitleEnum],
                attribute="title.name",
            ),
            "phone_number": fields.String(required=False, description="phone number"),
            "email_address": fields.String(required=True, description="email_address"),
            "first_name": fields.String(required=True, description="first name"),
            "last_name": fields.String(required=True, description="last name"),
            "date_of_birth": fields.Date(required=True, description="date of birth"),
            "job_title": fields.String(required=True, description="job title"),
            "tenancy_start_date": fields.Date(
                required=True, description="tenancy start date"
            ),
            "tenancy_end_date": fields.Date(
                required=False, description="tenancy end date"
            ),
        },
    )

    tenant_update = api.model(
        "Tenant",
        {
            "id": fields.Integer(required=True, description="id"),
            "title": fields.String(
                required=False,
                description="title",
                enum=[x.name for x in TitleEnum],
                attribute="title.name",
            ),
            "phone_number": fields.String(required=False, description="phone number"),
            "first_name": fields.String(
                required=True, description="first name", attribute="first_name"
            ),
            "last_name": fields.String(required=True, description="last name"),
            "date_of_birth": fields.Date(required=True, description="date of birth"),
            "job_title": fields.String(required=True, description="job title"),
            "tenancy_start_date": fields.Date(
                required=True, description="tenancy start date"
            ),
            "tenancy_end_date": fields.Date(
                required=False, description="tenancy end date"
            ),
        },
    )
    tenant_documents = api.model(
        "TenantDocument",
        {
            "id": fields.Integer(required=True, description="id"),
            "tenant_id": fields.Integer(required=True, description="tenant id"),
            "created_date": fields.DateTime(required=False, description="date created"),
            "updated_date": fields.DateTime(
                required=False, description="date last updated"
            ),
            "document_type_id": fields.Integer(
                required=True, description="document type"
            ),
            "file_name": fields.String(required=True, description="last name"),
            "file_ext": fields.String(required=True, description="last name"),
            "document_blob": fields.String(),
        },
    )
