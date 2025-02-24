"""Tenant Entity"""

from dataclasses import dataclass
import enum
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, Date, Enum, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
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
    def has_key(cls, name) -> bool:
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
    property_id: Mapped[int] = mapped_column(Integer, ForeignKey(Property.id))
    property = db.relationship("Property", back_populates="tenants")
    phone_number: Mapped[str] = mapped_column(String(20))
    email_address: Mapped[str] = mapped_column(EmailType)
    title: Mapped[TitleEnum] = mapped_column(Enum(TitleEnum))
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    date_of_birth: Mapped[datetime] = mapped_column(Date, nullable=True)
    job_title: Mapped[str] = mapped_column(String(100))
    tenancy_start_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    tenancy_end_date: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True)
    smoker: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    profile_pic: Mapped["TenantProfile"] = relationship(
        "TenantProfile", back_populates="tenant", uselist=False
    )  # uselist demotes a 1:1 relationship
    notes: Mapped[List["TenantNote"]] = relationship("TenantNote")
    documents: Mapped[List["TenantDocument"]] = relationship("TenantDocument")


@dataclass
class TenantNote(BaseClass):
    """Tenant note Model for storing tenant notes"""

    __tablename__ = "tenantNote"
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey(Tenant.id))
    note: Mapped[str] = mapped_column(String(2000))


@dataclass
class TenantProfile(BaseClass):
    """Tenant profile pic stored as base64 str"""

    __tablename__ = "tenant-profile"
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey(Tenant.id))
    image: Mapped[LargeBinary] = mapped_column(LargeBinary)
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="profile_pic")


@dataclass
class DocumentType(BaseClass):
    """Document Type"""

    __tablename__ = "document-type"
    description: Mapped[str] = mapped_column(String(100))
    expiry: Mapped[Optional[datetime]] = mapped_column(Date)
    document: Mapped["TenantDocument"] = relationship(
        "TenantDocument", back_populates="document_type"
    )


@dataclass
class TenantDocument(BaseClass):
    """Tenant Documents stored as base64 str"""

    __tablename__ = "tenant-document"
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey(Tenant.id))
    tenant = relationship("Tenant", back_populates="documents")
    document_blob: Mapped[LargeBinary] = mapped_column(LargeBinary)
    file_name: Mapped[str] = mapped_column(String(100))
    file_ext: Mapped[set] = mapped_column(String(4))
    document_type_id: Mapped[int] = mapped_column(Integer, ForeignKey(DocumentType.id))
    document_type: Mapped["DocumentType"] = relationship("DocumentType")
