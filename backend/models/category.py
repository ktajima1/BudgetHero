from backend.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Category(Base):
    """
        This is the database class for the category table.
    """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True) # Unique identifier for each category
    category_name = Column(String, unique=True, nullable=False) # Names should be unique and case-insensitive
    description = Column(String, nullable=True) # Optional description for the category

    transactions = relationship("Transaction", back_populates="category") # Each transaction has a category