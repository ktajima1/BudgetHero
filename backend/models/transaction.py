import enum

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from backend.database import Base

class IncomeOrExpense(enum.Enum):
    INCOME = "Income"
    EXPENSE = "Expense"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False) # Form relationship with a User
    amount = Column(Float, nullable=False)
    type = Column(Enum(IncomeOrExpense), nullable=False) # Either Income or Expense
    date = Column(DateTime, nullable=False)
    category = Column(Integer, nullable=False) # Category for income, using category Id from Category
    description = Column(String, nullable=True) # Optional description for transaction

    # relationship() w/ user table
