from backend.database import Base
from sqlalchemy import Column, String, Float, Date

class ConversionRate(Base):
    """
        This is the database class for the category table.
    """

    __tablename__ = "conversion_rates"

    base_currency = Column(String, primary_key=True) # The base currency to be converted from
    target_currency = Column(String, primary_key=True) # The target currency to be converted to
    date = Column(Date, primary_key=True) # The date for the conversion rate
    rate = Column(Float, nullable=False) # The rate