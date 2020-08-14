from .. import db
import datetime
from .property import Property
import enum


class TitleEnum(enum.Enum):
	Mr = 1
	Mrs = 2
	Miss = 3
	Lord = 4
	Sir = 5


class Tenant(db.Model):
	""" Tenant Model for storing tenants """
	__tablename__ = "tenant"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	property_id = db.Column(db.Integer, db.ForeignKey(Property.id))
	property = db.relationship("Property", foreign_keys=[property_id])
	title = db.Column(db.Enum(TitleEnum))
	first_name = db.Column(db.String(100))
	last_name = db.Column(db.String(100))
	date_of_birth = db.Column(db.Date, nullable=True)
	job_title = db.Column(db.String(100))
	tenancy_start_date = db.Column(db.Date, nullable=False)
	tenancy_end_date = db.Column(db.Date, nullable=True)
	profile_pic = db.Column(db.String(255), nullable=True)
	notes = db.relationship("TenantNote")


class TenantNote(db.Model):
	""" Tenant note Model for storing tenant notes """
	__tablename__ = "tenantNote"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	tenant_id = db.Column(db.Integer, db.ForeignKey(Tenant.id))
	created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	note = db.Column(db.String(2000))
