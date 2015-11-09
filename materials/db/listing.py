from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, ForeignKey

Base = declarative_base()


class Listing(Base):
    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    material_id = Column(Integer, ForeignKey('materials.id'))
    url = Column(Text)

    def __repr__(self):
        return "<Listing(id='%s', url='%s')>" % (self.id, self.url)
