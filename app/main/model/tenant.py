from datetime import datetime
import enum

from sqlalchemy_utils import EmailType
from sqlalchemy import LargeBinary

from .property import Property
from .. import db


class TitleEnum(enum.Enum):
	Mr = 1
	Mrs = 2
	Miss = 3
	Ms = 4
	Lord = 5
	Sir = 6
	Dr = 7


class Tenant(db.Model):
	""" Tenant Model for storing tenants """
	__tablename__ = "tenant"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	property_id = db.Column(db.Integer, db.ForeignKey(Property.id))
	property = db.relationship("Property", foreign_keys=[property_id])
	phone_number = db.Column(db.String(20))
	email_address = db.Column(EmailType)
	title = db.Column(db.Enum(TitleEnum))
	first_name = db.Column(db.String(100))
	last_name = db.Column(db.String(100))
	date_of_birth = db.Column(db.Date, nullable=True)
	job_title = db.Column(db.String(100))
	tenancy_start_date = db.Column(db.Date, nullable=False)
	tenancy_end_date = db.Column(db.Date, nullable=True)
	profile_pic = db.relationship("TenantProfile", back_populates="tenant", uselist=False)
	notes = db.relationship("TenantNote")
	created_date = db.Column(db.DateTime, default=datetime.utcnow)
	updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  

	def __repr__(self):
		return "<Tenant 'Id:{} Title:{} FirstName:{} LastName{}'>".format(self.id, self.title, self.first_name, self.last_name)


class TenantNote(db.Model):
	""" Tenant note Model for storing tenant notes """
	__tablename__ = "tenantNote"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	tenant_id = db.Column(db.Integer, db.ForeignKey(Tenant.id))
	created_date = db.Column(db.DateTime, default=datetime.utcnow)
	updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  
	note = db.Column(db.String(2000))

	def __repr__(self):
		return "<Tenant Note 'Id:{} Note:{}'>".format(self.id, self.note)


class TenantProfile(db.Model):
	"""Tenant profile pic stored as base64 str"""
	__tablename__ = "tenant-profile"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	tenant_id = db.Column(db.Integer, db.ForeignKey(Tenant.id))
	created_date = db.Column(db.DateTime, default=datetime.utcnow)
	updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  
	image = db.Column(LargeBinary)
	tenant = db.relationship("Tenant", back_populates="profile_pic")

	def __repr__(self):
		return "<Tenant Profile 'Id:{} tenant:{}'>".format(self.id, self.tenant.first_name + ' ' + self.tenant.last_name)