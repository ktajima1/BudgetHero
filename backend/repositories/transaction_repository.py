from sqlite3 import IntegrityError
from backend.models.transaction import Transaction
from backend.database import get_session
from backend.services.transaction import *

def create_transaction(user, type, amount, category, description):
    # find user
    # connect to transaction db using user id
    # create a transaction using amount, type (income or expense), category
    # if: description, add description.
    # create and commit transaction
    pass

def delete_transaction(transaction):
    pass

def modify_transaction(transaction):
    # How do i want to  do this? i want to make it so that the "Amount", "Type", "Category" and "Description" fields of the transaction can be modified and then committed
    # Should i reserve this method to be used w/ a button that allows
    pass

def create_category(category):
    pass

def delete_category(category):
    pass

def get_transactions(user, filters): # Change filters parameter to specific filters like amount and such once i figure out the specific implementation
    # return specific transactions that match the criteria
    # type
    # category
    # amount range
    # description key words?
    pass

def get_all_transactions(user):
    #  just return all transactions
    pass

def get_all_categories():
    pass