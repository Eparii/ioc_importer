from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from utils import get_connection_string


# SQLAlchemy engine
connection_string = get_connection_string('../config.json')
engine = create_engine(connection_string)

# A base class for declarative models
Base = declarative_base()


# Models for the database tables
class Source(Base):
    __tablename__ = 'source_t'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))

    ip_addresses = relationship('IP', backref='source', cascade='all, delete-orphan')
    urls = relationship('URL', backref='source', cascade='all, delete-orphan')


class IP(Base):
    __tablename__ = 'ip_t'
    id = Column(Integer, primary_key=True)
    ip_address = Column(String)

    id_source = Column(Integer, ForeignKey('source_t.id', ondelete='CASCADE'))


class URL(Base):
    __tablename__ = 'url_t'
    id = Column(Integer, primary_key=True)
    url = Column(Text)

    id_source = Column(Integer, ForeignKey('source_t.id', ondelete='CASCADE'))


# Ensures creation of the tables in the database
Base.metadata.create_all(engine)
