from backend.models.user import User

class UserRepository():
    """
    The repository used to connect to the user model
    """
    def __init__(self, session):
        self.session = session

    def rollback(self):
        """
        Rolls back the changes to the database.
        """
        self.session.rollback()

    def commit(self):
        """
        Commit the changes to the database.
        """
        self.session.commit()

    def create_user(self, username: str, hashed_password: str) -> User:
        """
        Creates a new user using the given username and hashed password.
        Args:
            username (str): The username of the user.
            hashed_password (str): The hashed password of the user.
        Returns:
            User: The new user.
        """
        user = User(username=username,
                    password_hash=hashed_password,
                    account_balance=0)
        self.session.add(user)
        return user

    def find_user(self, username: str) -> User | None:
        """
        Finds a user using the given username.
        Args:
            username (str): The username of the user.
        Returns:
            User: The user matching the given username.
            None: The user was not found.
        """
        return self.session.query(User).filter_by(username=username).first()

    def delete_user(self, user: User):
        """
        Deletes a user using the given user instance.
        Args:
            user (User): The user instance.
        """
        self.session.delete(user)

    def get_current_balance(self, user: User) -> float:
        """
        Returns the current balance of the given user.
        Args:
            user (User): The user instance.
        """
        return user.account_balance

    def change_balance(self, user: User, balance: float):
        """
        Changes the balance of the given user.
        Args:
            user (User): The user instance.
            balance (float): The new balance of the user.
        """
        user.account_balance = balance

    def change_password(self, user: User, new_hashed_password: str):
        """
        Changes the password of the given user.
        Args:
            user (User): The user instance.
            new_hashed_password (str): The new hashed password of the user.
        """
        user.password_hash = new_hashed_password
