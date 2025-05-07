from backend.models.conversion_rate import ConversionRate
from datetime import datetime

class ConversionRepository():
    """
     This is the repository for currency conversions, used to insert, delete, modify, and retrieve data from the Conversion_Rate model.
     """
    def __init__(self, session):
        self.session = session

    def rollback(self):
        """
        Rollback the current session.
        """
        self.session.rollback()

    def commit(self):
        """
        Commit changes to the database.
        """
        self.session.commit()

    def log_rate(self, base_currency: str, target_currency: str, date: datetime.date, rate: float) -> ConversionRate:
        """
        Logs a new conversion rate to the database using the given base currency, target currency, and rate obtained from a third-party API using the given date.

        Args:
            base_currency (String): The base currency of the conversion.
            target_currency (String): The target currency of the conversion.
            date (Date): The date of the conversion.
            rate (Float): The new conversion rate.

        Returns:
            ConversionRate: The new conversion rate.
        """
        new_conv_rate = ConversionRate(
            base_currency=base_currency,
            target_currency=target_currency,
            date=date,
            rate=rate
        )
        self.session.add(new_conv_rate)
        print(f"[curr_repo.log_rate]: logged [{base_currency} : {target_currency} : {date}] in DB")
        return new_conv_rate

    def delete_rate(self, conv_rate: ConversionRate):
        """
        Deletes a conversion rate from the database.

        Args:
            conv_rate (ConversionRate): The conversion rate to delete.
        """
        self.session.delete(conv_rate)
        print(f"[curr_repo.delete_rate]: deleted [{conv_rate.base_currency} : {conv_rate.target_currency} : {conv_rate.date}] in DB")

    def change_rate(self, conv_rate: ConversionRate, new_rate: float):
        """
        Changes a conversion rate in the database.

        Args:
            conv_rate (ConversionRate): The conversion rate to change.
            new_rate (Float): The new conversion rate.
        """
        old_rate = conv_rate.rate
        conv_rate.rate = new_rate
        print(f"[curr_repo.delete_rate]: changed rate for [{conv_rate.base_currency} : {conv_rate.target_currency}] from '{old_rate}' to '{new_rate}'")

    def get_rate(self, base_currency: str, target_currency: str, date: datetime.date) -> ConversionRate | None:
        """
        Gets a conversion rate from the database.

        Args:
            base_currency (String): The base currency of the conversion.
            target_currency (String): The target currency of the conversion.
            date (Date): The date of the conversion.

        Returns:
            ConversionRate: The conversion rate.
            None: If the conversion rate is not found.
        """
        return self.session.query(ConversionRate).filter(ConversionRate.base_currency == base_currency,
                                                         ConversionRate.target_currency == target_currency,
                                                         ConversionRate.date == date
                                                         ).first()
