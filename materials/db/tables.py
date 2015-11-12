from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Material(Base):
    __tablename__ = 'materials'

    id = Column(Integer, primary_key=True)
    compound_name = Column(Text, nullable=False)
    smiles = Column(Text, nullable=True)

    listings = relationship('Listing', backref='listings', cascade='all, delete-orphan', passive_deletes=True)

    def __repr__(self):
        return "<Material(id='%s', smiles='%s', compound_name='%s')>" % (self.id, self.smiles, self.compound_name)


class Listing(Base):
    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    material_id = Column(Integer, ForeignKey('materials.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    url = Column(Text)

    measurements = relationship('Measurement', backref='measurements', cascade='all, delete-orphan',
                                passive_deletes=True)
    references = relationship('Reference', backref='references', cascade='all, delete-orphan',
                              passive_deletes=True)

    def __repr__(self):
        return "<Listing(id='%s', url='%s')>" % (self.id, self.url)


class Measurement(Base):
    __tablename__ = 'measurements'

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listings.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    property_id = Column(Integer, ForeignKey('properties.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    value = Column(Integer, nullable=False)
    error = Column(Integer, nullable=True)
    unit = Column(Text, nullable=False)

    property = relationship('Property', cascade='all, delete-orphan', passive_deletes=True)

    def __repr__(self):
        return "<Reference(id='%s', value='%s')>" % (self.id, self.value)


class Reference(Base):
    __tablename__ = 'references'

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listings.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    name = Column(Text, nullable=False)

    def __repr__(self):
        return "<Reference(id='%s', name='%s')>" % (self.id, self.name)


class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

    def __repr__(self):
        return "<Unit(id='%s', name='%s')>" % (self.id, self.name)
