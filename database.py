# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Create the SQLite database with check_same_thread=False
engine = create_engine('sqlite:///frisbee_elo.db', echo=False, connect_args={'check_same_thread': False})

# Create a configured "Session" class using scoped_session
Session = scoped_session(sessionmaker(bind=engine))

# Base class for declarative class definitions
Base = declarative_base()
