from sqlite3 import IntegrityError
from backend.repositories.transaction_repository import TransactionRepository
from backend.models.enums import IncomeOrExpense

class TransactionService:
    def __init__(self, session):
        self.repo = TransactionRepository(session)

    def create_transaction(self, user, amount, type, date, category_id, description):
        validation_errors = validate_transaction(amount, type, date, category_id, description)
        if validation_errors:
            print("trans_serv.create_trans: Transaction validation failed, see following errors:")
            for error in validation_errors:
                print(f"\t{validation_errors[error]}")
            return False # print some message to frontend
        try:
            # Change datatype of 'type' to enum from string
            trans_type = to_enum(type)
            if trans_type is None:
                print(f"trans_serv.create_trans: something went wrong, invalid transaction type: {type}")
                return False
            transaction = self.repo.create_transaction(user, amount, trans_type, date, category_id, description)
            print(f"trans_serv.create_trans: Created transaction successfully: {transaction.id}")
            return True
        except IntegrityError as e:
            print(f"trans_serv.create_trans: Transaction already exists: {e}")
            return False

        # find user
        # connect to transaction db using user id
        # create a transaction using amount, type (income or expense), category
        # if: description, add description.
        # create and commit transaction

    def delete_transaction(self, transaction):
        try:
            self.repo.delete_transaction(transaction)
            print("trans_serv.del_trans: Transaction successfully deleted.")
            return True
        except Exception as e:
            print(f"trans_serv.del_trans: Transaction could not be deleted: {e}")
            return False

    def modify_transaction(self, transaction, amount, type, date, category_id, description):
        # Check that transaction fields are valid
        validation_errors = validate_transaction(amount, type, date, category_id, description)
        if validation_errors:
            print("trans_serv.modify_trans: Transaction validation failed, see following errors:")
            for error in validation_errors:
                print(f"\t{validation_errors[error]}")
            return False
        try:
            self.repo.modify_transaction(transaction, amount, type, date, category_id, description)
            print("trans_serv.modify_trans: Transaction successfully updated.")
            return True
        except Exception as e:
            print(f"trans_serv.modify_trans: Transaction could not be modified: {e}")
            return False

    def get_transactions(self, user, filters):  # Change filters parameter to specific filters like amount and such once i figure out the specific implementation
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

    def get_all_transactions(self, user):
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
            return None

    def get_details(self, transaction):
        return (f"Transaction id: {transaction.id}, "
                f"User: {transaction.user_id}, "
                f"Amount: {transaction.amount}, "
                f"Type: {transaction.type}, "
                f"Date: {transaction.date}, "
                f"Category: {transaction.category_id}, "
                f"Description: {transaction.description}")

# Helper methods

def validate_transaction(amount, type, date, category_id, description):
    errors = {}
    # Cannot have negative value for amount
    if amount < 0:
        errors['amount'] = "Amount cannot be negative."
    # Type must be either INCOME or EXPENSE
    if type.lower() not in ['income', 'expense']:
        errors['type'] = "Unknown type: " + type.upper()
    #     Add more validation checks if necessary
    return errors if errors else None

def to_enum(type):
    trans_type = None
    if type.lower() == "income":
        trans_type = IncomeOrExpense.INCOME
    if type.lower() == "expense":
        trans_type = IncomeOrExpense.EXPENSE
    return trans_type