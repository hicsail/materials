from sqlalchemy import Table, Column, Integer, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()
mixture_components = Table('mixture_components', Base.metadata,
                           Column('mixture_id', Integer, ForeignKey('mixtures.id'), primary_key=True),
                           Column('component_id', Integer, ForeignKey('components.id'), primary_key=True))


class Component(Base):
    __tablename__ = 'components'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    formula = Column(Text, nullable=True)
    bond_length = Column(Float, nullable=True)
    bond_angle = Column(Float, nullable=True)
    energy = Column(Float, nullable=True)
    smiles = Column(Text, nullable=True)

    mixtures = relationship('Mixture', backref="_components", secondary=mixture_components, cascade='all, delete',
                            passive_deletes=True)

    def __repr__(self):
        return "<Component(id='%s', compound_name='%s', smiles='%s', bond_length='%s', bond_angle='%s', energy='%s')>" \
               % (self.id, self.compound_name, self.smiles, self.bond_length, self.bond_angle, self.energy)


class Mixture(Base):
    __tablename__ = 'mixtures'

    id = Column(Integer, primary_key=True)
    # Used to get all components for a mixture without having to loop through them
    # See http://docs.sqlalchemy.org/en/latest/orm/extensions/associationproxy.html
    components = association_proxy('_components', 'name')

    listings = relationship('Listing', backref='mixture', cascade='all, delete-orphan', passive_deletes=True)

    def __repr__(self):
        return "<Mixture(id='%s')>" % self.id


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
    """
    A listing is defined by a single reference. All listings have a collection of measurement groups, and each group
    contains multiple individual measurements. For example, a group could be consist of individual temperature,
    pressure and viscosity measurements. They all share the same measurement_group_id. A collection of groups shares
    the same listing_id.
    """
    __tablename__ = 'measurements'

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listings.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    property_id = Column(Integer, ForeignKey('properties.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    measurement_group_id = Column(Integer, nullable=False)
    value = Column(Float, nullable=False)
    error = Column(Integer, nullable=True)

    def __repr__(self):
        return "<Measurement(id='%s', value='%s', error='%s')>" % (self.id, self.value, self.error)


class Reference(Base):
    __tablename__ = 'references'

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=True)
    full = Column(Text, nullable=False)

    listings = relationship('Listing', backref='reference', cascade='all, delete-orphan', passive_deletes=True)

    def __repr__(self):
        return "<Reference(id='%s', title='%s', full='%s')>" % (self.id, self.title, self.full)


class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    unit = Column(Text, nullable=True)

    measurements = relationship('Measurement', backref='property', cascade='all, delete-orphan', passive_deletes=True)

    def __repr__(self):
        return "<Property(id='%s', name='%s', unit='%s')>" % (self.id, self.name, self.unit)
