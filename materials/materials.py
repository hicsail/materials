import sqlalchemy
from config import config
from sqlalchemy import engine_from_config
from db import Base, Listing, Property, Measurement, Reference, Component, Mixture


def init():
    print sqlalchemy.__version__
    engine = engine_from_config(config, prefix='sqlalchemy.')
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    init()
