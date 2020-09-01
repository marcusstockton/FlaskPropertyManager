from flask import  request
from flask_restx import Namespace, fields
from werkzeug.datastructures import FileStorage
from ...model.tenant import TitleEnum
import json
import os
import base64
from flask import current_app


class File(fields.Raw):
    """ Custom field to return a file...hopefully.... """
    def format(self, value):
        with open(os.path.join(current_app.config['UPLOAD_FOLDER'], value), "rb") as imageFile:
            str = base64.b64encode(imageFile.read())
            return json.dumps(str.decode()).replace("'", '"')[1:-1]


class CurrentTenants(fields.Raw):
    def format(self, value):
        return value.upper()


class FileLocationToUrl(fields.Raw):
    def format(self, value):
        return request.host + '/Uploads/' + value


class TenantDto:
    api = Namespace('tenant', description='tenant related operations')

    tenant_notes = api.model('TenantNote', {
        'id': fields.String(required=True, description='id'),
        'created_date': fields.DateTime(required=True, description='date created'),
        'note': fields.String(required=True, description='note'),
    })

    tenant_notes_create = api.model('TenantNote', {
        'note': fields.String(required=True, description='note'),
    })

    tenant = api.model('Tenant', {
        'id': fields.String(required=True, description='id'),
        'title': fields.String(required=False, description='title'),
        'first_name': fields.String(required=True, description='first name'),
        'last_name': fields.String(required=True, description='last name'),
        'date_of_birth': fields.DateTime(required=True, description='date of birth'),
        'job_title': fields.String(required=True, description='job title'),
        'tenancy_start_date': fields.DateTime(required=True, description='tenancy start date'),
        'tenancy_end_date': fields.DateTime(required=True, description='tenancy end date'),
        'profile': File(required=False, attribute='profile_pic'),
        'profile_url': FileLocationToUrl(required=False, attribute='profile_pic'),
        'notes': fields.List(fields.Nested(tenant_notes), required=False, description='tenant notes'),
    })
    
    tenant_create_parser = api.parser()
    tenant_create_parser.add_argument('profile', location='files', type=FileStorage, required=False, help="Upload an image of the tenant")
    tenant_create_parser.add_argument("title", location='form', type='string', required=False, choices=([title.name for title in TitleEnum]))
    tenant_create_parser.add_argument("first_name", location='form', type='string', required=True)
    tenant_create_parser.add_argument("last_name", location='form', type='string', required=True)
    tenant_create_parser.add_argument("date_of_birth", location='form', type="date", required=False, help="yyyy-mm-dd")
    tenant_create_parser.add_argument("job_title", location='form', type='string', required=False)
    tenant_create_parser.add_argument("tenancy_start_date", location='form', type='date', required=True, help="yyyy-mm-dd")
    tenant_create_parser.add_argument("tenancy_end_date", location='form', type='date', required=False, help="yyyy-mm-dd")
