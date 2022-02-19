from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.database import Base
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, Enum, DateTime, BigInteger
from enum import Enum as enum_type


class GroupStatus(str, enum_type):
    active = 'active'
    deleted = 'deleted'


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    affiliate_id = Column(Integer, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    is_named = Column(Boolean, default=False)
    is_funnel = Column(Boolean, default=False)
    status = Column(Enum(GroupStatus), default=GroupStatus.active)
    cdate = Column(DateTime(timezone=True), server_default=func.now())
    mdate = Column(DateTime(timezone=True), onupdate=func.now())
    phones = relationship("Phone")

    def has_affiliate(self, affiliate_id: int) -> bool:
        return self.affiliate_id == affiliate_id


class Phone(Base):
    __tablename__ = 'phones'
    __table_args__ = (UniqueConstraint('group_id', 'phone'),)
    id = Column(Integer, primary_key=True)
    group_id = Column(ForeignKey(Group.id, ondelete='CASCADE'), nullable=False, index=True)
    phone = Column(BigInteger, nullable=False)
    name = Column(String(30))
    deleted = Column(Boolean, default=False)
    cdate = Column(DateTime(timezone=True), server_default=func.now())
    mdate = Column(DateTime(timezone=True), onupdate=func.now())