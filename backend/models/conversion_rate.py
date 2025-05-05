from backend.database import Base
from sqlalchemy import Column, String, DateTime, Float

class ConversionRate(Base):
    __tablename__ = "conversion_rates"

    base_currency = Column(String, primary_key=True)
    target_currency = Column(String, primary_key=True)
    date = Column(DateTime, primary_key=True)
    rate = Column(Float, nullable=False)