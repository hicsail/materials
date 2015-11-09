from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text

Base = declarative_base()


class Unit(Base):
    __tablename__ = 'units'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

    def __repr__(self):
        return "<Unit(id='%s', name='%s')>" % (self.id, self.name)
