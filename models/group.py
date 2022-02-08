from sqlalchemy import Column
from sqlalchemy.sql import func
from db.database import Base
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, Enum, DateTime
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
