from sqlite3 import IntegrityError
from backend.repositories.transaction_repository import TransactionRepository

# class Transaction:
#     def __init__(self, transaction_id, user_id, transaction_type, amount, date):
#         self.transaction_id = transaction_id
#         self.user_id = user_id
#         self.transaction_type = transaction_type
#         self.amount = amount
#         self.date = date

def validate_transaction(amount, type, date, category, description):
    errors = {}
    if amount < 0:
        errors['amount'] = "Amount cannot be negative."
    if type not in ['Income', 'Expense']: # might need to be capitalized
        errors['type'] = "Type must be either 'Income' or 'Expense'."
    #     Add more validation checks if necessary
    return errors if errors else None

class TransactionService:
    def __init__(self, session):
        self.repo = TransactionRepository(session)

    def create_transaction(self, user, amount, type, date, category, description):
        validation_errors = validate_transaction(amount, type, date, category, description)
        if validation_errors:
            print("Transaction validation failed, observe following errors:")
            for error in validation_errors:
                print(f"{error}")
            return False # print some message to frontend
        # transaction = Transaction(user.id, type, amount, category, description)
        self.repo.create_transaction(user, amount, type, date, category, description)
        return True

        # find user
        # connect to transaction db using user id
        # create a transaction using amount, type (income or expense), category
        # if: description, add description.
        # create and commit transaction
    def delete_transaction(self, transaction):
        self.repo.delete_transaction(transaction)
        pass

    def modify_transaction(self, transaction):
        # How do i want to  do this? i want to make it so that the "Amount", "Type", "Category" and "Description" fields of the transaction can be modified and then committed
        # Should i reserve this method to be used w/ a button that allows
        pass

    def get_transactions(self, user, filters):  # Change filters parameter to specific filters like amount and such once i figure out the specific implementation
        # return specific transactions that match the criteria
        # type
        # category
        # amount range
        # description key words?

        pass

    def get_all_transactions(self, user):
        #  just return all transactions
        self.repo.get_all_transactions(user)
        pass