from backend.database import Base
from backend.utils.enums import IncomeOrExpense
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False) # Form relationship with a User
    amount = Column(Float, nullable=False)
    type = Column(Enum(IncomeOrExpense), nullable=False) # Either Income or Expense
    date = Column(DateTime, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False) # Category for income, using category Id from Category
    description = Column(String, nullable=True) # Optional description for transaction

    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")

