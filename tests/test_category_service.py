import unittest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models.category import Category
from backend.services.category_service import CategoryService
class TestCategoryService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from backend.models.user import User
        from backend.models.transaction import Transaction
        from backend.models.conversion_rate import ConversionRate
        from backend.models.category import Category
        from backend.database import Base

        db_path = os.path.abspath("category_test.db")
        if os.path.exists(db_path):
            os.remove(db_path)
        cls.engine = create_engine("sqlite:///category_test.db")
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    def test_create_category(self):
        service = CategoryService(self.session)

        # Invalid (empty name)
        result = service.create_category("", "A description")
        self.assertIn("category_name", result)

        # Valid
        category = service.create_category("Food", "Food related expenses")
        self.assertIsInstance(category, Category)

    def test_modify_category(self):
        service = CategoryService(self.session)
        category = service.create_category("Transport", "Transport expenses")

        # Modify with valid data
        result = service.modify_category(category, "Travel", "Updated description")
        self.assertTrue(result)

        # Modify with invalid name
        result = service.modify_category(category, "", "Desc")
        self.assertIn("category_name", result)

    def test_delete_category(self):
        service = CategoryService(self.session)
        category = service.create_category("Utilities", "Utility bills")
        result = service.delete_category(category)
        self.assertTrue(result)

    def test_get_methods(self):
        service = CategoryService(self.session)
        category = service.create_category("Leisure", "Leisure activities")

        # Get by id
        found = service.get_category_by_id(category.id)
        self.assertEqual(found.category_name, "leisure")

        # Get by name (partial match)
        matches = service.get_category_by_name("lei")
        self.assertTrue(any(c.category_name == "leisure" for c in matches))

        # Get all
        all_categories = service.get_all_categories()
        self.assertGreaterEqual(len(all_categories), 1)

    def test_get_details(self):
        service = CategoryService(self.session)
        category = service.create_category("Misc", "Miscellaneous")
        details = service.get_details(category)
        self.assertIn("Category id", details)


if __name__ == "__main__":
    unittest.main()
