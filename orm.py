"""
Contains MySQL ORM

"""

import datetime
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer

Base = declarative_base()

class LaundryViewDataTable(Base):
    __tablename__ = 'laundry_view_data'

    id = Column('id', Integer, primary_key=True)
    room = Column('room', Integer)
    timestamp = Column('timestamp', DateTime, default=datetime.datetime.utcnow)
    washers_available = Column('washers_available', TINYINT)
    dryers_available = Column('dryers_available', TINYINT)

    def __init__(self, room, washers_available, dryers_available):
            self.room = room
            self.washers_available = washers_available
            self.dryers_available = dryers_available

    def __repr__(self):
            return '<LaundryViewDataTable(%d)>' % self.room
