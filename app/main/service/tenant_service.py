import os
from datetime import datetime as dt

from flask import current_app
from werkzeug.utils import secure_filename

from app.main import db
from app.main.model.property import Property
from app.main.model.tenant import Tenant, TenantNote


def get_all_tenants_for_property(portfolio_id, property_id):
    return Tenant.query.filter_by(portfolio_id=portfolio_id)\
                        .filter(property_id=property_id).all()


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
    return response_object, 204 
    

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
        return response_object, 201
    return 'Not found', 404


def save_new_tenant(portfolio_id, property_id, data, profile):
    property = Property.query.filter_by(id=property_id).first()
    if property is None:
        response_object = {
            'status': 'fail',
            'message': 'No property found',
        }
        return response_object, 409
    
    if property.portfolio_id != portfolio_id:
        response_object = {
            'status': 'fail',
            'message': 'Property does not exist against this portfolio',
        }
        return response_object, 404

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
        return response_object, 409

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

    if profile is not None:
        __add_profile_to_tenant(new_tenant, profile)

    response_object = {
        'status': 'success',
        'message': 'Successfully created tenant.',
        'data': {
            'id': new_tenant.id
        }
    }
    return response_object, 201


def get_tenant_by_id(portfolio_id, property_id, tenant_id):
    return Tenant.query.filter_by(property_id=property_id).filter_by(id=tenant_id).first()


def __add_profile_to_tenant(new_tenant, profile):
    # Save image off
    img_name = secure_filename(profile.filename)
    tenant_id_folder = os.path.join('tenants', str(new_tenant.id))
    profile_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], tenant_id_folder)
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)
    profile.save(os.path.join(profile_dir, img_name))
    new_tenant.profile_pic = os.path.join(tenant_id_folder, img_name)
    save_changes(new_tenant)


def save_changes(data):
    db.session.add(data)
    db.session.commit()
