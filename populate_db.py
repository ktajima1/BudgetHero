from backend.database import initialize_database, get_session
from backend.models.transaction import Transaction
from backend.models.user import User
from backend.services.user_service import UserService
from backend.services.transaction_service import TransactionService
from backend.services.category_service import CategoryService
from backend.services.conversion_service import ConversionService
from datetime import datetime, timedelta
import random
from typing import List

def generate_random_datetime(start: datetime, end: datetime) -> datetime:
    """Generate a random datetime between two datetime objects."""
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)

def generate_amount(min_amount: float, max_amount: float) -> float:
    """Generate a random amount within a range."""
    return round(random.uniform(min_amount, max_amount), 2)

def generate_transactions(gen_num: int, user: User, amount_range: tuple[float, float], type_str: str,
                          date_range: tuple[datetime, datetime], cat_range: tuple[int, int]) -> List[Transaction]:
    """Generate random transactions for a user."""
    transactions = []
    for _ in range(gen_num):
        amount = round(random.uniform(amount_range[0], amount_range[1]), 2) # Generate a random amount in the range
        category_id = random.randint(cat_range[0], cat_range[1]) # Generate a random int in the range
        date = generate_random_datetime(date_range[0], date_range[1])

        new_trans = transaction_service.create_transaction(
            user, amount, type_str, date, category_id, f"Random [{type_str.upper()}] transaction: {amount}"
        )
        transactions.append(new_trans)
    return transactions

if __name__ == "__main__":
    initialize_database()
    with get_session() as session:
        # Dates used to generate random dates
        start_date = datetime(2022, 12, 25, 14, 30, 0)  # Dec 25, 2020 at 2:30 PM
        end_date = datetime(2024, 12, 25, 14, 30, 0)  # Dec 25, 2024 at 2:30 PM
        date_range = (start_date, end_date)

        # Start services
        user_service = UserService(session)
        transaction_service = TransactionService(session)
        category_service = CategoryService(session)
        conversion_service = ConversionService(session)

        # Create five users
        user1 = user_service.register_user("user1", "11111P@ss")
        user2 = user_service.register_user("user2", "22222P@ss")
        user3 = user_service.register_user("user3", "33333P@ss")
        user4 = user_service.register_user("user5", "44444P@ss")
        user5 = user_service.register_user("user6", "55555P@ss")

        # Create three income categories
        in_cat1 = category_service.create_category("Work", "Money from work")
        in_cat2 = category_service.create_category("Side-Gig", "Money from doing sidequests")
        in_cat3 = category_service.create_category("Allowance", "Money from parents")
        # Create three expense categories
        ex_cat1 = category_service.create_category("Food", "Food bills")
        ex_cat2 = category_service.create_category("Utilities", "Paying utilities")
        ex_cat3 = category_service.create_category("Gaming", "Buying games")

        # Create ten income transactions and ten expense transactions for each user
        user1_income_list = generate_transactions(10, user1, (1,250), "INCOME", date_range, (1,3))
        user1_expense_list = generate_transactions(10, user1, (1, 250), "EXPENSE", date_range, (4, 6))
        user2_income_list = generate_transactions(10, user2, (1, 250), "INCOME", date_range, (1, 3))
        user2_expense_list = generate_transactions(10, user2, (1, 250), "EXPENSE", date_range, (4, 6))
        user3_income_list = generate_transactions(10, user3, (1, 250), "INCOME", date_range, (1, 3))
        user3_expense_list = generate_transactions(10, user3, (1, 250), "EXPENSE", date_range, (4, 6))
        user4_income_list = generate_transactions(10, user4, (1, 250), "INCOME", date_range, (1, 3))
        user4_expense_list = generate_transactions(10, user4, (1, 250), "EXPENSE", date_range, (4, 6))
        user5_income_list = generate_transactions(10, user5, (1, 250), "INCOME", date_range, (1, 3))
        user5_expense_list = generate_transactions(10, user5, (1, 250), "EXPENSE", date_range, (4, 6))
