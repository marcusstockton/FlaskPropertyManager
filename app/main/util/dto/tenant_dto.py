import json
import base64

from flask import current_app
from flask import request
from flask_restx import Namespace, fields

from ...model.tenant import TitleEnum

class Base64Decoder(fields.Raw):
    def format(self, value):
        data_bytes = base64.b64encode(value)
        data = data_bytes.decode("utf-8")
        return data


class CurrentTenants(fields.Raw):
    def format(self, value):
        return value.upper()


class FileLocationToUrl(fields.Raw):
    def format(self, value):
        return value


class TenantDto:
    api = Namespace('tenant', description='tenant related operations')

    tenant_notes = api.model('TenantNote', {
        'id': fields.String(required=True, description='id'),
        'created_date': fields.DateTime(required=False, description='date created'),
        'updated_date': fields.DateTime(required=False, description='date last updated'),
        'note': fields.String(required=True, description='note'),
    })

    tenant_profile = api.model('TenantProfile', {
        'id': fields.String(required=True, description='id'),
        'created_date': fields.DateTime(required=False, description='date created'),
        'updated_date': fields.DateTime(required=False, description='date last updated'),
        'image_base_64': Base64Decoder(attribute="image"),
    })

    tenant_notes_create = api.model('TenantNote', {
        'note': fields.String(required=True, description='note'),
    })

    tenant = api.model('Tenant', {
        'id': fields.String(required=True, description='id'),
        'title': fields.String(required=False, description='title', enum=[x.name for x in TitleEnum], attribute='title.name'),
        'phone_number': fields.String(required=False, description='phone number'),
        'first_name': fields.String(required=True, description='first name', attribute='first_name'),
        'last_name': fields.String(required=True, description='last name'),
        'date_of_birth': fields.DateTime(required=True, description='date of birth'),
        'job_title': fields.String(required=True, description='job title'),
        'tenancy_start_date': fields.DateTime(required=True, description='tenancy start date'),
        'tenancy_end_date': fields.DateTime(required=True, description='tenancy end date'),
        'profile_pic': fields.List(fields.Nested(tenant_profile), required=False, description='tenant profile pic'),
        'notes': fields.List(fields.Nested(tenant_notes), required=False, description='tenant notes'),
        'created_date': fields.DateTime(required=False, description='date created'),
        'updated_date': fields.DateTime(required=False, description='date last updated'),
    })
    
    tenant_create_parser = api.parser()
    tenant_create_parser.add_argument("title", location='form', type='string', required=False, choices=([title.name for title in TitleEnum]))
    tenant_create_parser.add_argument("first_name", location='form', type='string', required=True)
    tenant_create_parser.add_argument("last_name", location='form', type='string', required=True)
    tenant_create_parser.add_argument("date_of_birth", location='form', type="date", required=False, help="yyyy-mm-dd")
    tenant_create_parser.add_argument("job_title", location='form', type='string', required=False)
    tenant_create_parser.add_argument("tenancy_start_date", location='form', type='date', required=True, help="yyyy-mm-dd")
    tenant_create_parser.add_argument("tenancy_end_date", location='form', type='date', required=False, help="yyyy-mm-dd")
