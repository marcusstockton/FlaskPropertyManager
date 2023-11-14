from dataclasses import dataclass
import enum
from datetime import datetime

from sqlalchemy import LargeBinary
from sqlalchemy_utils import EmailType

from .property import Property
from .. import db


class TitleEnum(enum.Enum):
    """Title Enum"""

    Mr = 1
    Mrs = 2
    Miss = 3
    Ms = 4
    Lord = 5
    Sir = 6
    Dr = 7

    @classmethod
    def has_key(cls, name):
        """Checks name is in enum"""
        return name in cls.__members__  # solution above 1

    @classmethod
    def list(cls):
        """Lists the enums"""
        return list(map(lambda c: c.value, cls))


@dataclass
class Tenant(db.Model):
    """Tenant Model for storing tenants"""

    __tablename__ = "tenant"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    property_id: int = db.Column(db.Integer, db.ForeignKey(Property.id))
    property = db.relationship("Property", back_populates="tenants")
    phone_number: str = db.Column(db.String(20))
    email_address = db.Column(EmailType)
    title = db.Column(db.Enum(TitleEnum))
    first_name: str = db.Column(db.String(100))
    last_name: str = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date, nullable=True)
    job_title: str = db.Column(db.String(100))
    tenancy_start_date = db.Column(db.Date, nullable=False)
    tenancy_end_date = db.Column(db.Date, nullable=True)
    profile_pic = db.relationship(
        "TenantProfile", back_populates="tenant", uselist=False
    )  # uselist demotes a 1:1 relationship
    notes = db.relationship("TenantNote")
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


@dataclass
class TenantNote(db.Model):
    """Tenant note Model for storing tenant notes"""

    __tablename__ = "tenantNote"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tenant_id: int = db.Column(db.Integer, db.ForeignKey(Tenant.id))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    note: str = db.Column(db.String(2000))


@dataclass
class TenantProfile(db.Model):
    """Tenant profile pic stored as base64 str"""

    __tablename__ = "tenant-profile"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tenant_id: int = db.Column(db.Integer, db.ForeignKey(Tenant.id))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    image = db.Column(LargeBinary)
    tenant = db.relationship("Tenant", back_populates="profile_pic")
