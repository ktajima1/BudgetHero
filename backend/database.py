from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URI

# Create engine and session factory
Base = declarative_base()

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

def get_session():
    # generator to create a session
    session = Session()
    try:
        yield session
    finally:
        session.close()