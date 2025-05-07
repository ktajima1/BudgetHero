from backend.utils.enums import IncomeOrExpense
from backend.models.transaction import Transaction
from backend.models.user import User
from sqlalchemy import or_, func, desc
from datetime import datetime
from typing import Any, List, Dict


class TransactionRepository():
    def __init__(self, session):
        self.session = session

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()

    def create_transaction(self, user: User, amount: float, type_enum: IncomeOrExpense, date: datetime, category_id: int, description: str) -> Transaction:
        transaction = Transaction(
            user_id=user.id,
            amount=amount,
            type=type_enum,
            date=date, category_id=category_id,
            description=description
        )
        self.session.add(transaction)
        # find user
        # connect to transaction db using user id
        # create a transaction using amount, type (income or expense), category
        # if: description, add description.
        # create and commit transaction
        return transaction

    def delete_transaction(self, transaction: Transaction):
        self.session.delete(transaction)

    def modify_transaction(self, transaction: Transaction, amount: float, type_enum: IncomeOrExpense, date: datetime, category_id: int, description: str):
        # How do i want to  do this? i want to make it so that the "Amount", "Type", "Category" and "Description" fields of the transaction can be modified and then committed
        # Should i reserve this method to be used w/ a button that allows
        if amount is not None:
            transaction.amount = amount
        if type_enum is not None:
            transaction.type = type_enum
        if date is not None:
            transaction.date = date
        if category_id is not None:
            transaction.category_id = category_id
        if description is not None:
            transaction.description = description
        print(f"[trans_repo.modify_trans]: Updated transaction {transaction.id}")

    def get_transactions(self, user: User, filters: Dict[str, Any]) -> List[Transaction]:
        # return specific transactions that match the criteria
        # initially get full all transactions for user
        query = self.session.query(Transaction).filter_by(user_id=user.id)

        # filter by transaction id
        # Note: filtering by transaction id is a direct search for a specific id
        # and will return a single transaction
        if 'id' in filters and filters['id'] is not None:
            query = query.filter_by(id=filters['id'])

        # filter by type (income or expense)
        # note: filter['type'] should be an IncomeOrExpense ENUM value
        if 'type_enum' in filters and filters['type_enum'] is not None:
            query = query.filter(Transaction.type == filters['type_enum'])

        # filter by category (note, filters['category'] must contain category_id
        if 'category' in filters and filters['category'] is not None:
            query = query.filter(Transaction.category_id == filters['category'])

        # filter by amount range
        if 'min_amount' in filters and filters['min_amount'] is not None:
            query = query.filter(Transaction.amount >= filters['min_amount'])
        if 'max_amount' in filters and filters['max_amount'] is not None:
            query = query.filter(Transaction.amount <= filters['max_amount'])

        # filter by keywords in description
        if 'description' in filters and filters['description']:
            keywords = filters['description']
            for keyword in keywords:
                query = query.filter(or_(func.lower(Transaction.description.contains(keyword.lower()))))
        print("trans_repo.get_trans: returning transactions that match filters")
        return query.all()

    def get_recent_transactions(self, user: User, limit: int = 5) -> List[Transaction]:
        print(f"[trans_repo.get_recent_trans]: Fetching {limit} recent transactions for user {user.id}")
        return (
            self.session.query(Transaction)
            .filter_by(user_id=user.id)
            .order_by(desc(Transaction.date))
            .limit(limit)
            .all()
        )

    def get_all_transactions(self, user: User) -> List[Transaction]:
        #  just return all transactions
        all_transactions = self.session.query(Transaction).filter_by(user_id=user.id).all()  # Does this return a list?
        print("Returning all transactions")
        return all_transactions
