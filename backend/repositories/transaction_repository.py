from backend.utils.enums import IncomeOrExpense
from backend.models.transaction import Transaction
from backend.models.user import User
from sqlalchemy import or_, func, desc
from datetime import datetime
from typing import Any, List, Dict


class TransactionRepository():
    """
    This is the repository for the transaction model
    """
    def __init__(self, session):
        self.session = session

    def rollback(self):
        """
        Rollback the session
        """
        self.session.rollback()

    def commit(self):
        """
        Commit changes to the database.
        """
        self.session.commit()

    def create_transaction(self, user: User, amount: float, type_enum: IncomeOrExpense, date: datetime, category_id: int, description: str) -> Transaction:
        """
        Creates a new transaction for the given user

        Args:
            user (User): the user to create the transaction for
            amount (float): the amount of the transaction
            type_enum (IncomeOrExpense): the type of income or expense
            date (datetime): the date of the transaction
            category_id (int): the category id of the transaction
            description (str): the description of the transaction

        Returns:
            Transaction: the transaction
        """
        transaction = Transaction(
            user_id=user.id,
            amount=amount,
            type=type_enum,
            date=date, category_id=category_id,
            description=description
        )
        self.session.add(transaction)
        return transaction

    def delete_transaction(self, transaction: Transaction):
        """
        Deletes a transaction from the database

        Args:
            transaction (Transaction): the transaction to delete
        """
        self.session.delete(transaction)

    def modify_transaction(self, transaction: Transaction, amount: float, type_enum: IncomeOrExpense, date: datetime, category_id: int, description: str):
        """
        Modifies a transaction from the database

        Args:
            transaction (Transaction): the transaction to modify
            amount (float): the new amount of the transaction
            type_enum (IncomeOrExpense): the type of transaction, income or expense
            date (datetime): the new date of the transaction
            category_id (int): the new category id of the transaction
            description (str): the new description of the transaction
        """
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
        """
        Returns a list of transactions for the given user that matches the given criteria in filters

        Args:
            user (User): the user to get the transactions for
            filters (Dict[str, Any]): the filters to apply to the transactions

        Returns:
            List[Transaction]: the list of matching transactions
        """
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
        """
        Returns a list of the n recent transactions for the given user (default to 5)

        Args:
            user (User): the user to get the transactions for
            limit (int): the number of transactions to return (default to 5)

        Returns:
            List[Transaction]: the list of matching transactions
        """
        print(f"[trans_repo.get_recent_trans]: Fetching {limit} recent transactions for user {user.id}")
        return (
            self.session.query(Transaction)
            .filter_by(user_id=user.id)
            .order_by(desc(Transaction.date))
            .limit(limit)
            .all()
        )

    def get_all_transactions(self, user: User) -> List[Transaction]:
        """
        Returns a list of all transactions for the given user

        Args:
            user (User): the user to get the transactions for
        Returns:
            List[Transaction]: the list of matching transactions
        """
        #  just return all transactions
        all_transactions = self.session.query(Transaction).filter_by(user_id=user.id).all()  # Does this return a list?
        print("Returning all transactions")
        return all_transactions
