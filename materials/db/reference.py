from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, ForeignKey

Base = declarative_base()


class Reference(Base):
    __tablename__ = 'references'

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listings.id'))
    name = Column(Text, nullable=False)

    def __repr__(self):
        return "<Reference(id='%s', name='%s')>" % (self.id, self.name)
