from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URI
from contextlib import contextmanager

# Create base, engine and session
Base = declarative_base()

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

def get_base():
    return Base

def get_engine():
    return engine

@contextmanager
def get_session():
    # generator to create a session
    session = Session()
    try:
        yield session
    finally:
        session.close()


def initialize_database():
    Base.metadata.create_all(bind=engine)