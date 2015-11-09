from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class Measurement(Base):
    __tablename__ = 'measurements'

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listings.id'))
    unit_id = Column(Integer, ForeignKey('units.id'))
    value = Column(Integer, nullable=False)

    unit = relationship("Unit")

    def __repr__(self):
        return "<Reference(id='%s', value='%s')>" % (self.id, self.value)
