from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text

Base = declarative_base()


class Material(Base):
    __tablename__ = 'materials'

    id = Column(Integer, primary_key=True)
    smiles = Column(Text, nullable=False)
    compound_name = Column(Text, nullable=False)

    def __repr__(self):
        return "<Material(id='%s', smiles='%s', compound_name='%s')>" % (self.id, self.smiles, self.compound_name)
