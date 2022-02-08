from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from db.database import Base
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean, BigInteger
from models.group import Group


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
