from backend.models.transaction import Transaction

class TransactionRepository():
    def __init__(self, session):
        self.session = session

    def create_transaction(self, user, amount, type, date, category, description):
        transaction = Transaction(user.id, amount, type, date, category, description)
        self.session.add(transaction)
        self.session.commit()
        # find user
        # connect to transaction db using user id
        # create a transaction using amount, type (income or expense), category
        # if: description, add description.
        # create and commit transaction
        return transaction

    def delete_transaction(self, transaction):
        self.session.delete(transaction)
        self.session.commit()

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
        list_of_transactions = self.session.query(Transaction).filter_by(#FILTERS HERE).all() # Does this return a list?
        return list_of_transactions

    def get_all_transactions(self, user):
        #  just return all transactions
        all_transactions = self.session.query(Transaction).filter_by(user_id=user.id).all()  # Does this return a list?
        return all_transactions
