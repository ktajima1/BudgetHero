from backend.database import Base
from sqlalchemy import Column, Integer, String

class ConversionRate(Base):
    __tablename__ = "exchange_rates"

    id = Column(Integer, primary_key=True, autoincrement=True)