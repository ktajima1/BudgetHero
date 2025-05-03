import unittest
import sys
import os

from backend.database import initialize_database, get_session
from backend.models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, session
from backend.services.auth_service import AuthService


#
# if __name__ == "__main__":
#     delete_user("admin", "12345L@w")
#     create_user("admin", "10936S@n")
#     login_user("admin", "10936S@n")
#     login_user("admin", "12345L@w")
#     change_password("admin", "12345L@w")
#     login_user("admin", "10936S@n")
#     login_user("admin", "12345L@w")

class TestUserMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from backend.models.user import User
        from backend.database import Base

        # Delete test_db to refresh
        db_path = os.path.abspath('test.db')
        if os.path.exists(db_path):
            os.remove(db_path)

        # Create engine and session
        cls.engine = create_engine('sqlite:///test.db')
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

        Base.metadata.create_all(cls.engine)

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    # def test_create_user(self):
    #     print("Test: Creating user <start>:")
    #     _create_user(self.session, "admin", "10936S@n")
    #     print("Test: Creating user <end>:")
    #     user = self.session.query(User).filter_by(username="admin").first()
    #     self.assertIsNotNone(user, "User should exist in database")
    #     self.assertEqual(user.username, "admin")
    #
    # def test_login_user(self):
    #     print("Test: Login user <start>:")
    #     _login_user(self.session, "admin", "10936S@n")
    #     print("Test: Creating user <end>:")
    #
    # def test_change_password(self):
    #     print("Test: Change password <start>:")
    #     _change_password(self.session, "admin", "12345Me@w")
    #     print("Test: Change password <end>:")
    #
    # def test_delete_user(self):
    #     print("Test: Delete user <start>:")
    #     _delete_user(self.session, "admin", "10936S@n")
    #     print("Test: Delete user <end>:")
    #     user = self.session.query(User).filter_by(username="admin").first()
    #     self.assertIsNone(user, "User should not exist in database")

    def test_user_methods(self):
        auth_service = AuthService(self.session)

        auth_service.delete_user("admin", "12345L@w")
        auth_service.delete_user("admin", "10936S@n")
        auth_service.register_user("admin", "10936S@n")
        auth_service.login_user("admin", "10936S@n")
        auth_service.login_user("admin", "12345L@w")
        auth_service.change_password("admin", "12345L@w")
        auth_service.login_user("admin", "10936S@n")
        auth_service.login_user("admin", "12345L@w")

if __name__ == '__main__':
    unittest.main() #this is the normal usage
    #or using console. python -m unittest scriptname.py