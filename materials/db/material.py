from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

Base = declarative_base()


class Material(Base):
    __tablename__ = 'materials'

    id = Column(Integer, primary_key=True)
    smiles = Column(Text, nullable=False)
    compound_name = Column(Text, nullable=False)

    listings = relationship('Listing', backref='listings', cascade='all, delete-orphan', passive_deletes=True)

    def __repr__(self):
        return "<Material(id='%s', smiles='%s', compound_name='%s')>" % (self.id, self.smiles, self.compound_name)
