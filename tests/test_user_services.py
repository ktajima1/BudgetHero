import unittest
import sys
import os
from backend.models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, session
from backend.controllers.auth_controller import _create_user, _login_user, _change_password, _delete_user
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
        # Create base, engine and session
        cls.Base = declarative_base()
        cls.engine = create_engine('sqlite:///test.db')
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

        cls.Base.metadata.create_all(cls.engine)
        

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        db_path = "tests/test.db"
        if os.path.exists(db_path):
            os.remove(db_path)

    def test_create_user(self):
        _create_user(session, "admin", "10936S@n")
        user = self.session.query(User).filter_by(username="admin").first()
        self.assertEqual(user.username, "admin")


if __name__ == '__main__':
    #print(sys.argv)
    # unittest.main(argv=[''], exit=False) # use this option for jupyter notebooks, Reason: sys.argv is used in unittest call. First parameter must be the script to be tested. But in notebook, the first parameter is either IPython or Jupyter. So, you will get an the error about kernel connection.
    unittest.main() #this is the normal usage
    #or using console. python -m unittest scriptname.py