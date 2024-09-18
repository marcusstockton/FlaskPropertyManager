"""Tenant Entity"""

from dataclasses import dataclass
import enum
from datetime import datetime
from typing import Optional
from sqlalchemy import LargeBinary
from sqlalchemy.orm import Mapped
from sqlalchemy_utils import EmailType
from app.main.model.base import BaseClass


from .property import Property
from .. import db


class TitleEnum(enum.Enum):
    """Title Enum"""

    MR = 1, "Mr"
    MRS = 2, "Mrs"
    MISS = 3, "Miss"
    MS = 4, "Ms"
    LORD = 5, "Lord"
    SIR = 6, "Sir"
    DR = 7, "Dr"
    LADY = 8, "Lady"
    DAME = 9, "Dame"
    PROFESSOR = 10, "Professor"
    MX = 11, "Mx"

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
    property_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey(Property.id))
    property = db.relationship("Property", back_populates="tenants")
    phone_number: Mapped[str] = db.Column(db.String(20))
    email_address: Mapped[str] = db.Column(EmailType)
    title: TitleEnum = db.Column(db.Enum(TitleEnum))
    first_name: Mapped[str] = db.Column(db.String(100))
    last_name: Mapped[str] = db.Column(db.String(100))
    date_of_birth: Mapped[datetime] = db.Column(db.Date, nullable=True)
    job_title: Mapped[str] = db.Column(db.String(100))
    tenancy_start_date: Mapped[datetime] = db.Column(db.Date, nullable=False)
    tenancy_end_date: Mapped[Optional[datetime]] = db.Column(db.Date, nullable=True)
    smoker: Mapped[bool] = db.Column(db.Boolean, nullable=False, default=False)
    profile_pic = db.relationship(
        "TenantProfile", back_populates="tenant", uselist=False
    )  # uselist demotes a 1:1 relationship
    notes = db.relationship("TenantNote")
    documents = db.relationship("TenantDocument")


@dataclass
class TenantNote(BaseClass):
    """Tenant note Model for storing tenant notes"""

    __tablename__ = "tenantNote"
    tenant_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey(Tenant.id))
    note: Mapped[str] = db.Column(db.String(2000))


@dataclass
class TenantProfile(BaseClass):
    """Tenant profile pic stored as base64 str"""

    __tablename__ = "tenant-profile"
    tenant_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey(Tenant.id))
    image: Mapped[LargeBinary] = db.Column(LargeBinary)
    tenant = db.relationship("Tenant", back_populates="profile_pic")


@dataclass
class DocumentType(BaseClass):
    """Document Type"""

    __tablename__ = "document-type"
    description: Mapped[str] = db.Column(db.String(100))
    expiry: Mapped[Optional[datetime]] = db.Column(db.Date)
    document = db.relationship("TenantDocument", back_populates="document_type")


@dataclass
class TenantDocument(BaseClass):
    """Tenant Documents stored as base64 str"""

    __tablename__ = "tenant-document"
    tenant_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey(Tenant.id))
    tenant = db.relationship("Tenant", back_populates="documents")
    document_blob: Mapped[LargeBinary] = db.Column(LargeBinary)
    file_name: Mapped[str] = db.Column(db.String(100))
    file_ext: Mapped[set] = db.Column(db.String(4))
    document_type_id: Mapped[int] = db.Column(
        db.Integer, db.ForeignKey(DocumentType.id)
    )
    document_type = db.relationship("DocumentType")
