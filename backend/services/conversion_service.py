from backend.models.conversion_rate import ConversionRate
from backend.repositories.conversion_repository import ConversionRepository
from backend.utils.error_utils import handle_errors
from backend.utils.supported_currencies import SUPPORTED_CURRENCIES
from backend.utils.currency_conversion_api import get_rate_from_API
import sqlite3
from sqlalchemy.exc import IntegrityError
from typing import Dict
from datetime import datetime

class ConversionService:
    def __init__(self, session):
        self.repo = ConversionRepository(session)

    def get_rate(self, base_currency: str, target_currency: str, date: datetime) -> ConversionRate | None:
        try:
            # First search the conversion_rate database to see if rate already exists. If not, fetch rate from API
            conv_rate = self.repo.get_rate(base_currency, target_currency, date)
            if conv_rate is not None:
                print(f"[conv_serv.get_rate]: Target rate acquired from DB")
                return conv_rate
            else: # Fallback to API
                print(f"[conv_serv.get_rate]: Rate does not exist in DB, fetching from API")
                get_rate_from_API(base_currency, target_currency, date)
                return None
        except Exception as e:
            print(f"[conv_serv.get_rate]: something went wrong: {e}")
            return None

    def log_rate(self, base_currency: str, target_currency: str, date: datetime, rate: float) -> ConversionRate | None:
        validation_errors = validate_rate(base_currency, target_currency, date, rate)
        if validation_errors:
            handle_errors(validation_errors, "conv_serv.log_rate")
            return None
        try:
            print(f"[conv_serv.log_rate]: Creating rate for [{base_currency} : {target_currency} : {date}]")
            new_rate = self.repo.log_rate(base_currency, target_currency, date, rate)
            self.repo.commit()  # Commit the changes
            return new_rate
        except (IntegrityError, sqlite3.IntegrityError) as e:
            print(f"[conv_serv.log_rat]: Rate creation failed due to IntegrityError: {e}")
            self.repo.rollback()  # Rollback changes to refresh session
            return None
        except Exception as e:
            print(f"[conv_serv.log_rat]: Unknown error: {e}")
            return None

    def delete_rate(self, conv_rate: ConversionRate) -> bool:
        try:
            print(f"[conv_serv.del_conv]: Running deletion of rate [{conv_rate.base_currency}:{conv_rate.target_currency}]")
            self.repo.delete_rate(conv_rate)
            self.repo.commit()
            return True
        except Exception as e:
            print(f"[conv_serv.del_conv]: Rate could not be deleted: {e}")
            return False

    def change_rate(self, conv_rate: ConversionRate, new_rate: float) -> bool:
        try:
            print(f"[conv_serv.change_conv]: Changing rate for [{conv_rate.base_currency}:{conv_rate.target_currency}]")
            self.repo.change_rate(conv_rate, new_rate)
            self.repo.commit()
            return True
        except Exception as e:
            print(f"[conv_serv.change_conv]: Rate could not be changed: {e}")
            return False

    def get_details(self, conv_rate: ConversionRate) -> str:
        return(f"Base Currency: {conv_rate.base_currency} "
              f"Target Currency: {conv_rate.target_currency} "
              f"Date: {conv_rate.date} "
              f"Rate: {conv_rate.rate} ")

def validate_rate(base_currency: str, target_currency: str, date: datetime, rate: float) -> Dict[str, str]:
    errors = {}
    # Category name cannot be empty
    if base_currency not in SUPPORTED_CURRENCIES:
        errors["base_currency"] = f"Base currency {base_currency} is not supported"
    if target_currency not in SUPPORTED_CURRENCIES:
        errors["target_currency"] = f"Target currency {target_currency} is not supported"
    if rate <= 0:
        errors["rate"] = f"Rate must be greater than 0"
    # Add further validation checks here
    return errors