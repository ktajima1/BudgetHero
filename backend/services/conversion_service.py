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
    """
    Conversion service used to handle business logic for converting currencies
    """
    def __init__(self, session):
        self.repo = ConversionRepository(session)

    def get_rate(self, base_currency: str, target_currency: str, date: datetime.date) -> ConversionRate | None:
        """
        Gets the rate for a given base currency and target currency by a date.
        Args:
            base_currency: The base currency.
            target_currency: The target currency.
            date: The date to get the rate for.
        Returns:
            ConversionRate: the conversion rate
            None: If conversion rate could not be found
        """
        try:
            # First search the conversion_rate database to see if rate already exists. If not, fetch rate from API
            conv_rate = self.repo.get_rate(base_currency, target_currency, date)
            if conv_rate is not None:
                print(f"[conv_serv.get_rate]: Target rate acquired from DB")
                return conv_rate
            else: # Fallback to API
                print(f"[conv_serv.get_rate]: Rate does not exist in DB, fetching from API")
                requested_rate = get_rate_from_API(base_currency, target_currency, date)
                if requested_rate is not None:
                    print(f"\t[conv_serv.get_rate]: Rate received from API, logging into DB")
                    new_conv_rate = self.log_rate(base_currency, target_currency, date, requested_rate)
                    return new_conv_rate
                return None
        except (IntegrityError, sqlite3.IntegrityError) as e:
            print(f"[conv_serv.get_rate]: Rate creation from API failed due to IntegrityError: {e}")
            self.repo.rollback()  # Rollback changes to refresh session
            return None
        except Exception as e:
            print(f"[conv_serv.get_rate]: something went wrong: {e}")
            return None

    def log_rate(self, base_currency: str, target_currency: str, date: datetime, rate: float) -> ConversionRate | Dict[str,str] | None:
        """
        Logs a new rate for a given base currency and target currency and date. Checks that currency types are of the 147 currencies supported by the app before creating.
        Args:
            base_currency: The base currency.
            target_currency: The target currency.
            date: The date to get the rate for.
            rate: The new rate.
        returns:
            ConversionRate: the conversion rate
            None: If conversion rate could not be found
            Dict[str,str]: If conversion rate has validation errors
        """
        validation_errors = validate_rate(base_currency, target_currency, date, rate)
        if validation_errors:
            handle_errors(validation_errors, "conv_serv.log_rate")
            return validation_errors
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
        """
        Deletes rate given a conversion rate.
        Args:
            conv_rate: The conversion rate instance
        Returns:
            True: If the rate was deleted.
            False: If the rate was not deleted.
        """
        try:
            print(f"[conv_serv.del_conv]: Running deletion of rate [{conv_rate.base_currency}:{conv_rate.target_currency}]")
            self.repo.delete_rate(conv_rate)
            self.repo.commit()
            return True
        except Exception as e:
            print(f"[conv_serv.del_conv]: Rate could not be deleted: {e}")
            return False

    def change_rate(self, conv_rate: ConversionRate, new_rate: float) -> bool:
        """
        Changes rate given a conversion rate instance and new rate.
        Args:
            conv_rate: The conversion rate instance
            new_rate: The new rate.
        Returns:
            True: If the rate was changed.
            False: If the rate was not changed.
        """
        try:
            print(f"[conv_serv.change_conv]: Changing rate for [{conv_rate.base_currency}:{conv_rate.target_currency}]")
            self.repo.change_rate(conv_rate, new_rate)
            self.repo.commit()
            return True
        except Exception as e:
            print(f"[conv_serv.change_conv]: Rate could not be changed: {e}")
            return False

    def get_details(self, conv_rate: ConversionRate) -> str:
        """
        Gets details of a given conversion rate.
        Args:
            conv_rate: The conversion rate instance
        Returns:
            str: Details of a given conversion rate
        """
        return(f"Base Currency: {conv_rate.base_currency} "
              f"Target Currency: {conv_rate.target_currency} "
              f"Date: {conv_rate.date} "
              f"Rate: {conv_rate.rate} ")

def validate_rate(base_currency: str, target_currency: str, date: datetime, rate: float) -> Dict[str, str]:
    """
    Checks whether a given base currency and target currency are a valid currency type supported by the app. Checks that rate is greater than 0
    Args:
        base_currency: The base currency.
        target_currency: The target currency.
        date: The date to get the rate for.
        rate: The new rate.
    Returns:
        Dict[str, str]: If the rate is valid.
        {}: If no errors were found.
    """
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