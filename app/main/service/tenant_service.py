from datetime import datetime as dt
from http import HTTPStatus
from sqlite3 import IntegrityError

from sqlalchemy import update
from werkzeug.exceptions import NotFound, BadRequest

from app.main import db
from app.main.model.portfolio import Portfolio
from app.main.model.property import Property
from app.main.model.tenant import Tenant, TenantNote, TenantProfile, TitleEnum


def get_all_tenants_for_property(portfolio_id, property_id):
    """ Gets all the tenants for a property """
    portfolio = Portfolio.query.filter_by(id=portfolio_id).one()
    if portfolio is None:
        raise BadRequest("No Portfolio found")

    if property_id in [prop.id for prop in portfolio.properties]:
        tenants = Tenant.query.filter_by(property_id=property_id).all()
        return tenants
    else:
        raise BadRequest("Property id does't exist against this Portfolio.")

def update_tenant(property_id, tenant_id, data):
    '''Updates a tenent record'''
    if int(data['id']) != tenant_id:
        raise BadRequest("ID's do not match.")

    tenant = Tenant.query.filter_by(id=data['id']).filter(Tenant.property_id == property_id).first()

    if tenant is not None:
        data['date_of_birth'] = dt.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        data['tenancy_start_date'] = dt.strptime(data['tenancy_start_date'], '%Y-%m-%d').date()
        data['tenancy_end_date'] = dt.strptime(data['tenancy_end_date'], '%Y-%m-%d').date()
        try:
            stmt = update(Tenant).where(Tenant.id == tenant_id).values(data)
            db.session.execute(stmt)
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Successfully updated tenant.',
                'data': {
                    'id': tenant_id
                }
            }
            return response_object, HTTPStatus.NO_CONTENT
        except IntegrityError as err:
            raise IntegrityError(err) from err


def delete_tenant(property_id, tenant_id):
    '''Deletes a tenant'''
    tenant = Tenant.query.filter_by(property_id=property_id, id=tenant_id)
    if tenant.scalar() is None:
        raise NotFound()
    tenant.delete()
    db.session.commit()
    response_object = {
        'status': 'success',
        'message': 'Successfully deleted tenant.',
        'data': {}
    }
    return response_object, HTTPStatus.NO_CONTENT


def save_new_tenant(portfolio_id, property_id, data):
    '''Creates a new tenant against the supplied portfolio and property'''
    property = Property.query.filter_by(id=property_id).first()
    if property is None:
        raise NotFound()

    if property.portfolio_id != portfolio_id:
        raise NotFound('Property does not exist against this portfolio')

    # check if tenant already exists?
    existing_tenant = Tenant.query.filter(Tenant.property_id == property_id,
                                         Tenant.first_name == data['first_name'],
                                         Tenant.last_name == data['last_name'],
                                         Tenant.date_of_birth == data['date_of_birth']).scalar()
    if existing_tenant is not None:
        raise BadRequest('Tenant already exists at this property')

    title = TitleEnum[data['title']]
    new_tenant = Tenant(
        title=title,
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        date_of_birth=dt.strptime(data['date_of_birth'], '%Y-%m-%d'),
        job_title=data.get('job_title'),
        tenancy_start_date=dt.strptime(data['tenancy_start_date'], '%Y-%m-%d'),
        tenancy_end_date=data.get('tenancy_end_date')
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
    '''Returns a tenant by supplied id'''
    tenant = Tenant.query.filter(Tenant.property_id == property_id, Tenant.id == tenant_id).first()
    if tenant is None:
        raise NotFound("Tenant not found with id")
        # return "Tenant not found with id", HTTPStatus.NOT_FOUND
    if tenant.property.portfolio_id != portfolio_id:
        raise BadRequest('Issue with property portfolio supplied.')

    return tenant


def add_profile_to_tenant(tenant_id, image_str):
    '''Adds an image of the tenant to the tenant record'''
    # Save image off
    tenant_profile = TenantProfile(
        tenant_id=tenant_id,
        image=image_str
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


def save_changes(data) -> None:
    '''Saves changes'''
    db.session.add(data)
    db.session.commit()
