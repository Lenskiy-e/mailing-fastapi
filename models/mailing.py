from sqlalchemy import Column, ForeignKey
from db.database import Base
from sqlalchemy.sql.sqltypes import Integer, String, Text, DateTime, Enum, Float
from models.group import Group
from sqlalchemy.sql import func
from enum import Enum as enum_type
from exceptions.mailing import InvalidStatusToChange


class MailingStatus(str, enum_type):
    finished = 'finished'
    new = 'new'
    pending = 'pending'
    rejected = 'rejected'
    waiting = 'waiting'
    ready_to_send = 'ready to send'

    def get_changeable_statuses(self) -> []:
        return [self.new, self.ready_to_send]


class Mailing(Base):
    __tablename__ = 'mailing'
    id = Column(Integer, primary_key=True)
    affiliate_id = Column(Integer, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    alpha_name = Column(String(255), nullable=False)
    group_id = Column(Integer, ForeignKey(Group.id, ondelete='RESTRICT'), nullable=False)
    message = Column(Text, nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    status = Column(Enum(MailingStatus))
    parts_count = Column(Integer, nullable=False)
    cost = Column(Float)
    roi = Column(Float)
    payout_id = Column(Integer)
    cdate = Column(DateTime(timezone=True), server_default=func.now())
    mdate = Column(DateTime(timezone=True), onupdate=func.now())

    def change_status(self, status: MailingStatus) -> None:
        if status not in MailingStatus.get_changeable_statuses:
            raise InvalidStatusToChange(status)

        self.status = status
