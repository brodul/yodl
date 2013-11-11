from sqlalchemy import (
    Column,
    Integer,
    Text,
    Unicode,
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class SongItem(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    songname = Column(Unicode, unique=True)
    youtube_id = Column(Text, unique=True)
