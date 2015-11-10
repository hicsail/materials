from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Listing(Base):
    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    material_id = Column(Integer, ForeignKey('materials.id', ondelete='CASCADE', onupdate='CASCADE'))
    url = Column(Text)

    measurements = relationship('Measurement', backref='measurements', cascade='all, delete-orphan',
                                passive_deletes=True)
    references = relationship('Reference', backref='references', cascade='all, delete-orphan',
                              passive_deletes=True)

    def __repr__(self):
        return "<Listing(id='%s', url='%s')>" % (self.id, self.url)
