from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class Listing(Base):
    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    material_id = Column(Integer, ForeignKey('materials.id'))
    url = Column(Text)

    measurements = relationship('Measurement', backref=backref('measurements', order_by=id))
    references = relationship('Reference', backref=backref('references', order_by=id))

    def __repr__(self):
        return "<Listing(id='%s', url='%s')>" % (self.id, self.url)
