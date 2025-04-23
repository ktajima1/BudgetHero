from backend.database import engine, Base
from backend.models import user

def initialize_database():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    initialize_database()
    print("Database tables created")