from email.mime import image
import os
from datetime import datetime as dt
from app.main.model import tenant

from flask import current_app
from werkzeug.utils import secure_filename
from http import HTTPStatus

from app.main import db
from app.main.model.property import Property
from app.main.model.tenant import Tenant, TenantNote, TenantProfile


def get_all_tenants_for_property(property_id):
    tenants = Tenant.query.filter_by(property_id=property_id).all()

    return tenants


def update_tenant(property_id, data, profile):
    tenant = Tenant.query.filter_by(id=data['id'])\
                        .filter(property_id=property_id).update(data)
    save_changes(tenant)
    response_object = {
        'status': 'success',
        'message': 'Successfully updated tenant.',
        'data': {
            'id': tenant.id
        }
    }
    return response_object, HTTPStatus.NO_CONTENT
    

def delete_tenant(property_id, tenant_id):
    tenant = Tenant.query.filter_by(property_id=property_id).filter(id=tenant_id)
    if tenant is not None:
        Tenant.query.filter_by(property_id=property_id).filter(id=tenant_id).delete()
        save_changes(tenant)
        response_object = {
            'status': 'success',
            'message': 'Successfully deleted tenant.',
            'data': {}
        }
        return response_object, HTTPStatus.NO_CONTENT
    return 'Not found', HTTPStatus.NOT_FOUND


def save_new_tenant(portfolio_id, property_id, data, profile):
    property = Property.query.filter_by(id=property_id).first()
    if property is None:
        response_object = {
            'status': 'fail',
            'message': 'No property found',
        }
        return response_object, HTTPStatus.BAD_REQUEST
    
    if property.portfolio_id != portfolio_id:
        response_object = {
            'status': 'fail',
            'message': 'Property does not exist against this portfolio',
        }
        return response_object, HTTPStatus.NOT_FOUND

    # check if tenant already exists?
    if Tenant.query.filter_by(property_id=property_id)\
            .filter(portfolio__id=portfolio_id)\
            .filter(first_name=data['first_name'])\
            .filter(date_of_birth=data['first_name'])\
            .filter(last_name=data['last_name']).scalar():
        response_object = {
            'status': 'fail',
            'message': 'Tenant already exists at this property',
            'data': {
                'first_name': data['first_name'],
                'last_name': data['last_name']
            }
        }
        return response_object, HTTPStatus.BAD_REQUEST

    new_tenant = Tenant(
        title=data['title'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        date_of_birth=dt.strptime(data['date_of_birth'], '%Y-%m-%d'),
        job_title=data['job_title'],
        tenancy_start_date=dt.strptime(data['tenancy_start_date'], '%Y-%m-%d'),
        tenancy_end_date=dt.strptime(data['tenancy_end_date'], '%Y-%m-%d')
    )
    if 'note' in data:
        new_note = TenantNote(
            note=data['note']
        )
        new_tenant.notes.append(new_note)    
    
    property.tenants.append(new_tenant)
    
    save_changes(property)

    response_object = {
        'status': 'success',
        'message': 'Successfully created tenant.',
        'data': {
            'id': new_tenant.id
        }
    }
    return response_object, HTTPStatus.CREATED


def get_tenant_by_id(portfolio_id, property_id, tenant_id):
    tenant = Tenant.query.filter_by(property_id=property_id).filter_by(id=tenant_id).first()
    if tenant.property.portfolio_id != portfolio_id:
        response_object = {
            'status': 'fail',
            'message': 'Issue with property portfolio supplied.',
            'data': {
                'portfolio_id': portfolio_id,
                'property_id': property_id
            }
        }
        return response_object, HTTPStatus.BAD_REQUEST
    return tenant


def add_profile_to_tenant(tenant_id, image_str):
    # Save image off
    tenant_profile = tenant.TenantProfile(
        tenant_id = tenant_id,
        image = image_str
    )
    save_changes(tenant_profile)
    response_object = {
        'status': 'success',
        'message': 'Successfully uploaded the tenant image.',
        'data': {
            'id': tenant_profile.id
        }
    }
    return response_object, HTTPStatus.CREATED


def save_changes(data):
    db.session.add(data)
    db.session.commit()
