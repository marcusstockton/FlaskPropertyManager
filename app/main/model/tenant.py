from dataclasses import dataclass
import enum
from datetime import datetime
from typing import List
from sqlalchemy.orm import Mapped

from sqlalchemy import LargeBinary
from sqlalchemy_utils import EmailType

from app.main.model.base import BaseClass

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
class Tenant(BaseClass):
    """Tenant Model for storing tenants"""

    __tablename__ = "tenant"
    # id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    property_id: int = db.Column(db.Integer, db.ForeignKey(Property.id))
    property = db.relationship("Property", back_populates="tenants")
    phone_number: str = db.Column(db.String(20))
    email_address: str = db.Column(EmailType)
    title: TitleEnum = db.Column(db.Enum(TitleEnum))
    first_name: str = db.Column(db.String(100))
    last_name: str = db.Column(db.String(100))
    date_of_birth: datetime = db.Column(db.Date, nullable=True)
    job_title: str = db.Column(db.String(100))
    tenancy_start_date: datetime = db.Column(db.Date, nullable=False)
    tenancy_end_date: datetime = db.Column(db.Date, nullable=True)
    smoker: bool = db.Column(db.Boolean, nullable=False, default=False)
    profile_pic: Mapped["TenantProfile"] = db.relationship(
        "TenantProfile", back_populates="tenant", uselist=False
    )  # uselist demotes a 1:1 relationship
    notes: Mapped[List["TenantNote"]] = db.relationship("TenantNote")
    # created_date: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    # updated_date: datetime = db.Column(
    #     db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    # )


@dataclass
class TenantNote(BaseClass):
    """Tenant note Model for storing tenant notes"""

    __tablename__ = "tenantNote"
    # id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tenant_id: int = db.Column(db.Integer, db.ForeignKey(Tenant.id))
    # created_date: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    # updated_date: datetime = db.Column(
    #     db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    # )
    note: str = db.Column(db.String(2000))


@dataclass
class TenantProfile(BaseClass):
    """Tenant profile pic stored as base64 str"""

    __tablename__ = "tenant-profile"
    # id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tenant_id: int = db.Column(db.Integer, db.ForeignKey(Tenant.id))
    # created_date: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    # updated_date: datetime = db.Column(
    #     db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    # )
    image: LargeBinary = db.Column(LargeBinary)
    tenant = db.relationship("Tenant", back_populates="profile_pic")
