import sqlite3
from datetime import datetime
from typing import List, Dict, Any

from sqlalchemy.exc import IntegrityError

from backend.models.transaction import Transaction
from backend.models.user import User
from backend.repositories.transaction_repository import TransactionRepository
from backend.models.enums import IncomeOrExpense
from backend.utils.error_utils import handle_errors

class TransactionService:
    def __init__(self, session):
        self.repo = TransactionRepository(session)

    def create_transaction(self, user: User, amount: float, type: str, date: datetime, category_id: int, description: str) -> Transaction | None:
        validation_errors = validate_transaction(user, amount, type, date, category_id, description)
        if validation_errors:
            handle_errors(validation_errors, "trans_serv.create_trans")
            return None
        try:
            # Change datatype of 'type' to enum from string
            trans_type = to_enum(type)
            if trans_type is None:
                print(f"trans_serv.create_trans: something went wrong, invalid transaction type: {type}")
                return None
            new_transaction = self.repo.create_transaction(user, amount, trans_type, date, category_id, description)
            self.repo.commit() # Commit changes
            print(f"trans_serv.create_trans: Created transaction successfully: {new_transaction.id}")
            return new_transaction
        except (IntegrityError, sqlite3.IntegrityError) as e:
            print(f"trans_serv.create_trans: Transaction already exists: {e}")
            self.repo.rollback() # Rollback changes to refresh session
            return None
        except Exception as e:
            print(f"trans_serv.create_trans: Unknown error: {e}")
            return None

        # find user
        # connect to transaction db using user id
        # create a transaction using amount, type (income or expense), category
        # if: description, add description.
        # create and commit transaction

    def delete_transaction(self, transaction: Transaction) -> bool:
        try:
            self.repo.delete_transaction(transaction)
            self.repo.commit()  # Commit changes
            print("trans_serv.del_trans: Transaction successfully deleted.")
            return True
        except Exception as e:
            print(f"trans_serv.del_trans: Transaction could not be deleted: {e}")
            return False

    def modify_transaction(self, transaction: Transaction, amount: float, type: IncomeOrExpense, date: datetime, category_id: int, description: str) -> bool:
        # Check that transaction fields are valid
        validation_errors = validate_transaction(amount, type, date, category_id, description)
        if validation_errors:
            handle_errors(validation_errors, "trans_serv.modify_trans")
            return False
        try:
            self.repo.modify_transaction(transaction, amount, type, date, category_id, description)
            self.repo.commit()  # Commit changes
            print("trans_serv.modify_trans: Transaction successfully updated.")
            return True
        except Exception as e:
            print(f"trans_serv.modify_trans: Transaction could not be modified: {e}")
            return False

    def get_transactions(self, user: User, filters: Dict[str, Any]) -> List[Transaction]:  # Change filters parameter to specific filters like amount and such once i figure out the specific implementation
        try:
            transactions_list = self.repo.get_transactions(user, filters)
            if transactions_list:
                print("trans_serv.get_trans: Filtered transactions acquired")
                return transactions_list
            else:
                print("trans_serv.get_trans: No matching transactions acquired")
                return []
        except Exception as e:
            print(f"trans_serv.get_trans: something went wrong: {e}")
            return []

    def get_all_transactions(self, user: User) -> List[Transaction]:
        #  just return all transactions
        try:
            transactions_list = self.repo.get_all_transactions(user)
            if transactions_list:
                print("trans_serv.get_all_trans: All transactions acquired")
                return transactions_list
            else:
                print("trans_serv.get_all_trans: No matching transactions acquired")
                return []
        except Exception as e:
            print(f"trans_serv.get_all_trans: Transaction could not be found: {e}")
            return []

    def get_details(self, transaction: Transaction):
        return (f"Transaction id: {transaction.id}, "
                f"User: {transaction.user_id}, "
                f"Amount: {transaction.amount}, "
                f"Type: {transaction.type}, "
                f"Date: {transaction.date}, "
                f"Category: {transaction.category_id}, "
                f"Description: {transaction.description}")

# Helper methods

def validate_transaction(user: User, amount: float, type: str, date: datetime, category_id: int, description: str) -> Dict[str, str]:
    errors = {}
    if user is None:
        errors["user"] = f"User is invalid"
    # Cannot have negative value for amount
    if amount < 0:
        errors['amount'] = "Amount cannot be negative."
    # Type must be either INCOME or EXPENSE
    if type.lower() not in ['income', 'expense']:
        errors['type'] = "Unknown type: " + type.upper()
    #     Add more validation checks if necessary
    return errors if errors else None

def to_enum(type: str) -> IncomeOrExpense | None:
    trans_type = None
    if type.lower() == "income":
        trans_type = IncomeOrExpense.INCOME
    if type.lower() == "expense":
        trans_type = IncomeOrExpense.EXPENSE
    return trans_type