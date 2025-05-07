from backend.models.conversion_rate import ConversionRate
from datetime import datetime

class ConversionRepository():
    def __init__(self, session):
        self.session = session

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()

    def log_rate(self, base_currency: str, target_currency: str, date: datetime.date, rate: float) -> ConversionRate:
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
        self.session.delete(conv_rate)
        print(f"[curr_repo.delete_rate]: deleted [{conv_rate.base_currency} : {conv_rate.target_currency} : {conv_rate.date}] in DB")

    def change_rate(self, conv_rate: ConversionRate, new_rate: float):
        old_rate = conv_rate.rate
        conv_rate.rate = new_rate
        print(f"[curr_repo.delete_rate]: changed rate for [{conv_rate.base_currency} : {conv_rate.target_currency}] from '{old_rate}' to '{new_rate}'")

    def get_rate(self, base_currency: str, target_currency: str, date: datetime.date) -> ConversionRate | None:
        return self.session.query(ConversionRate).filter(ConversionRate.base_currency == base_currency,
                                                         ConversionRate.target_currency == target_currency,
                                                         ConversionRate.date == date
                                                         ).first()
