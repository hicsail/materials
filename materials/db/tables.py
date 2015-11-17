from sqlalchemy import Table, Column, Integer, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
mixture_components = Table('mixture_components', Base.metadata,
                           Column('component_id', Integer, ForeignKey('components.id')),
                           Column('mixture_id', Integer, ForeignKey('mixtures.id')))


class Component(Base):
    __tablename__ = 'components'

    id = Column(Integer, primary_key=True)
    component_name = Column(Text, nullable=False)
    bond_length = Column(Float, nullable=True)
    bond_angle = Column(Float, nullable=True)
    energy = Column(Float, nullable=True)
    smiles = Column(Text, nullable=True)

    mixtures = relationship('Mixture', secondary=mixture_components, backref='components', cascade='all, delete-orphan',
                            passive_deletes=True)

    def __repr__(self):
        return "<Component(id='%s', compound_name='%s', smiles='%s', bond_length='%s', bond_angle='%s', energy='%s')>" \
               % (self.id, self.compound_name, self.smiles, self.bond_length, self.bond_angle, self.energy)


class Mixture(Base):
    __tablename__ = 'mixtures'

    id = Column(Integer, primary_key=True)

    listings = relationship('Listing', backref='mixture', cascade='all, delete-orphan', passive_deletes=True)

    def __repr__(self):
        return "<Mixture(id='%s', compound_name='%s')>" % (self.id, self.component_id)


class Listing(Base):
    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    mixture_id = Column(Integer, ForeignKey('mixtures.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    reference_id = Column(Integer, ForeignKey('references.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    url = Column(Text)

    measurements = relationship('Measurement', backref='listing', cascade='all, delete-orphan',
                                passive_deletes=True)

    def __repr__(self):
        return "<Listing(id='%s', url='%s')>" % (self.id, self.url)


class Measurement(Base):
    __tablename__ = 'measurements'

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listings.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    property_id = Column(Integer, ForeignKey('properties.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    value = Column(Float, nullable=False)
    error = Column(Integer, nullable=True)
    unit = Column(Text, nullable=True)

    def __repr__(self):
        return "<Measurement(id='%s', value='%s')>" % (self.id, self.value)


class Reference(Base):
    __tablename__ = 'references'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

    listings = relationship('Listings', backref='reference', cascade='all, delete-orphan', passive_deletes=True)

    def __repr__(self):
        return "<Reference(id='%s', name='%s')>" % (self.id, self.name)


class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

    measurements = relationship('Measurement', backref='property', cascade='all, delete-orphan', passive_deletes=True)

    def __repr__(self):
        return "<Property(id='%s', name='%s')>" % (self.id, self.name)
