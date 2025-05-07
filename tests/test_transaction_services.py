import unittest
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models.transaction import Transaction
from backend.services.transaction_service import TransactionService
from backend.services.user_service import UserService
from backend.utils.enums import IncomeOrExpense


class TestTransactionService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from backend.models.user import User
        from backend.models.transaction import Transaction
        from backend.models.conversion_rate import ConversionRate
        from backend.models.category import Category
        from backend.database import Base

        # Remove old test database
        db_path = os.path.abspath('transaction_test.db')
        if os.path.exists(db_path):
            os.remove(db_path)

        cls.engine = create_engine('sqlite:///transaction_test.db')
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

        Base.metadata.create_all(cls.engine)

        cls.user_service = UserService(cls.session)
        cls.trans_service = TransactionService(cls.session)

        # Create a test user
        cls.user = cls.user_service.register_user("testuser", "Test@1234")
        assert isinstance(cls.user, User)

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    def test_create_transaction_success(self):
        date = datetime.now()
        trans = self.trans_service.create_transaction(
            user=self.user,
            amount=50.0,
            type_str="income",
            date=date,
            category_id=1,
            description="Salary"
        )
        self.assertIsInstance(trans, Transaction)
        self.assertEqual(trans.amount, 50.0)
        self.assertEqual(trans.type, IncomeOrExpense.INCOME)

    def test_create_transaction_validation_error(self):
        result = self.trans_service.create_transaction(
            user=self.user,
            amount=-100.0,  # Invalid
            type_str="gift",  # Invalid
            date=datetime.now(),
            category_id=1,
            description="Bad transaction"
        )
        self.assertIsInstance(result, dict)
        self.assertIn("amount", result)
        self.assertIn("type", result)

    def test_delete_transaction_success(self):
        trans = self.trans_service.create_transaction(
            user=self.user,
            amount=20.0,
            type_str="expense",
            date=datetime.now(),
            category_id=2,
            description="Groceries"
        )
        success = self.trans_service.delete_transaction(trans)
        self.assertTrue(success)

    def test_modify_transaction_success(self):
        trans = self.trans_service.create_transaction(
            user=self.user,
            amount=100.0,
            type_str="income",
            date=datetime.now(),
            category_id=3,
            description="Bonus"
        )
        result = self.trans_service.modify_transaction(
            transaction=trans,
            amount=150.0,
            type_enum=IncomeOrExpense.INCOME,
            date=datetime.now(),
            category_id=3,
            description="Updated bonus"
        )
        self.assertTrue(result)

    def test_get_transactions(self):
        transactions = self.trans_service.get_transactions(user=self.user, filters={})
        self.assertIsInstance(transactions, list)

    def test_get_recent_transactions(self):
        self.trans_service.create_transaction(
            user=self.user,
            amount=10.0,
            type_str="expense",
            date=datetime.now(),
            category_id=4,
            description="Snacks"
        )
        recent = self.trans_service.get_recent_transactions(user=self.user, limit=2)
        self.assertLessEqual(len(recent), 2)

    def test_get_all_transactions(self):
        all_trans = self.trans_service.get_all_transactions(user=self.user)
        self.assertIsInstance(all_trans, list)

    def test_get_details(self):
        trans = self.trans_service.create_transaction(
            user=self.user,
            amount=5.0,
            type_str="expense",
            date=datetime.now(),
            category_id=5,
            description="Coffee"
        )
        details = self.trans_service.get_details(trans)
        self.assertIn("Transaction id", details)


if __name__ == '__main__':
    unittest.main()
