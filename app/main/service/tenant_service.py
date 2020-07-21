from app.main import db
from app.main.model.tenant import Tenant
from app.main.model.property import Property
from datetime import datetime as dt

def get_all_tenants_for_property(propertyId):
    return Tenant.query.filter_by(property_id=propertyId).all()

def save_new_tenant(portfolioId, propertyId, data):
    property = Property.query.filter_by(id=propertyId).first()
    if property is None:
        response_object = {
            'status': 'fail',
            'message': 'No property found',
        }
        return response_object, 409
    
    if property.portfolio_id != portfolioId:
        response_object = {
            'status': 'fail',
            'message': 'Property does not exist against this portfolio',
        }
        return response_object
    
    new_tenant = Tenant(
        first_name = data['first_name'],
        last_name = data['last_name'],
        date_of_birth = dt.strptime(data['date_of_birth'], '%Y-%m-%d'),
        job_title = data['job_title'],
        tenancy_start_date = dt.strptime(data['tenancy_start_date'], '%Y-%m-%d'),
        tenancy_end_date = dt.strptime(data['tenancy_end_date'], '%Y-%m-%d') 
            if 'tenancy_end_date' in data 
            else dt.strptime(str(dt.min.date()), '%Y-%m-%d'),
    )
    if 'note' in data:
        # We've got a note to add in...?
        pass
    
    property.tenants.append(new_tenant)
    save_changes(property)
    response_object = {
        'status': 'success',
        'message': 'Successfully created tenant.',
        'data': {
            'id': new_tenant.id
        }
    }
    return response_object, 201


def save_changes(data):
    db.session.add(data)
    db.session.commit()


