import unittest
import os

from backend.models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.services.user_service import UserService
from backend.utils.enums import IncrementOrDecrement


class TestUserMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from backend.models.user import User
        from backend.models.transaction import Transaction
        from backend.models.conversion_rate import ConversionRate
        from backend.models.category import Category
        from backend.database import Base

        # Delete test_db to refresh
        db_path = os.path.abspath('user_test.db')
        if os.path.exists(db_path):
            os.remove(db_path)

        # Create engine and session
        cls.engine = create_engine('sqlite:///user_test.db')
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

        Base.metadata.create_all(cls.engine)

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    def test_create_user(self):
        auth_service = UserService(self.session)

        # Invalid username
        result = auth_service.register_user("abc", "Valid1@Password")
        self.assertIn("length", result)

        # Invalid password
        result = auth_service.register_user("validuser", "short")
        self.assertIn("length", result)

        # Valid registration
        user = auth_service.register_user("testuser", "Valid1@Password")
        self.assertIsInstance(user, User)

        # Duplicate username
        duplicate = auth_service.register_user("testuser", "Valid1@Password")
        self.assertIsNone(duplicate)

    def test_login_user(self):
        auth_service = UserService(self.session)
        auth_service.register_user("loginuser", "Login1@Pass")

        # Successful login
        user = auth_service.login_user("loginuser", "Login1@Pass")
        self.assertIsNotNone(user)

        # Incorrect password
        user = auth_service.login_user("loginuser", "WrongPass1@")
        self.assertIsNone(user)

        # Nonexistent user
        user = auth_service.login_user("nouser", "Login1@Pass")
        self.assertIsNone(user)

    def test_change_password(self):
        auth_service = UserService(self.session)
        auth_service.register_user("changepassuser", "Change1@Pass")

        # Invalid password
        result = auth_service.change_password("changepassuser", "short")
        self.assertIn("length", result)

        # Valid password change
        result = auth_service.change_password("changepassuser", "NewValid1@")
        self.assertTrue(result)

        # Confirm login works with new password
        user = auth_service.login_user("changepassuser", "NewValid1@")
        self.assertIsNotNone(user)

    def test_delete_user(self):
        auth_service = UserService(self.session)
        auth_service.register_user("deleteuser", "Delete1@Pass")

        # Wrong password
        result = auth_service.delete_user("deleteuser", "Wrong1@Pass")
        self.assertFalse(result)

        # Correct password
        result = auth_service.delete_user("deleteuser", "Delete1@Pass")
        self.assertTrue(result)

        # Try to login after deletion
        user = auth_service.login_user("deleteuser", "Delete1@Pass")
        self.assertIsNone(user)

    def test_user_methods(self):
        auth_service = UserService(self.session)
        auth_service.register_user("checkuser", "Check1@User")

        # Check if user exists
        self.assertTrue(auth_service.check_if_user_exists("checkuser"))
        self.assertFalse(auth_service.check_if_user_exists("ghostuser"))

        # Check balance and update
        user = auth_service.login_user("checkuser", "Check1@User")
        original_balance = auth_service.get_current_balance(user)
        updated_balance = auth_service.update_balance(user, 50, IncrementOrDecrement.INCREMENT)
        self.assertEqual(updated_balance, original_balance + 50)

        updated_balance = auth_service.update_balance(user, 20, IncrementOrDecrement.DECREMENT)
        self.assertEqual(updated_balance, original_balance + 30)


if __name__ == '__main__':
    unittest.main() #this is the normal usage
    #or using console. python -m unittest scriptname.py