from sqlite3 import IntegrityError
from backend.repositories.auth_repository import AuthRepository
from backend.errors import InvalidPasswordError

import re

class AuthService:
    def __init__(self, session):
        self.repo = AuthRepository(session)

    def register_user(self, username, password):
        # Check that username fits requirements. Uniqueness is checked when adding user to database via catching DuplicateUsernameError
        username_errors = validate_username(username)
        # Check that password fits requirements
        password_errors = validate_password(password)

        if username_errors:
            print("username error")
            return False  # Code should display message on frontend for what errors exist with the username

        if password_errors:
            for error in password_errors:
                print(f"password error: {error}")
            return False  # Code should display message on frontend for what errors exist with the password

        hashed_password = hash_password(password)  # Hash the password to store in database
        print("preparing to create user")
        try:
            self.repo.create_user(username, hashed_password)
            print("created user")
            return True
        except IntegrityError:
            print("user already exists")
            return False

    def login_user(self, username, password):
        try:
            print("logging in")
            user = self.repo.find_user(username)
            if user and user.password_hash == hash_password(password):
                print("logged in")
                return user
            else:
                print("login failed")
                return None
        except Exception as e:
            print(f"login error: {e}")

    def change_password(self, username, new_password):
        try:
            password_errors = validate_password(new_password)
            if password_errors:
                for error in password_errors:
                    print(f"password error: {error}")
                print("CHANGE PASSWORD FAILED:")
                return False

            user = self.repo.find_user(username)
            new_hashed_password = hash_password(new_password)
            self.repo.change_password(user, new_hashed_password)
            print("CHANGE PASSWORD SUCCESSFUL")
            return True
        except Exception as e:
            print(f"changing password error: {e}")

    def delete_user(self, username, password):
        try:
            user = self.repo.find_user(username)
            if user is None:
                print("DELETION FAILED: user does not exist")
                return False
            else:
                hashed_password = hash_password(password)
                if user.password_hash == hashed_password:
                    self.repo.delete_user(user)
                    print("deleted user")
                else:
                    print("DELETE FAILED: password does not match")
        except Exception as e:
            print(f"deletion error: {e}")

# Look up hashing algorithm for passwords
def hash_password(password):
    return password + "hashed"

# Username requirements:
#   - Must be 4 or more characters long
def validate_username(username):
    errors = {}
    if len(username) < 4:
        errors["length"] = "Username must be at least 4 characters long"
    return errors if errors else None

# Requirements:
# - 1 capital letter
# - 1 lowercase letter
# - 1 number
# - 1 symbol
# - 8 or more characters
def validate_password(password):
    errors = {}
    if len(password) < 8:
        errors["length"] = "Password must be at least 8 characters long"
    # Check for at least 1 capital letter
    if not re.search(r'[A-Z]', password):
        errors["capital"] = "Password must contain at least 1 capital letter"
    # Check for at least 1 lowercase letter
    if not re.search(r'[a-z]', password):
        errors["lowercase"] = "Password must contain at least 1 lowercase letter"
    # Check for at least 1 number
    if not re.search(r'[0-9]', password):
        errors["number"] = "Password must contain at least 1 number"
    # Check for at least 1 symbol (adjust the symbol characters as needed)
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors["symbol"] = "Password must contain at least 1 symbol"
    return errors if errors else None

