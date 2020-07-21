from flask_restx import Namespace, fields


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
        'first_name': fields.String(required=True, description='first name'),
        'last_name': fields.String(required=True, description='last name'),
        'date_of_birth': fields.DateTime(required=True, description='date of birth'),
        'job_title': fields.String(required=True, description='job title'),
        'tenancy_start_date': fields.DateTime(required=True, description='tenancy start date'),
        'tenancy_end_date': fields.DateTime(required=True, description='tenancy end date'),
        'notes': fields.List(fields.Nested(tenant_notes), required=False, description='tenant notes'),
    })

    tenant_create = api.model('Tenant', {
        'first_name': fields.String(required=True, description='first name'),
        'last_name': fields.String(required=True, description='last name'),
        'date_of_birth': fields.DateTime(required=True, description='date of birth'),
        'job_title': fields.String(required=False, description='job title'),
        'tenancy_start_date': fields.DateTime(required=True, description='tenancy start date'),
        'tenancy_end_date': fields.DateTime(required=False, description='tenancy end date'),
        'notes': fields.List(fields.Nested(tenant_notes_create), required=False, description='tenant notes'),
    })