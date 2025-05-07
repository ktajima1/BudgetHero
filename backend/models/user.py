from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from backend.database import Base

class User(Base):
    """
        This is the database for the users table
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True) # Unique user id
    username = Column(String(50), unique=True) # unique username
    password_hash = Column(String(128)) # the password hash
    account_balance = Column(Float, nullable=False) # user's account balance for financial tracking

    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan") # users own multiple transactions

