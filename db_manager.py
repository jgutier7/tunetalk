from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///users.db", echo=True)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

from sqlalchemy import Column, Integer, String

def init_db(): # 15 LOC
    # import your classes that represent tables in the DB and then create_all of the tables
    from talk_classes import Song, User 
    Base.metadata.create_all(bind=engine) # use bind 

init_db()
