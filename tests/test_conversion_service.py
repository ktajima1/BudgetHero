import unittest
import os
from datetime import datetime, date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models.conversion_rate import ConversionRate
from backend.services.conversion_service import ConversionService

class TestConversionService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from backend.models.user import User
        from backend.models.transaction import Transaction
        from backend.models.conversion_rate import ConversionRate
        from backend.models.category import Category
        from backend.database import Base

        db_path = os.path.abspath('conversion_test.db')
        if os.path.exists(db_path):
            os.remove(db_path)

        cls.engine = create_engine('sqlite:///conversion_test.db')
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

        Base.metadata.create_all(cls.engine)

        cls.service = ConversionService(cls.session)

        cls.base_currency = "USD"
        cls.target_currency = "EUR"
        cls.today = date.today()  # Correct: only date, not datetime
        cls.rate = 1.1

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    def test_log_rate_success(self):
        rate = self.service.log_rate(self.base_currency, self.target_currency, self.today, self.rate)
        self.assertIsInstance(rate, ConversionRate)
        self.assertEqual(rate.base_currency, self.base_currency)
        self.assertEqual(rate.target_currency, self.target_currency)

    def test_log_rate_validation_error(self):
        result = self.service.log_rate("FAKE", self.target_currency, self.today, -5)
        self.assertIsInstance(result, dict)
        self.assertIn("base_currency", result)
        self.assertIn("rate", result)

    def test_get_rate_from_db(self):
        # Ensure there's a rate in the DB
        self.service.log_rate(self.base_currency, self.target_currency, self.today, self.rate)
        rate = self.service.get_rate(self.base_currency, self.target_currency, self.today)
        self.assertIsInstance(rate, ConversionRate)

    def test_delete_rate_success(self):
        conv = self.service.log_rate(self.base_currency, "JPY", self.today, 150.0)
        success = self.service.delete_rate(conv)
        self.assertTrue(success)

    def test_change_rate_success(self):
        conv = self.service.log_rate("USD", "GBP", self.today, 0.75)
        success = self.service.change_rate(conv, 0.77)
        self.assertTrue(success)
        updated = self.service.repo.get_rate("USD", "GBP", self.today)
        self.assertEqual(updated.rate, 0.77)

    def test_get_details(self):
        conv = self.service.log_rate("USD", "CAD", self.today, 1.25)
        details = self.service.get_details(conv)
        self.assertIn("Base Currency: USD", details)
        self.assertIn("Target Currency: CAD", details)
        self.assertIn("Rate: 1.25", details)


if __name__ == '__main__':
    unittest.main()
