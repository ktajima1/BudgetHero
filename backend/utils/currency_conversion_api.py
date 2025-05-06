import requests
from config import CURRENCY_API_KEY  # API Key should be put in config file
from datetime import datetime


def get_rate_from_API(base_currency: str, target_currency: str, date: datetime) -> float | None:
    """Fetch historical conversion rate for a given date (YYYY-MM-DD)."""

    # Convert datetime to proper string format to fetch from API
    date_str = date.strftime("%Y-%m-%d")

    url = f"https://api.currencyapi.com/v3/historical"
    params = {
        "apikey": CURRENCY_API_KEY,
        "date": date_str,
        "base_currency": base_currency,
        "currencies": target_currency,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        return data['data'][target_currency]['value']
    except Exception as e:
        print(f"[currency_utils.get_conversion_rate] Error fetching rate: {e}")
        return None